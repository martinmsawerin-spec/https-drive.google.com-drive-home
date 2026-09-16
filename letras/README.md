# Generador de Letras de Cambio — SAWERIN S.A.C.

Genera letras de cambio a partir de la plantilla real "LETRA limpia.psd"
del usuario, para la carpeta de Drive **LETRAS PERU**:
https://drive.google.com/drive/folders/1KdyUBkId535nPnkfJrVAZG4nneVNiLbB

## Datos fijos (girador)

- Razón social: SAWERIN S.A.C
- RUC: 20608495470
- Lugar de giro: LIMA

## Numeración

El número de letra es correlativo.

- 524 — CORPORACION BLESS SAC (2026-08-12/13)
- 525 — SOPORTE TECNICO, TECNOLOGIA Y SERVICIOS E.I.R.L. (2026-09-16)

La próxima letra debe usar el número **526**.

## Flujo de entrega (acordado 2026-08-13)

Hay dos generadores porque la subida automática a Drive vía la
herramienta de este entorno **no es confiable con imágenes JPEG que
tienen tramos largos de color plano** (p. ej. el fondo blanco de un
escaneo) — el mecanismo de transcripción falla en reproducir series muy
largas del mismo carácter repetido, y Drive rechaza el archivo como
"base64 inválido". Por eso:

1. **`gen_letra_psd.py`** — réplica visual exacta de la plantilla real
   (fondo escaneado + texto superpuesto en las posiciones reales de la
   plantilla). Se **entrega directamente al usuario por chat**
   (`SendUserFile`), nunca por subida automática a Drive. El usuario la
   arrastra a la carpeta si la quiere ahí. **Este es el formato que usa
   el usuario habitualmente.**
2. **`gen_letra.py`** — recreación 100% vectorial (sin imágenes
   incrustadas, ~15-20 KB), visualmente muy fiel pero no idéntica
   pixel a pixel. Al no tener tramos de bytes repetidos, se sube sin
   problema a Drive automáticamente y puede usarse como respaldo ahí
   si el usuario lo pide.

## Nota sobre persistencia del entorno

El contenedor de esta sesión puede reiniciarse (p. ej. tras inactividad)
y perder todo lo que no esté commiteado y **pusheado** al repo. Si
`git push` es bloqueado por el clasificador de auto-mode, avisar al
usuario — sin push, este directorio `letras/` desaparece en el próximo
reinicio y hay que reconstruirlo (fondo del PSD + scripts) desde cero
en la siguiente sesión. El PSD original vive en Drive como
"LETRA limpia.psd" (carpeta LETRAS PERU) por si hay que re-extraer
`plantilla_fondo.png`.

## Uso — `gen_letra_psd.py` (formato real, para entrega por chat)

```python
from gen_letra_psd import gen_letra_psd
data = dict(
    numero="526", f_giro_dia="DD", f_giro_mes="MM", f_giro_anio="AAAA",
    f_venc_dia="DD", f_venc_mes="MM", f_venc_anio="AAAA",
    moneda_importe="$ 0.00", monto_letras="... con 00/100 Dólares Americanos",
    girado="...", domicilio="...", doi="...",
)
gen_letra_psd("plantilla_fondo.png", data, "526 NOMBRE.pdf")
```

`plantilla_fondo.png` es el fondo limpio ya extraído del PSD real (capa
"Capa 1", sin texto). Requiere `Pillow`.

## Uso — `gen_letra.py` (vectorial, para subida automática a Drive)

`gen_letra(data, out_path)`. `data` requiere:

- `numero`, `lugar_giro`
- `f_giro_dia/mes/anio`, `f_venc_dia/mes/anio`
- `moneda_importe` (ej. "$ 156.00")
- `monto_letras` (monto en palabras)
- `beneficiario` (normalmente "SAWERIN S.A.C")
- `girado`, `domicilio`, `doi` (datos del deudor/cliente)
- `girador`, `girador_doi` (fijos: "SAWERIN S.A.C" / "20608495470")

Requiere `pymupdf`.
