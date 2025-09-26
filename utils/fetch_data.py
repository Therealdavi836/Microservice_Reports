import requests

def get_service_token():
    """
    Solicita un token Bearer al microservicio de autenticación.
    """
    auth_url = "http://localhost:8001/api/login"  # Endpoint de login en Laravel
    credentials = {
        "email": "servicio@empresa.com",  # Usuario de servicio
        "password": "123456"              # Contraseña del servicio
    }
    response = requests.post(auth_url, json=credentials)
    response.raise_for_status()  # Lanza error si falla el login
    return response.json().get("token")


def get_data_from_ms():
    """
    Consulta el microservicio de datos usando un token Bearer dinámico.
    """
    token = get_service_token()
    url = "http://localhost:8000/api/data"  # Endpoint de otro microservicio
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanza error si falla la consulta
    return response.json()