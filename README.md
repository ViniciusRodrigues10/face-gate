# Controle de Acesso com Reconhecimento Facial e Gestos

Este projeto é um sistema inteligente de **controle de acesso** que combina **reconhecimento facial** e **detecção de gestos manuais** para permitir ou negar a abertura de um portão. O sistema foi desenvolvido como parte da disciplina **Técnicas de Prototipagem** no Instituto Federal da Paraíba - IFPB.

## 👨‍🏫 Orientador
**Moacy Pereira da Silva**

## 👨‍💻 Desenvolvedores

- Álisson Brener da Silva – [alisson.brener@academico.ifpb.edu.br](mailto:alisson.brener@academico.ifpb.edu.br)  
- Caio Lívio Leite Muniz Dantas – [dantas.caio@academico.ifpb.edu.br](mailto:dantas.caio@academico.ifpb.edu.br)  
- Vinícius Gonzaga Cavalcante Rodrigues – [vinicius.gonzaga@academico.ifpb.edu.br](mailto:vinicius.gonzaga@academico.ifpb.edu.br)

## 📌 Descrição do Projeto

Este projeto propõe uma solução moderna e sem contato para controlar o acesso de veículos a ambientes restritos. A autenticação é feita através da identificação do **rosto do usuário** e confirmação por **gesto intencional**, aumentando a **segurança**, **conveniência** e **higiene** no processo de entrada/saída.

---

## ⚙️ Como Funciona

1. **Detecção de Presença**  
   Um sensor PIR ou uma câmera com detecção de movimento ativa o sistema ao detectar alguém próximo.

2. **Reconhecimento Facial**  
   Utiliza uma câmera HD e bibliotecas como OpenCV + Dlib para identificar se o rosto pertence a um usuário autorizado.

3. **Detecção de Gestos**  
   Após o reconhecimento facial, o sistema espera um gesto (ex: movimento horizontal da mão) para executar a ação de abrir ou fechar o portão.

4. **Controle do Portão**  
   O portão é acionado por motor DC (com driver L298N) ou servo motor, controlado via Arduino.

5. **Feedback e Segurança**  
   LEDs, displays e notificações informam sobre o status do acesso. Falhas podem ser registradas e um botão de emergência pode travar o sistema.

---

## 🎯 Aplicações e Benefícios

- **Alta segurança:** Acesso somente para rostos autorizados + gesto intencional.
- **Sistema sem contato:** Mais higiênico e conveniente.
- **Personalizável:** Possibilidade de configurar gestos para diferentes perfis.
- **Integração fácil:** Pode ser adaptado a sistemas de automação residencial.

---

## 🧪 Casos de Uso

### ✅ Acesso Autorizado
1. Usuário se aproxima →  
2. Sistema ativa a câmera →  
3. Reconhecimento facial →  
4. Gesto detectado →  
5. Portão abre ou fecha

### ❌ Acesso Negado
1. Pessoa não cadastrada →  
2. Reconhecimento falha →  
3. LED vermelho acende →  
4. Portão permanece fechado

---

## ✅ Requisitos

### Funcionais
- Captura de imagem em tempo real
- Autenticação facial com banco de dados
- Detecção de gestos manuais
- Controle de motor para abertura/fechamento
- Feedback visual do status
- Modo de emergência

### Não-Funcionais
- Baixa latência (< 2s)
- Operação em diferentes condições de luz
- Resistência a intempéries
- Baixo consumo de energia
- Código modular e escalável

---

## 🔧 Materiais Utilizados

| Item | Quantidade | Finalidade |
|------|------------|------------|
| Arduino + processador externo | 1 | Controle principal |
| Câmera USB HD | 1 | Captura facial |
| Sensor PIR | 1 | Detecção de presença |
| Motor DC com redutor / Servo | 1 | Movimento do portão |
| Driver L298N | 1 | Controle do motor |
| LEDs (verde/vermelho) | 1 de cada | Indicação de acesso |
| Display LCD 16x2 (opcional I2C) | 1 | Feedback textual |
| Sensores de fim de curso | 2 | Posição do portão |
| Botão de emergência | 1 | Trava de segurança |
| Protoboard e jumpers | - | Prototipagem |
| Fonte 5V/12V | 1 | Alimentação |

---

## 🛠️ Ferramentas e Softwares

- **OpenCV + Dlib / Face Recognition** – Reconhecimento facial  
- **MediaPipe / OpenCV (Hands)** – Detecção de gestos  
- **Python** – Linguagem principal  
- **VSCode / Jupyter** – Ambiente de desenvolvimento  
- **Multímetro / Ferro de solda** – Testes e montagem  
- **Internet (Wi-Fi/Ethernet)** – Para notificações (opcional)

---

## 📐 Diagramas

- Diagrama de blocos do sistema  
- Diagrama elétrico do protótipo  
*(ver arquivos incluídos no repositório)*

---

## 📍 Local

**Campina Grande - PB, 2025**  
Projeto acadêmico desenvolvido no Instituto Federal da Paraíba (IFPB).

---

## 📄 Licença

Este projeto é de uso educacional e está sob a licença MIT. Sinta-se à vontade para estudar, adaptar e reutilizar, com os devidos créditos aos autores.

---

