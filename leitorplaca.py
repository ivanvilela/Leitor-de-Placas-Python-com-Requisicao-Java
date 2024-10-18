import cv2
import numpy as np
import imutils
import pytesseract
import requests

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
        if cv2.isContourConvex(aprox):
            if len(aprox) == 4:
                location = aprox
                break

    beginX = beginY = endX = endY = None
    if location is None:
        plate = False
    else:
        mask = np.zeros(gray.shape, np.uint8)
        img_plate = cv2.drawContours(mask, [location], 0, 255, -1)
        img_plate = cv2.bitwise_and(img, img, mask=mask)

        (y, x) = np.where(mask == 255)
        (beginX, beginY) = (np.min(x), np.min(y))
        (endX, endY) = (np.max(x), np.max(y))

        plate = gray[beginY:endY, beginX:endX]

    return plate

def ocr_plate(plate):
    config_tesseract = "--tessdata-dir tessdata --psm 8"
    text = pytesseract.image_to_string(plate, lang="por", config=config_tesseract)
    text = "".join(c for c in text if c.isalnum())
    return text

def preprocessing(img):
    increase = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    _, otsu = cv2.threshold(increase, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return otsu

# Função para enviar a placa detectada ao serviço Java para a entrada do veículo
def send_plate_to_java_service_entry(plate_text):
    url = 'http://localhost:8080/api/v1/parking-records/entry'  # Endpoint para entrada do veículo
    headers = {
        'X-API-KEY': '9aBc#3xZ!8qL@1mN$6tR',
        'Content-Type': 'application/json'
    }
    data = {
        'plate': plate_text  # Formato esperado pelo PlateDTO
    }

    try:
        # Enviar a requisição POST com os dados da placa e o cabeçalho de API Key
        response = requests.post(url, headers=headers, json=data)

        # Verificar o status da resposta
        if response.status_code == 201:
            print('Registro de entrada criado com sucesso')
            return {'status': 'success', 'message': 'Registro de entrada criado com sucesso'}
        elif response.status_code == 404:
            print('Carro não cadastrado')
            return {'status': 'error', 'message': 'Carro não cadastrado'}
        elif response.status_code == 403:
            print('Acesso não autorizado')
            return {'status': 'error', 'message': 'Acesso não autorizado'}
        else:
            print(f'Erro no servidor: {response.status_code}')
            return {'status': 'error', 'message': 'Erro no servidor', 'status_code': response.status_code}
    
    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar ao servidor: {str(e)}')
        return {'status': 'error', 'message': f'Erro ao conectar ao servidor: {str(e)}'}

# Função para enviar a placa detectada ao serviço Java para a saída do veículo
def send_plate_to_java_service_exit(plate_text):
    url = 'http://localhost:8080/api/v1/parking-records/exit'  # Endpoint para saída do veículo
    headers = {
        'X-API-KEY': '9aBc#3xZ!8qL@1mN$6tR',
        'Content-Type': 'application/json'
    }
    data = {
        'plate': plate_text  # Formato esperado pelo PlateDTO
    }

    try:
        # Enviar a requisição POST com os dados da placa e o cabeçalho de API Key
        response = requests.post(url, headers=headers, json=data)

        # Verificar o status da resposta
        if response.status_code == 201:
            print('Registro de saída criado com sucesso')
            return {'status': 'success', 'message': 'Registro de saída criado com sucesso'}
        elif response.status_code == 404:
            print('Carro não cadastrado')
            return {'status': 'error', 'message': 'Carro não cadastrado'}
        elif response.status_code == 403:
            print('Acesso não autorizado')
            return {'status': 'error', 'message': 'Acesso não autorizado'}
        else:
            print(f'Erro no servidor: {response.status_code}')
            return {'status': 'error', 'message': 'Erro no servidor', 'status_code': response.status_code}
    
    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar ao servidor: {str(e)}')
        return {'status': 'error', 'message': f'Erro ao conectar ao servidor: {str(e)}'}

if __name__ == '__main__':
    input_image_path = 'static/images/img_carro02.jpg'

    # Detectar a placa na imagem
    plate = detect_plate(input_image_path)
    
    if plate is not False:
        processed_plate = preprocessing(plate)
        plate_text = ocr_plate(processed_plate)
        
        # Simulação de envio da placa para a entrada e saída do veículo
        print("Enviando placa para o serviço de entrada...")
        response_entry = send_plate_to_java_service_entry(plate_text)
        print(f'Resposta do serviço Java (Entrada): {response_entry}')
        
        print("Enviando placa para o serviço de saída...")
        response_exit = send_plate_to_java_service_exit(plate_text)
        print(f'Resposta do serviço Java (Saída): {response_exit}')
    else:
        print('Nenhuma placa detectada')
