import cv2
import os
import numpy as np
import mediapipe as mp
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import pickle
from .models import UserFace
from django.core.files.base import ContentFile
import uuid
import requests
from django.http import JsonResponse

# Configurações do MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Configurações
FACE_DETECTOR = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
FACES_DIR = os.path.join(settings.MEDIA_ROOT, 'faces')
os.makedirs(FACES_DIR, exist_ok=True)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'recognizer/face_model.yml')
MAPPINGS_PATH = os.path.join(settings.BASE_DIR, 'recognizer/mappings.pkl')
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Variáveis globais inicializadas
face_samples = []
ids = []
name_to_id = {}
id_to_name = {}
id_count = 0
TESTE = False #Flag para indicar uso ou não do ESP (True = sem ESP)


def load_model():
    global RECOGNIZER, id_count, name_to_id, id_to_name

    if os.path.exists(MODEL_PATH):
        RECOGNIZER.read(MODEL_PATH)

    if os.path.exists(MAPPINGS_PATH):
        with open(MAPPINGS_PATH, 'rb') as f:
            name_to_id, id_to_name = pickle.load(f)
            id_count = max(id_to_name.keys(), default=0) + 1


def save_model():
    RECOGNIZER.write(MODEL_PATH)
    with open(MAPPINGS_PATH, 'wb') as f:
        pickle.dump((name_to_id, id_to_name), f)


def preprocess_face(face_img):
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(gray)


def count_open_fingers(landmarks, hand_label="Right"):
    fingers = []

    if hand_label == "Right":
        if landmarks.landmark[4].x < landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else: 
        if landmarks.landmark[4].x > landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

    tips_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for tip, pip in zip(tips_ids, pip_ids):
        if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

def register_face(request):
    global id_count

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, "Nome é obrigatório")
            return redirect('register_face')

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messages.error(request, "Não foi possível acessar a câmera")
            return redirect('register_face')

        sample_count = 0
        cv2.namedWindow('Cadastro Facial', cv2.WINDOW_NORMAL)

        user_dir = os.path.join(FACES_DIR, name.lower().replace(' ', '_'))
        os.makedirs(user_dir, exist_ok=True)

        while sample_count < 30:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = FACE_DETECTOR.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_roi = preprocess_face(frame[y:y + h, x:x + w])

                if name not in name_to_id:
                    name_to_id[name] = id_count
                    id_to_name[id_count] = name
                    id_count += 1

                filename = f"{uuid.uuid4().hex}.jpg"
                filepath = os.path.join(user_dir, filename)

                resized_face = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
                cv2.imwrite(filepath, resized_face)

                user_face = UserFace(name=name)
                user_face.image.save(filename, ContentFile(open(filepath, 'rb').read()))
                user_face.save()

                face_samples.append(resized_face)
                ids.append(name_to_id[name])
                sample_count += 1

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Amostras: {sample_count}/30", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('Cadastro Facial', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if sample_count > 0:
            RECOGNIZER.train(np.array(face_samples), np.array(ids))
            save_model()
            messages.success(request, f"{name} cadastrado com sucesso!")
        else:
            messages.warning(request, "Nenhuma face detectada")

        return redirect('index')

    return render(request, 'core/register.html')

def recognize_face_and_hand(request):
    load_model()
    
    if not id_to_name:
        messages.error(request, "Nenhum rosto cadastrado")
        return redirect('index')
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messages.error(request, "Câmera indisponível")
        return redirect('index')
    
    recognized_name = None
    hand_state = None  # 'open' ou 'closed'
    confidence_threshold = 80
    
    cv2.namedWindow('Verificação de Acesso', cv2.WINDOW_NORMAL)
    
    while recognized_name is None or hand_state is None:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Processamento para reconhecimento facial
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_DETECTOR.detectMultiScale(gray, 1.3, 5)
        
        # Processamento para detecção de mãos (usa imagem colorida)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        # Reconhecimento facial
        face_detected = False
        for (x, y, w, h) in faces:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            
            id_, confidence = RECOGNIZER.predict(face_roi)
            
            if confidence < confidence_threshold and id_ in id_to_name:
                recognized_name = id_to_name[id_]
                color = (0, 255, 0)
                text = recognized_name
                face_detected = True
            else:
                color = (0, 0, 255)
                text = "Desconhecido"
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # Detecção de mão
        if results.multi_hand_landmarks and face_detected:
            for hand_landmarks in results.multi_hand_landmarks:
                dedos = count_open_fingers(hand_landmarks)
                abertura = min(dedos * 20, 100)

                if TESTE:
                    print(f"[SIMULADO] Enviando para ESP32: abertura = {abertura}%")
                else:
                    try:
                        esp_ip = 'http://192.168.137.60'
                        payload = {"abertura": abertura}
                        headers = {"Content-Type": "application/json"}
                        requests.post(f"{esp_ip}/abrir", json=payload, headers=headers, timeout=3)
                    except Exception as e:
                        cap.release()
                        return JsonResponse({"erro": f"Erro ao comunicar com ESP32: {e}"}, status=500)

                request.session['recognized'] = True
                request.session['user_name'] = recognized_name
                request.session['gate_open'] = True
                request.session['abertura'] = abertura

                cap.release()
                cv2.destroyAllWindows()
                
                if recognized_name and dedos:
                    # Redireciona para a tela de acesso liberado
                    return redirect('gate_open', user_name=recognized_name)
                else:
                    if recognized_name:
                        # messages.warning(request, "Acesso negado: mostre a mão aberta para liberar")
                        return render(request, 'core/gate_closed.html')
                    else:
                        messages.error(request, "Rosto não reconhecido")
                    return redirect('index')


def gate_open(request, user_name):
    user_name = request.session.get('user_name', 'Desconhecido')
    abertura = request.session.get('abertura', 0)

    context = {
        'user_name': user_name,
        'gate_open': True,
        'abertura': abertura,
        'message': f"Acesso liberado com {abertura}% de abertura"
    }
    return render(request, 'core/gate_open.html', context)



def index(request):
    context = {}
    if 'recognized' in request.session:
        context = {
            'recognized': request.session['recognized'],
            'user_name': request.session.get('user_name', ''),
            'gate_open': request.session.get('gate_open', False)
        }
        request.session.pop('recognized', None)
        request.session.pop('user_name', None)
        request.session.pop('gate_open', None)

    return render(request, 'core/index.html', context)