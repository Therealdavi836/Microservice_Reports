from locust import HttpUser, task, between
import random

class ReportServiceCapacityTest(HttpUser):
    wait_time = between(1, 2)
    token = "Bearer TOKEN_DE_PRUEBA_AQUI"

    @task(3)
    def generate_pdf_report(self):
        """Carga intensiva de generación de PDF"""
        headers = {"Authorization": self.token}
        payload = {
            "ms_url": "http://127.0.0.1:8002/api/vehicles",
            "type": f"stress_pdf_{random.randint(1, 100)}"
        }

        with self.client.post("/report/pdf", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error PDF: {response.status_code}")

    @task(2)
    def generate_excel_report(self):
        """Carga intensiva de generación de Excel"""
        headers = {"Authorization": self.token}
        payload = {
            "ms_url": "http://127.0.0.1:8002/api/vehicles",
            "type": f"stress_excel_{random.randint(1, 100)}"
        }

        with self.client.post("/report/excel", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error Excel: {response.status_code}")