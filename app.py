#Microservicio de generación de reportes en PDF y Excel

from flask import Flask, request, send_file
from reports.pdf_report import generate_pdf
from reports.excel_report import generate_excel
import requests

app = Flask(__name__)

def get_data_from_ms(ms_url, token):
    """
    Consulta cualquier microservicio usando el token Bearer recibido.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ms_url, headers=headers)
    response.raise_for_status()
    return response.json()

@app.route("/report/pdf", methods=["POST"])
def report_pdf():
    # Obtiene el token enviado por el usuario
    token = request.headers.get("Authorization")
    if not token:
        return {"error": "Token no proporcionado"}, 401

    token = token.replace("Bearer ", "")
    ms_url = request.json.get("ms_url")  # URL del microservicio
    if not ms_url:
        return {"error": "ms_url no proporcionado"}, 400

    # Obtiene los datos y genera el PDF
    data = get_data_from_ms(ms_url, token)
    filename = generate_pdf(data)
    return send_file(filename, as_attachment=True)

@app.route("/report/excel", methods=["POST"])
def report_excel():
    # Obtiene el token enviado por el usuario
    token = request.headers.get("Authorization")
    if not token:
        return {"error": "Token no proporcionado"}, 401

    token = token.replace("Bearer ", "")
    ms_url = request.json.get("ms_url")  # URL del microservicio
    if not ms_url:
        return {"error": "ms_url no proporcionado"}, 400

    # Obtiene los datos y genera el Excel
    data = get_data_from_ms(ms_url, token)
    filename = generate_excel(data)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)