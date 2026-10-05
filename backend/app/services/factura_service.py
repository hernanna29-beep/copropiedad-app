from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generar_factura_pdf(pago) -> BytesIO:
    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloFactura",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=8,
    )

    subtitulo = ParagraphStyle(
        "SubtituloFactura",
        parent=estilos["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=20,
    )

    contenido = []

    contenido.append(
        Paragraph(
            "COPROPIEDAD APP",
            titulo,
        )
    )

    contenido.append(
        Paragraph(
            "FACTURA / CUENTA DE COBRO",
            subtitulo,
        )
    )

    datos_factura = [
        ["Número de factura", f"FAC-{pago.id:06d}"],
        ["Concepto", pago.concepto],
        ["Periodo", pago.periodo],
        ["Valor", f"${pago.valor:,.0f}".replace(",", ".")],
        ["Estado", pago.estado],
    ]

    if pago.fecha_vencimiento:
        datos_factura.append(
            [
                "Fecha de vencimiento",
                str(pago.fecha_vencimiento),
            ]
        )

    tabla = Table(
        datos_factura,
        colWidths=[55 * mm, 95 * mm],
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.black,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (1, 0),
                    (1, -1),
                    "Helvetica",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    contenido.append(tabla)

    contenido.append(Spacer(1, 20))

    contenido.append(
        Paragraph(
            "Documento generado por COPROPIEDAD APP.",
            estilos["Normal"],
        )
    )

    documento.build(contenido)

    buffer.seek(0)

    return buffer