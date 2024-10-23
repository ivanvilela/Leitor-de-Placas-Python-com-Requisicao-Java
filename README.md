# Leitor-de-Placas-Python-com-Requisicao-Java

Este projeto é um aplicativo Python que utiliza a biblioteca OpenCV e Tesseract OCR para detectar e ler placas de veículos a partir de imagens. Além disso, ele envia os dados da placa detectada para um serviço Java para registrar a entrada e a saída do veículo.

## Funcionalidades

- Detecção de placas de veículos em imagens.
- Leitura de texto da placa usando Tesseract OCR.
- Envio de dados da placa detectada para um serviço Java via requisições HTTP POST.

## Tecnologias Utilizadas

- Python
- OpenCV
- NumPy
- imutils
- pytesseract
- Requests

## Pré-requisitos

- Python 3.x
- OpenCV
- NumPy
- imutils
- pytesseract
- Tesseract OCR instalado no seu sistema
- Um serviço Java rodando localmente que aceite requisições para registro de entrada e saída de veículos.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/leitor-de-placas.git
   cd leitor-de-placas

2. Instale as dependências necessárias:
    ```bash
   pip install opencv-python numpy imutils pytesseract requests

3. Configure o caminho para o executável do Tesseract no código (de acordo com o caminho de instalação do tesseract na sua máquina):
    ```bash
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

4. Certifique-se de que o serviço Java esteja em execução e acessível em
   http://localhost:8080/api/v1/parking-records/entry e
   http://localhost:8080/api/v1/parking-records/exit.

5. Uso:
   Para detectar uma placa e enviar os dados, execute o arquivo Python principal:
    ```bash
    python .py

