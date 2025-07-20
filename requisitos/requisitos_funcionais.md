# ✅ Requisitos Funcionais – Projeto de Controle de Acesso com Reconhecimento Facial e Gestos

Este documento descreve os requisitos funcionais do sistema, ou seja, o que o sistema deve fazer para cumprir seus objetivos.

---

## RF01 – Captura de imagens em tempo real
O sistema deve capturar imagens do rosto dos usuários em tempo real através de uma câmera conectada, sempre que uma presença for detectada.

---

## RF02 – Autenticação por reconhecimento facial
O sistema deve comparar as imagens capturadas com um banco de dados de rostos cadastrados para autenticar o usuário.

---

## RF03 – Detecção de gestos manuais
Após autenticação facial bem-sucedida, o sistema deve identificar gestos manuais (ex: mão aberta portão abre) utilizando técnicas de visão computacional.

---

## RF04 – Controle de portão (abrir/fechar)
O sistema deve ser capaz de abrir ou fechar o portão, utilizando motores (DC ou servo), com base no gesto detectado e no estado atual do portão.

---

## RF05 – Modo de emergência
O sistema deve permitir o bloqueio manual do portão por meio de um botão de emergência que interrompe a lógica automática de abertura/fechamento.

---

## RF06 – Feedback visual ao usuário
O sistema deve fornecer informações visuais ao usuário por meio de LEDs (verde/vermelho) e/ou display LCD, indicando os estados como:
- Acesso autorizado
- Acesso negado
- Portão aberto ou fechado
- Portão aberto 20%
- Portão aberto 40%
- Portão aberto 60%
- Portão aberto 80%
- Portão aberto 100%

---
