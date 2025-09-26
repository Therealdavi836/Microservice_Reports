# Archivo de reportes en PDF

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime

def generate_pdf(data, filename="reporte.pdf"):
    """
    Genera un PDF en formato tabla usando datos JSON con ajuste dinámico.
    """
    # Usamos formato horizontal para más espacio
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    # Título
    title = Paragraph("Reporte de Usuarios", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Si data es un diccionario lo convertimos en lista
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
    headers = [col for col in headers if col in all_columns]
    extra_cols = [col for col in all_columns if col not in headers]
    headers.extend(extra_cols)

    # Construcción de tabla
    table_data = [headers]
    for row in data:
        row_values = []
        for h in headers:
            value = row.get(h, "")
            # Usar Paragraph solo para strings largas, no números
            if isinstance(value, (int, float)):
                row_values.append(str(value))  # número como string plano
            elif isinstance(value, str) and len(value) > 20:
                row_values.append(Paragraph(value, styles["Normal"]))
            else:
                row_values.append(str(value))
        table_data.append(row_values)

    # Calcular ancho de columnas dinámicamente
    page_width = landscape(A4)[0] - 80
    col_width = page_width / len(headers)
    col_widths = [col_width for _ in headers]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Estilos
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    elements.append(table)

    # Footer con fecha
    elements.append(Spacer(1, 12))
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generado el {fecha}", styles["Normal"]))

    doc.build(elements)
    return filename