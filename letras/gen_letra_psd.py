import sys
from PIL import Image, ImageDraw, ImageFont

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# field bboxes extracted from the real PSD text layers (px, at native 3125x2206)
FIELDS = {
    "numero": (872, 459, 942, 492, BOLD),
    "f_giro_dia": (1451, 484, 1494, 517, BOLD),
    "f_giro_mes": (1580, 484, 1626, 517, BOLD),
    "f_giro_anio": (1701, 486, 1797, 519, BOLD),
    "f_venc_dia": (1857, 484, 1900, 517, BOLD),
    "f_venc_mes": (2016, 484, 2062, 517, BOLD),
    "f_venc_anio": (2167, 484, 2263, 517, BOLD),
    "moneda_importe": (2458, 452, 2651, 491, BOLD),
    "girado": (989, 1079, 1631, 1114, BOLD),
    "doi": (944, 1294, 1187, 1324, REG),
}
MONTO_BOX = (1102, 793, 2490, 836)          # cantidad en letras
DOMICILIO_BOX = (1031, 1186, 1758, 1290)    # domicilio (wraps, bounded before the Banco mini-table)


def fit_size(draw, text, font_path, max_width, max_height):
    size = int(max_height)
    while size > 6:
        f = ImageFont.truetype(font_path, size)
        w = draw.textlength(text, font=f)
        if w <= max_width:
            return f
        size -= 1
    return ImageFont.truetype(font_path, 6)


def wrap_lines(draw, text, font_path, size, max_width):
    f = ImageFont.truetype(font_path, size)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return f, lines


def gen_letra_psd(bg_path, data, out_path, jpeg_quality=70, resize_width=None, resolution=200.0):
    base = Image.open(bg_path).convert("RGB")
    draw = ImageDraw.Draw(base)

    for key, (x0, y0, x1, y1, font_path) in FIELDS.items():
        text = str(data[key])
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        f = fit_size(draw, text, font_path, x1 - x0, (y1 - y0) * 1.15)
        draw.text((cx, cy), text, font=f, fill=(0, 0, 0), anchor="mm")

    # cantidad en letras (single line, sized to fit the box)
    mx0, my0, mx1, my1 = MONTO_BOX
    f = fit_size(draw, data["monto_letras"], REG, (mx1 - mx0), (my1 - my0) * 1.05)
    draw.text(((mx0 + mx1) / 2, (my0 + my1) / 2), data["monto_letras"], font=f, fill=(0, 0, 0), anchor="mm")

    # domicilio (wraps, auto-shrinks to fit in 2 lines)
    dx0, dy0, dx1, dy1 = DOMICILIO_BOX
    size = 30
    while size > 14:
        f, lines = wrap_lines(draw, data["domicilio"], REG, size, dx1 - dx0)
        if len(lines) <= 2:
            break
        size -= 1
    line_h = int(size * 1.25)
    y = dy0
    for ln in lines:
        draw.text((dx0, y), ln, font=f, fill=(0, 0, 0), anchor="la")
        y += line_h

    if resize_width and base.width > resize_width:
        ratio = resize_width / base.width
        base = base.resize((resize_width, int(base.height * ratio)), Image.LANCZOS)

    base = base.convert("L")
    base.save(out_path, "PDF", resolution=resolution, quality=jpeg_quality)
    return out_path
