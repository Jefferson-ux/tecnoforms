import { predecir } from "../../lib/api";

export async function solicitarPrediccion(imagen: Blob): Promise<void> {
  try {
    const resultado = await predecir(imagen);
    window.dispatchEvent(new CustomEvent("resultado", { detail: resultado }));
  } catch (error) {
    window.dispatchEvent(new CustomEvent("error-prediccion", { detail: (error as Error).message }));
  }
}