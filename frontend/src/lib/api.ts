const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export interface Prediccion {
  id: number | null;
  digito: number;
  confianza: number;
  probabilidades: number[];
  imagen_procesada: string;
}

export async function predecir(imagen: Blob): Promise<Prediccion> {
  const form = new FormData();
  form.append("archivo", imagen, "digito.png");

  let res: Response;
  try {
    res = await fetch(`${API_URL}/predict`, { method: "POST", body: form });
  } catch {
    throw new Error("No se pudo conectar con la API. ¿Está corriendo uvicorn?");
  }

  if (!res.ok) {
    const cuerpo = await res.json().catch(() => null);
    throw new Error(typeof cuerpo?.detail === "string" ? cuerpo.detail : `Error ${res.status}`);
  }
  return res.json();
}