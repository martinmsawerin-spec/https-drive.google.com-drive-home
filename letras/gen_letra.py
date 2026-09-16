import pymupdf as fitz
import sys, textwrap

W, H = 760, 368

def wrap_to_width(text, max_width, size, font="helv"):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fitz.get_text_length(trial, fontname=font, fontsize=size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def gen_letra(data, out_path):
    doc = fitz.open()
    page = doc.new_page(width=W, height=H)
    black = (0, 0, 0)

    def line(x0, y0, x1, y1, width=0.7):
        page.draw_line((x0, y0), (x1, y1), color=black, width=width)

    def rect(x0, y0, x1, y1, width=0.7):
        page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=black, width=width)

    def text(x, y, s, size=9, font="helv", bold=False, align=None, box_x1=None):
        f = "hebo" if bold else font
        if align == "center" and box_x1 is not None:
            tw = fitz.get_text_length(s, fontname=f, fontsize=size)
            x = x + ((box_x1 - x) - tw) / 2
        page.insert_text((x, y), s, fontsize=size, fontname=f, color=black)

    # Outer border
    rect(8, 8, W - 8, H - 8, width=1.1)

    # Title bar
    line(8, 38, W - 8, 38, width=1.1)
    text(8, 30, "LETRA DE CAMBIO", size=16, bold=True, align="center", box_x1=W - 8)

    # Left clauses column
    LX0, LX1 = 8, 155
    line(LX1, 38, LX1, H - 8, width=1.1)
    text(14, 50, "Cláusulas Especiales:", size=7.5, bold=True)
    clauses = [
        "1) En caso de mora esta Letra de Cambio generará las tasas de "
        "interés compensatorio y moratorio más altas que la Ley "
        "permita a su último Tenedor.",
        "2) El plazo de su vencimiento podrá ser prorrogado por el "
        "Tenedor, por el plazo que este señale sin que sea necesaria "
        "la intervención del obligado principal ni de los solidarios.",
        "3) Su importe debe ser pagado solo en la misma moneda que "
        "expresa este Título Valor.",
        "4) Esta Letra de Cambio no requiere ser protestada por falta de pago.",
    ]
    cy = 62
    for cl in clauses:
        for ln in wrap_to_width(cl, LX1 - LX0 - 10, 6.8):
            text(14, cy, ln, size=6.8)
            cy += 8.2
        cy += 3

    # ---- Header table (NUMERO / LUGAR DE GIRO / FECHA DE GIRO / FECHA DE VENCIMIENTO / MONEDA E IMPORTE)
    col_numero = (155, 225)
    col_lugar = (225, 315)
    col_fgiro = (315, 455)
    col_fgiro_sub = [(315, 361.7), (361.7, 408.3), (408.3, 455)]
    col_fvenc = (455, 595)
    col_fvenc_sub = [(455, 501.7), (501.7, 548.3), (548.3, 595)]
    col_moneda = (595, 752)

    top, subh, bot = 38, 58, 90
    line(8, top, W - 8, top, width=1.1)
    line(155, subh, 752, subh, width=0.6)
    line(155, bot, 752, bot, width=1.1)
    for x in [col_numero[0], col_lugar[0], col_fgiro[0], col_fvenc[0], col_moneda[0], 752]:
        line(x, top, x, bot, width=0.8)
    for x in [col_fgiro_sub[1][0], col_fgiro_sub[2][0], col_fvenc_sub[1][0], col_fvenc_sub[2][0]]:
        line(x, subh, x, bot, width=0.5)

    text(col_numero[0], 49, "NUMERO", size=7.5, bold=True, align="center", box_x1=col_numero[1])
    text(col_lugar[0], 49, "LUGAR DE GIRO", size=7.5, bold=True, align="center", box_x1=col_lugar[1])
    text(col_fgiro[0], 49, "FECHA DE GIRO", size=7.5, bold=True, align="center", box_x1=col_fgiro[1])
    text(col_fvenc[0], 49, "FECHA DE VENCIMIENTO", size=7, bold=True, align="center", box_x1=col_fvenc[1])
    text(col_moneda[0], 49, "MONEDA E IMPORTE", size=7.5, bold=True, align="center", box_x1=col_moneda[1])

    for (x0, x1), lbl in zip(col_fgiro_sub, ["DIA", "MES", "AÑO"]):
        text(x0, 57, lbl, size=6.5, bold=True, align="center", box_x1=x1)
    for (x0, x1), lbl in zip(col_fvenc_sub, ["DIA", "MES", "AÑO"]):
        text(x0, 57, lbl, size=6.5, bold=True, align="center", box_x1=x1)

    text(col_numero[0], 78, data["numero"], size=11, align="center", box_x1=col_numero[1])
    text(col_lugar[0], 78, data["lugar_giro"], size=10, align="center", box_x1=col_lugar[1])
    for (x0, x1), v in zip(col_fgiro_sub, [data["f_giro_dia"], data["f_giro_mes"], data["f_giro_anio"]]):
        text(x0, 78, v, size=9.5, align="center", box_x1=x1)
    for (x0, x1), v in zip(col_fvenc_sub, [data["f_venc_dia"], data["f_venc_mes"], data["f_venc_anio"]]):
        text(x0, 78, v, size=9.5, align="center", box_x1=x1)
    text(col_moneda[0], 79, data["moneda_importe"], size=12, bold=True, align="center", box_x1=col_moneda[1])

    # ---- "Por esta LETRA DE CAMBIO..." line
    y = 102
    text(163, y, "Por esta LETRA DE CAMBIO se servirá(n) pagar incondicionalmente a la", size=9)
    y += 11
    text(163, y, f"Orden de {data['beneficiario']} la cantidad de:", size=9)

    # amount box
    box_y0, box_y1 = 122, 142
    rect(163, box_y0, 752, box_y1, width=0.8)
    text(175, 135, data["monto_letras"], size=10.5)

    y = 154
    text(163, y, "En el siguiente lugar de pago o con cargo en la cuenta del Banco......................................",
         size=8.5)

    # ---- Girado / Domicilio / D.O.I. box + Banco mini-table
    gy0, gy1 = 162, 226
    gsplit = 470
    rect(163, gy0, 752, gy1, width=0.9)
    line(gsplit, gy0, gsplit, gy1, width=0.7)

    text(170, 176, "Girado:", size=8.5, bold=True)
    text(210, 176, data["girado"], size=9.5)
    text(170, 191, "Domicilio:", size=8.5, bold=True)
    dom_lines = wrap_to_width(data["domicilio"], gsplit - 220, 8)
    for i, ln in enumerate(dom_lines[:2]):
        text(220, 191 + i * 9.5, ln, size=8)
    doi_y = 191 + (min(len(dom_lines), 2)) * 9.5 + 8
    doi_y = max(doi_y, 208)
    text(170, doi_y, "D.O.I.", size=8.5, bold=True)
    text(196, doi_y, data["doi"], size=9)
    text(280, doi_y, "TELF. ......................", size=8)

    text(gsplit + 8, 172, "Importe a debitar en la siguiente cuenta del Banco que se indica", size=6.5, bold=True)
    bx = [gsplit, gsplit + 55, gsplit + 100, gsplit + 210, 752]
    line_y = 178
    line(gsplit, line_y, 752, line_y, width=0.5)
    for x in bx[1:-1]:
        line(x, line_y, x, gy1, width=0.5)
    for (x0, x1), lbl in zip(zip(bx, bx[1:]), ["BANCO", "OFICINA", "N° DE CUENTA", "D.C."]):
        text(x0, 186, lbl, size=6, bold=True, align="center", box_x1=x1)

    # ---- Girador row + firmas
    gr_y0 = gy1
    line(8, gr_y0, W - 8, gr_y0, width=1.1)
    text(163, gr_y0 + 14, "Nombre/Denominación o Razón Social del Girador:", size=8.5, bold=True)
    text(400, gr_y0 + 14, data["girador"], size=9.5)
    text(600, gr_y0 + 14, "D.O.I.", size=8.5, bold=True)
    text(624, gr_y0 + 14, data["girador_doi"], size=9)

    firma_y = gr_y0 + 60
    line(200, firma_y, 340, firma_y, width=0.7)
    text(200, firma_y + 10, "FIRMA", size=8, bold=True, align="center", box_x1=340)
    line(500, firma_y, 640, firma_y, width=0.7)
    text(500, firma_y + 10, "FIRMA", size=8, bold=True, align="center", box_x1=640)

    text(163, firma_y + 34, "Nombre del Representante(s): ......................................................................", size=8)

    # Footer
    line(8, H - 20, W - 8, H - 20, width=1.1)
    text(14, H - 10, "No escribir ni firmar debajo de esta línea", size=8, bold=True)

    doc.save(out_path, garbage=4, deflate=True)
    return out_path


if __name__ == "__main__":
    data = dict(
        numero="526",
        lugar_giro="LIMA",
        f_giro_dia="01", f_giro_mes="01", f_giro_anio="2026",
        f_venc_dia="01", f_venc_mes="01", f_venc_anio="2026",
        moneda_importe="$ 0.00",
        monto_letras="Cero con 00/100 Dólares Americanos",
        beneficiario="SAWERIN S.A.C",
        girado="EJEMPLO S.A.C.",
        domicilio="DIRECCION DE EJEMPLO",
        doi="00000000000",
        girador="SAWERIN S.A.C",
        girador_doi="20608495470",
    )
    out = sys.argv[1] if len(sys.argv) > 1 else "letra_ejemplo.pdf"
    gen_letra(data, out)
    print("saved", out)
