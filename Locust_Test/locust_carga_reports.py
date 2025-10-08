from locust import HttpUser, task, between
import random

class ReportServiceLoadTest(HttpUser):
    wait_time = between(1, 3)
    
    # Token simulado (usar uno válido del MS de autenticación)
    token = "Bearer TOKEN_DE_PRUEBA_AQUI"

    @task(2)
    def generate_pdf_report(self):
        """Genera un reporte PDF desde otro microservicio"""
        headers = {"Authorization": self.token}
        payload = {
            "ms_url": "http://127.0.0.1:8002/api/vehicles",  # ejemplo de microservicio consultado
            "type": f"vehiculos_{random.randint(1, 100)}"
        }

        with self.client.post("/report/pdf", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error PDF: {response.status_code}")

    @task(2)
    def generate_excel_report(self):
        """Genera un reporte Excel desde otro microservicio"""
        headers = {"Authorization": self.token}
        payload = {
            "ms_url": "http://127.0.0.1:8002/api/vehicles",
            "type": f"vehiculos_{random.randint(1, 100)}"
        }

        with self.client.post("/report/excel", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error Excel: {response.status_code}")

    @task(1)
    def health_check(self):
        """Verifica estado del servicio"""
        with self.client.get("/report/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Servicio no disponible")