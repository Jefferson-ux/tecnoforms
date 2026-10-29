import base64

import cv2
import numpy as np


def preprocesar(contenido: bytes) -> np.ndarray:
    """Bytes de una imagen -> matriz 28x28 uint8 (dígito blanco sobre fondo negro)."""
    img = cv2.imdecode(np.frombuffer(contenido, np.uint8), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("No se pudo leer la imagen")

    if img.ndim == 3 and img.shape[2] == 4:  # PNG con transparencia (canvas)
        alfa = img[:, :, 3:4].astype(np.float32) / 255.0
        img = (img[:, :, :3] * alfa + 255 * (1 - alfa)).astype(np.uint8)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Fondo claro u oscuro: se mira en las 4 esquinas (casi siempre son fondo)
    alto, ancho = img.shape
    t = max(5, min(alto, ancho) // 10)
    esquinas = np.concatenate(
        [
            img[:t, :t].ravel(),
            img[:t, -t:].ravel(),
            img[-t:, :t].ravel(),
            img[-t:, -t:].ravel(),
        ]
    )
    if esquinas.mean() > 127:
        img = cv2.bitwise_not(img)  # MNIST: dígito claro sobre fondo oscuro

    # Binarización automática (Otsu) y recorte al dígito
    _, binaria = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        raise ValueError("No se detectó ningún dígito en la imagen")
    mayor = max(contornos, key=cv2.contourArea)
    if cv2.contourArea(mayor) < 0.001 * alto * ancho:
        raise ValueError("No se detectó ningún dígito en la imagen")
    x, y, w, h = cv2.boundingRect(mayor)

    # Cuadrar con margen ANTES de redimensionar, para no deformar el dígito
    lado = max(w, h)
    tam = lado + 2 * int(lado * 0.25)
    lienzo = np.zeros((tam, tam), np.uint8)
    y0, x0 = (tam - h) // 2, (tam - w) // 2
    lienzo[y0 : y0 + h, x0 : x0 + w] = binaria[y : y + h, x : x + w]
    return cv2.resize(lienzo, (28, 28), interpolation=cv2.INTER_AREA)


def a_base64(img28: np.ndarray) -> str:
    _, buf = cv2.imencode(".png", img28)
    return "data:image/png;base64," + base64.b64encode(buf.tobytes()).decode()
