# Archivo de reportes en PDF con mejoras corregidas

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime

def truncate(text, max_len=30):
    """Trunca texto demasiado largo para evitar que se desborde."""
    text = str(text)
    return text if len(text) <= max_len else text[:max_len] + "..."

def generate_pdf(data, filename="reporte.pdf"):
    """
    Genera un PDF en formato tabla usando datos JSON con:
    - Ajuste dinámico de ancho de columnas
    - Encabezados más legibles
    - Alineación por tipo de dato
    - Truncado de campos largos
    """
    # Documento en horizontal para más espacio
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    # Título
    title = Paragraph("Reporte de Usuarios", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Si data es un dict, convertirlo en lista
    if isinstance(data, dict):
        data = [data]

    if not data:
        elements.append(Paragraph("No hay datos disponibles", styles["Normal"]))
        doc.build(elements)
        return filename

    # Detectar todas las columnas
    all_columns = set()
    for row in data:
        all_columns.update(row.keys())

    # Orden deseado de columnas
    headers = [
        "id",
        "role_id",
        "name",
        "email",
        "email_verified_at",
        "updated_at",
        "remember_token",
        "created_at",
    ]
    headers = [col for col in headers if col in all_columns]  # usar solo las que existan
    extra_cols = [col for col in all_columns if col not in headers]
    headers.extend(extra_cols)

    # Encabezados legibles
    display_headers = [h.replace("_", " ").title() for h in headers]

    # Construir tabla de datos
    table_data = [display_headers]
    for row in data:
        fila = []
        for h in headers:
            valor = row.get(h, "")
            if h in ("id", "role_id"):  # mostrar números como texto plano (sin Paragraph)
                fila.append(str(valor))
            else:  # para texto largo, truncar y usar Paragraph
                fila.append(Paragraph(truncate(valor), styles["Normal"]))
        table_data.append(fila)

    # Calcular anchos dinámicos
    page_width = landscape(A4)[0] - 80  # espacio útil (restamos márgenes)
    max_lengths = [max(len(str(row.get(h, ""))) for row in data) for h in headers]
    max_lengths = [max(l, len(h)) for l, h in zip(max_lengths, display_headers)]
    total_length = sum(max_lengths)
    col_widths = [(page_width * (ml / total_length)) for ml in max_lengths]

    # Crear tabla
    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Estilos de la tabla
    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Alineación vertical al centro
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]

    # Alineación personalizada: números → derecha, texto → izquierda
    for col_idx, col_name in enumerate(headers):
        if col_name in ("id", "role_id"):
            style_commands.append(("ALIGN", (col_idx, 1), (col_idx, -1), "RIGHT"))
        else:
            style_commands.append(("ALIGN", (col_idx, 1), (col_idx, -1), "LEFT"))

    table.setStyle(TableStyle(style_commands))
    elements.append(table)

    # Footer con fecha
    elements.append(Spacer(1, 12))
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generado el {fecha}", styles["Normal"]))

    doc.build(elements)
    return filename