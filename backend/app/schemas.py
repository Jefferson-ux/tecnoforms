from pydantic import BaseModel, Field


class Prediccion(BaseModel):
    id: int | None = None  # id en la base de datos (None si no hay Supabase)
    digito: int
    confianza: float
    probabilidades: list[float]
    imagen_procesada: str  # PNG 28x28 en base64: lo que "ve" el modelo


class Correccion(BaseModel):
    etiqueta_real: int = Field(ge=0, le=9)
