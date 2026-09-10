#!/usr/bin/env python3
"""Logo de packsmx para Linktree, en la paleta que ya usa el sitio.

Linktree recorta la imagen a un circulo y la muestra chica (~96 px), asi
que el dibujo va a sangre: el color llena el cuadrado entero y cualquier
recorte circular cae dentro de zona solida, sin borde raro.

La T es la misma del favicon (img/marca/icon.svg), redibujada con las
mismas proporciones para que la marca no cambie entre la pestana del
navegador y Linktree.

Se dibuja a 4x y se reduce con LANCZOS: ImageDraw no antialiasa, y a
96 px un borde escalonado se nota.
"""
from PIL import Image, ImageDraw

ORO = (230, 184, 67)
ORO2 = (201, 148, 42)
TINTA = (10, 9, 8)
TINTA_T = (21, 16, 5)   # el mismo #151005 del favicon

LADO = 1024
ESCALA = 4
G = LADO * ESCALA


def te(d, cx, cy, alto, color):
    """La T del favicon: barra ancha arriba, tronco centrado.

    Proporciones del original en viewBox 64: barra de 34 de ancho por 9 de
    alto, tronco de 10.4 por 25. Todo relativo al alto que se pida.
    """
    u = alto / 34.0            # el original mide 34 de alto (y=19 a y=53)
    barra_w, barra_h = 34 * u, 9 * u
    tronco_w = 10.4 * u
    x0, y0 = cx - barra_w / 2, cy - alto / 2
    d.polygon([
        (x0, y0), (x0 + barra_w, y0),
        (x0 + barra_w, y0 + barra_h),
        (cx + tronco_w / 2, y0 + barra_h),
        (cx + tronco_w / 2, y0 + alto),
        (cx - tronco_w / 2, y0 + alto),
        (cx - tronco_w / 2, y0 + barra_h),
        (x0, y0 + barra_h),
    ], fill=color)


def lienzo(fondo):
    img = Image.new("RGB", (G, G), fondo)
    return img, ImageDraw.Draw(img)


def guardar(img, nombre):
    img.resize((LADO, LADO), Image.LANCZOS).save(nombre, "PNG", optimize=True)
    print(f"  {nombre}")


# --- A: disco dorado, T oscura. Es el favicon actual, nacido circular. ---
img, d = lienzo(ORO)
te(d, G / 2, G / 2, G * 0.42, TINTA_T)
guardar(img, "logo-a-oro.png")

# --- B: fondo tinta, T dorada, anillo fino. El oro pesa mas sobre oscuro,
#        y el disco oscuro se sostiene en cualquier tema de Linktree. ---
img, d = lienzo(TINTA)
m = G * 0.055                                  # el anillo va bien adentro
d.ellipse([m, m, G - m, G - m], outline=ORO, width=int(G * 0.018))
te(d, G / 2, G / 2, G * 0.40, ORO)
guardar(img, "logo-b-tinta-anillo.png")

# --- C: fondo tinta, T dorada grande, sin anillo. La mas legible a 96 px. ---
img, d = lienzo(TINTA)
te(d, G / 2, G / 2, G * 0.46, ORO)
guardar(img, "logo-c-tinta-simple.png")

# --- Vista previa: como se ven recortados en circulo y en chico ---
prev = Image.new("RGB", (LADO, 360), (244, 241, 234))
for i, n in enumerate(["logo-a-oro.png", "logo-b-tinta-anillo.png", "logo-c-tinta-simple.png"]):
    o = Image.open(n)
    for j, tam in enumerate((256, 96)):
        c = o.resize((tam, tam), Image.LANCZOS)
        mask = Image.new("L", (tam * 4, tam * 4), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, tam * 4, tam * 4], fill=255)
        c.putalpha(mask.resize((tam, tam), Image.LANCZOS))
        x = 60 + i * 310 + (0 if j == 0 else 80)
        y = 30 if j == 0 else 300 - 96 + 30
        prev.paste(c, (x, y - (0 if j == 0 else 0)), c)
prev.save("logo-preview.png", "PNG")
print("  logo-preview.png")
