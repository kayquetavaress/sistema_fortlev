import easyocr
import cv2

reader = easyocr.Reader(['pt'])

def ler_imagem(caminho):

    # carregar imagem
    imagem = cv2.imread(caminho)

    # 🔥 transformar em escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # 🔥 aumentar contraste (muito importante)
    cinza = cv2.convertScaleAbs(cinza, alpha=2, beta=0)

    # 🔥 reduzir ruído
    cinza = cv2.GaussianBlur(cinza, (3, 3), 0)

    # OCR
    resultado = reader.readtext(cinza)

    textos = []

    for item in resultado:
        textos.append(item[1])

    return "\n".join(textos)
