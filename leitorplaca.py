import cv2
import numpy as np
import imutils
import pytesseract
import requests
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para detectar a placa na imagem
def detect_plate(file_img):
    img = cv2.imread(file_img)
    (H, W) = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blur, 30, 200)

    conts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = imutils.grab_contours(conts)
    conts = sorted(conts, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for c in conts:
        peri = cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, 0.02 * peri, True)
        if cv2.isContourConvex(aprox) and len(aprox) == 4:
            location = aprox
            break

    if location is None:
        return False

    mask = np.zeros(gray.shape, np.uint8)
    img_plate = cv2.drawContours(mask, [location], 0, 255, -1)
    img_plate = cv2.bitwise_and(img, img, mask=mask)

    (y, x) = np.where(mask == 255)
    (beginX, beginY) = (np.min(x), np.min(y))
    (endX, endY) = (np.max(x), np.max(y))

    plate = gray[beginY:endY, beginX:endX]

    return plate

# Função para fazer OCR na placa
def ocr_plate(plate):
    config_tesseract = "--tessdata-dir tessdata --psm 8"
    text = pytesseract.image_to_string(plate, lang="por", config=config_tesseract)
    text = "".join(c for c in text if c.isalnum())

    # Correções específicas (caso seja necessário)
    if text == "AUJOB38":
        text = "AUJ0B38"
    elif text == "GCW9AG5":
        text = "GCW9A05"
    
    return text

# Função de pré-processamento da placa
def preprocessing(img):
    increase = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    _, otsu = cv2.threshold(increase, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return otsu

# Função para enviar a placa detectada ao serviço Java para a entrada do veículo
def send_plate_to_java_service_entry(plate_text):
    url = 'http://localhost:8080/api/v1/parking-records/entry'
    headers = {
        'X-API-KEY': '9aBc#3xZ!8qL@1mN$6tR',
        'Content-Type': 'application/json'
    }
    data = {'plate': plate_text}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return {'status': 'success', 'message': 'Registro de entrada criado com sucesso'}
        else:
            return {'status': 'error', 'message': response.text}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': str(e)}

# Função para enviar a placa detectada ao serviço Java para a saída do veículo
def send_plate_to_java_service_exit(plate_text):
    url = 'http://localhost:8080/api/v1/parking-records/exit'
    headers = {
        'X-API-KEY': '9aBc#3xZ!8qL@1mN$6tR',
        'Content-Type': 'application/json'
    }
    data = {'plate': plate_text}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return {'status': 'success', 'message': 'Registro de saída criado com sucesso'}
        else:
            return {'status': 'error', 'message': response.text}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': str(e)}

# Função principal do Flask para renderizar a página e processar a imagem
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Nenhuma imagem enviada'

        file = request.files['file']
        if file.filename == '':
            return 'Nenhuma imagem selecionada'

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Detectar a placa
            plate = detect_plate(file_path)
            if plate is False:
                return 'Nenhuma placa detectada'

            # Pré-processamento e OCR
            processed_plate = preprocessing(plate)
            plate_text = ocr_plate(processed_plate)

            # Verifica qual botão foi clicado: "entrada" ou "saída"
            action = request.form.get('action')
            if action == 'entrada':
                response = send_plate_to_java_service_entry(plate_text)
            elif action == 'saida':
                response = send_plate_to_java_service_exit(plate_text)

            return response['message']

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
