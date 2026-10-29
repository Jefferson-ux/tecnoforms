import numpy as np

from .config import MODELOS_DIR

RUTA_CNN = MODELOS_DIR / "cnn_digitos.h5"
_cnn = None


def cargar_modelo() -> None:
    """Se llama UNA vez al arrancar el servidor (no en cada petición)."""
    global _cnn
    from tensorflow.keras.models import load_model

    if not RUTA_CNN.exists():
        raise FileNotFoundError(f"Falta el modelo: {RUTA_CNN}")
    _cnn = load_model(str(RUTA_CNN))


def cargado() -> bool:
    return _cnn is not None


def predecir(img28: np.ndarray) -> tuple[int, list[float]]:
    """Matriz 28x28 uint8 -> (dígito, lista de 10 probabilidades)."""
    x = img28.astype("float32").reshape(1, 28, 28, 1) / 255.0
    probs = _cnn.predict(x, verbose=0)[0]
    return int(np.argmax(probs)), [float(p) for p in probs]
