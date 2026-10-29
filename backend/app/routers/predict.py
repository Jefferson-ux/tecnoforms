""" "
- Ruta de Predicción :
    Utiliza Método POST para enviar datos y recibir una respuesta ->
    Enviar una imagen y recibir la predicción y confianza...
"""

from fastapi import APIRouter, File, HTTPException, UploadFile

from .. import models
from ..preprocessing import a_base64, preprocesar
from ..schemas import Prediccion

router = APIRouter(tags=["predicción"])


@router.post("/predict", response_model=Prediccion)
def predict(archivo: UploadFile = File(...)):
    try:
        img28 = preprocesar(archivo.file.read())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    digito, probabilidades = models.predecir(img28)
    confianza = probabilidades[digito]

    return Prediccion(
        digito=digito,
        confianza=confianza,
        probabilidades=probabilidades,
        imagen_procesada=a_base64(img28),
    )
