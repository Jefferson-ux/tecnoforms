export function crearLienzo(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext("2d")!;
  let dibujando = false;

  function limpiar() {
    ctx.fillStyle = "#fff"; // fondo BLANCO opaco: el backend espera tinta sobre papel
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "#000";
    ctx.lineWidth = 18;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
  }

  function posicion(e: PointerEvent) {
    const r = canvas.getBoundingClientRect();
    return {
      x: (e.clientX - r.left) * (canvas.width / r.width),
      y: (e.clientY - r.top) * (canvas.height / r.height),
    };
  }

  canvas.addEventListener("pointerdown", (e) => {
    dibujando = true;
    canvas.setPointerCapture(e.pointerId);
    const p = posicion(e);
    ctx.beginPath();
    ctx.moveTo(p.x, p.y);
    ctx.lineTo(p.x, p.y); // un punto, por si solo hace clic
    ctx.stroke();
  });

  canvas.addEventListener("pointermove", (e) => {
    if (!dibujando) return;
    const p = posicion(e);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
  });

  const terminar = () => (dibujando = false);
  canvas.addEventListener("pointerup", terminar);
  canvas.addEventListener("pointercancel", terminar);

  limpiar();

  return {
    limpiar,
    aBlob: () => new Promise<Blob | null>((listo) => canvas.toBlob(listo, "image/png")),
  };
}