# Archivo: generate_pdf.py

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import re

def generate_pdf(data, report_type="reporte", filename=None):
    """
    Genera un PDF dinámico en formato tabla a partir de cualquier JSON recibido.
    - data: lista o diccionario con datos a incluir.
    - report_type: string que describe el contenido ('usuarios', 'vehículos', 'ventas', etc.)
    - filename: opcional; si no se pasa, se genera automáticamente con base en report_type.
    """

    # Si no se especifica nombre, lo generamos automáticamente
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Asegurar nombre válido sin caracteres especiales
        safe_type = re.sub(r'[^a-zA-Z0-9_]', '_', report_type)
        filename = f"reporte_{safe_type}_{timestamp}.pdf"

    # Usamos formato horizontal para más espacio
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    # Título dinámico
    title = Paragraph(f"Reporte de {report_type.capitalize()}", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Convertir dict a lista si es necesario
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

    headers = list(all_columns)
    table_data = [headers]

    # Agregar filas de datos
    for row in data:
        row_values = []
        for h in headers:
            value = row.get(h, "")
            if isinstance(value, (int, float)):
                row_values.append(str(value))
            elif isinstance(value, str) and len(value) > 40:
                row_values.append(Paragraph(value, styles["Normal"]))
            else:
                row_values.append(str(value))
        table_data.append(row_values)

    # Calcular ancho de columnas dinámico
    page_width = landscape(A4)[0] - 80
    col_width = max(80, page_width / len(headers))
    col_widths = [col_width for _ in headers]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Estilo de tabla
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
    elements.append(Spacer(1, 12))

    # Footer con fecha
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generado automáticamente el {fecha}", styles["Normal"]))

    # Construir PDF
    doc.build(elements)
    return filename