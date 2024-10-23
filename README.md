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
    ```

3. Instalação do Tesseract OCR:
   - Baixe e instale o Tesseract OCR a partir do seguinte link: [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
   - Certifique-se de instalar todas as linguagens disponíveis para evitar erros durante o reconhecimento de texto.

4. Configure o caminho para o executável do Tesseract no código (de acordo com o caminho de instalação do tesseract na sua máquina):
    ```bash
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ```

5. Certifique-se de que o serviço Java esteja em execução e acessível em
   
    ` http://localhost:8080/api/v1/parking-records/entry ` e
    ` http://localhost:8080/api/v1/parking-records/exit. `

6. Uso:
   - Para detectar uma placa e enviar os dados, execute o arquivo Python principal:
   
    ```bash
    python leitorplaca.py
     ```

     **Caso ocorrer este erro: "error: pytesseract.pytesseract.TesseractError: (1, 'Error opening data file tessdata/eng.traineddata Please make sure the TESSDATA_PREFIX environment variable is set to your "tessdata" directory. Failed loading language \'eng\' Tesseract couldn\'t load any languages! Could not initialize tesseract.')"**
   - Abra o terminal no Visual Studio Code e execute os seguintes comandos:
     ```bash
     mkdir tessdata
     wget -O ./tessdata/por.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata?raw=true
     wget -O ./tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata?raw=true
     ```
   - Certifique-se de que a pasta `tessdata` no diretório do projeto contém os arquivos `por.traineddata` e `eng.traineddata`.
   - Se o erro persistir adicione PREFIX_DATA como variável ambiente de sistema:
     1. Pressione a tecla Windows e busque por "Editar variáveis ambiente de sistema".
     2. Clique em "Variáveis de Ambiente" no canto inferior direito.
     3. No painel "Variáveis do Sistema", clique em "Novo".
     4. Defina o nome da variável como `TESSDATA_PREFIX`.
     5. Clicar em "Novo"
     6. Nome da variável: TESSDATA_PREFIX
     7. Defina o valor da variável como o caminho onde o Tesseract está instalado, por exemplo: `C:\Program Files\Tesseract-OCR`.
    
   - Certifique-se de reiniciar o terminal ou o ambiente de desenvolvimento após adicionar a variável de ambiente para que as mudanças tenham efeito.

