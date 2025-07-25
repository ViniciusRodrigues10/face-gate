import network
import socket
import ujson
import time
from machine import Pin, PWM

# === CONFIG Wi-Fi ===
SSID = 'SEU_WIFI'
PASSWORD = 'SUASENHA'

# === PWM ===
servo = PWM(Pin(13), freq=50)

# === LED ===
led = Pin(2, Pin.OUT)  # LED no GPIO 2 (ajuste conforme necessário)
led.off()  # Começa apagado

# === Conectar-se ao Wi-Fi ===
def conecta_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print("Wi-Fi conectado!")
    print("IP:", wlan.ifconfig()[0])

# === Traduz % de abertura para PWM de servo ===
def porcentagem_para_pwm(abertura):
    abertura = max(0, min(180, abertura))  # limitar entre 0 e 100
    min_duty = 40   # 0 graus ≈ 0.5ms
    max_duty = 115  # 180 graus ≈ 2.5ms
    duty = int(min_duty + (abertura /180) * (max_duty - min_duty))
    return duty

# === Servidor HTTP ===
def iniciar_servidor():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Servidor HTTP iniciado em http://%s:80" % network.WLAN(network.STA_IF).ifconfig()[0])

    while True:
        cl, addr = s.accept()
        print("Cliente conectado:", addr)
        try:
            req = cl.recv(1024)
            req_str = req.decode()

            if "POST /abrir" in req_str:
                try:
                    # Separa cabeçalho e corpo
                    cabecalho, corpo_inicial = req_str.split("\r\n\r\n", 1)

                    # Busca o tamanho do corpo
                    content_length = 0
                    for linha in cabecalho.split("\r\n"):
                        if "Content-Length" in linha:
                            content_length = int(linha.split(":")[1].strip())
                            break

                    # Se o corpo que veio com o primeiro recv for incompleto, leia o restante
                    while len(corpo_inicial) < content_length:
                        corpo_inicial += cl.recv(1024).decode()

                    # Agora o corpo está completo
                    print("Corpo recebido:")
                    print(corpo_inicial)
                    dados = ujson.loads(corpo_inicial)

                    # Processa o JSON
                    abertura = dados.get("abertura", 0)
                    duty = porcentagem_para_pwm(abertura)
                    servo.duty(duty)
                    print(f"🔧 Abertura: {abertura}% -> PWM duty: {duty}")


                    # Resposta de sucesso
                    resposta = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n'
                    resposta += ujson.dumps({"status": "OK", "abertura": abertura})
                    cl.send(resposta)

                except Exception as e:
                    print("Erro ao processar JSON:", e)
                    cl.send('HTTP/1.1 400 Bad Request\r\n\r\n')
            # Adicione isso dentro de iniciar_servidor(), junto com os outros ifs

            elif "POST /led" in req_str:
                try:
                    cabecalho, corpo_inicial = req_str.split("\r\n\r\n", 1)
                    content_length = 0
                    for linha in cabecalho.split("\r\n"):
                        if "Content-Length" in linha:
                            content_length = int(linha.split(":")[1].strip())
                            break

                    while len(corpo_inicial) < content_length:
                        corpo_inicial += cl.recv(1024).decode()

                    dados = ujson.loads(corpo_inicial)
                    estado = dados.get("estado", "")

                    if estado == "on":
                        led.on()
                        print(f"LED LIGADO")
                    elif estado == "off":
                        led.off()

                    resposta = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n'
                    resposta += ujson.dumps({"status": "LED atualizado", "estado": estado})
                    cl.send(resposta)

                except Exception as e:
                    print("Erro ao processar LED:", e)
                    cl.send('HTTP/1.1 400 Bad Request\r\n\r\n')

            else:
                cl.send('HTTP/1.1 404 Not Found\r\n\r\n')

        finally:
            cl.close()


# === Executar ===
conecta_wifi()
iniciar_servidor()

