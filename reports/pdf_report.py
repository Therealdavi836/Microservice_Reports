#Archivo de reportes en PDF

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data, filename="reporte.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Reporte de Datos")
    
    y = 720
    for item in data:
        c.drawString(100, y, str(item))
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()
    return filename