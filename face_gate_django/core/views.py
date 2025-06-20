import cv2
import os
import uuid
import base64
from django.shortcuts import render, redirect
from .models import UserFace
import numpy as np
from django.conf import settings
from django.core.files.base import ContentFile

MEDIA_DIR = os.path.join(settings.MEDIA_ROOT, 'faces')

SAMPLES_PER_USER = 20  # Número de amostras por pessoa

def index(request):
    return render(request, 'core/index.html')

def register_face(request):
    if request.method == 'POST':
        name = request.POST['name']
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        saved = 0
        os.makedirs(MEDIA_DIR, exist_ok=True)

        while saved < SAMPLES_PER_USER:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                roi_color = frame[y:y+h, x:x+w]
                filename = f"{uuid.uuid4().hex}.png"
                filepath = os.path.join(MEDIA_DIR, filename)
                cv2.imwrite(filepath, roi_color)
                UserFace.objects.create(name=name, image=f"faces/{filename}")
                saved += 1

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Capturado {saved}/{SAMPLES_PER_USER}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.imshow('Cadastro Facial', frame)
                cv2.waitKey(500)
                break

        cap.release()
        cv2.destroyAllWindows()
        return redirect('index')

    return render(request, 'core/register.html')

def train_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_map = {}
    label_id = 0
    name_to_label = {}

    for face in UserFace.objects.all():
        path = os.path.join(settings.MEDIA_ROOT, face.image.name.replace("\\", "/"))
        if not os.path.exists(path):
            print(f"Arquivo não encontrado: {path}")
            continue
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Erro ao carregar imagem: {path}")
            continue
        if face.name not in name_to_label:
            name_to_label[face.name] = label_id
            label_map[label_id] = face.name
            label_id += 1
        faces.append(img)
        labels.append(name_to_label[face.name])

    if not faces:
        return None, None

    recognizer.train(faces, np.array(labels))
    return recognizer, label_map

# def recognize_face(request):
#     recognizer, label_map = train_recognizer()
#     if recognizer is None:
#         return render(request, 'core/index.html', {'message': 'Nenhuma face cadastrada para reconhecimento.'})

#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()
#     if not ret:
#         return render(request, 'core/index.html', {'message': 'Não foi possível capturar a imagem da webcam.'})

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

#     for (x, y, w, h) in faces:
#         roi = gray[y:y+h, x:x+w]
#         label, confidence = recognizer.predict(roi)
#         # Ajuste do limiar para aceitar somente confiável
#         if confidence < 50:  
#             name = label_map[label]
#             return render(request, 'core/index.html', {'message': f"Acesso autorizado para {name}. Abrindo portão..."})

#     return render(request, 'core/index.html', {'message': 'Acesso negado. Rosto não reconhecido.'})


def recognize_face(request):
    recognizer, label_map = train_recognizer()
    if recognizer is None:
        return render(request, 'core/index.html', {'message': 'Nenhuma face cadastrada para reconhecimento.'})

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    success_count = {}
    frame_count = 0
    max_frames = 20

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(roi)
            print(f"[DEBUG] Frame {frame_count}: label={label}, confiança={confidence:.2f}")

            if confidence < 45:
                name = label_map[label]
                success_count[name] = success_count.get(name, 0) + 1

                # Se uma pessoa for reconhecida >=3 vezes, autoriza
                if success_count[name] >= 3:
                    cap.release()
                    return render(request, 'core/index.html', {'message': f"Acesso autorizado para {name}. Abrindo portão..."})

        frame_count += 1
        cv2.waitKey(50)  # aguarda um pouco entre os frames

    cap.release()
    return render(request, 'core/index.html', {'message': 'Acesso negado. Rosto não reconhecido.'})
