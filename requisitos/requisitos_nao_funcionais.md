# ⚙️ Requisitos Não-Funcionais – Projeto de Controle de Acesso com Reconhecimento Facial e Gestos

Este documento descreve os requisitos não-funcionais do sistema, relacionados a desempenho, usabilidade, qualidade e restrições técnicas.

---

## RNF01 – Baixa latência no reconhecimento facial
O tempo entre a captura da imagem e a resposta (autorizado/negado) deve ser inferior a 2 segundos, garantindo uma experiência fluida ao usuário.

---

## RNF02 – Robustez em condições de iluminação variável
O sistema deve operar corretamente em ambientes com diferentes níveis de iluminação, como durante o dia, à noite ou em áreas sombreadas.

---

## RNF03 – Resistência física a intempéries
Todos os componentes expostos (câmera, sensores, LEDs, motores) devem estar protegidos por uma estrutura que suporte uso externo (chuva, sol, poeira).

---

## RNF04 – Eficiência energética
O sistema deve manter consumo de energia baixo, com sensores e câmera ativando apenas quando necessário (detecção de presença).

---

## RNF05 – Arquitetura modular e escalável
O código do software deve ser organizado de forma modular para facilitar futuras expansões, como:
- Novos tipos de gestos

---
