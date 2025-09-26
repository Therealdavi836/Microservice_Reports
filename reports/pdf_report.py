#Archivo de reportes en PDF

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data):
    """
    Genera un reporte PDF simple con los datos proporcionados.
    """
    filename = "reporte.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Reporte de datos")
    
    y = 720
    for item in data:
        c.drawString(100, y, str(item))
        y -= 20
    
    c.save()
    return filename