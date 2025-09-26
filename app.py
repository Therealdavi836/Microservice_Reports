#Microservicio de generación de reportes en PDF y Excel

from flask import Flask, request, send_file
from reports.pdf_report import generate_pdf
from reports.excel_report import generate_excel
from utils.fetch_data import get_data_from_ms

app = Flask(__name__)

@app.route("/report/pdf", methods=["POST"])
def report_pdf():
    """
    Genera un reporte PDF con los datos proporcionados o los obtiene del microservicio.
    """
    data = request.json or get_data_from_ms()
    filename = generate_pdf(data)
    return send_file(filename, as_attachment=True)

@app.route("/report/excel", methods=["POST"])
def report_excel():
    """
    Genera un reporte Excel con los datos proporcionados o los obtiene del microservicio.
    """
    data = request.json or get_data_from_ms()
    filename = generate_excel(data)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)