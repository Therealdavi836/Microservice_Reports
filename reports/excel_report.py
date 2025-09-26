#Archivo de reportes en Excel

import pandas as pd

def generate_excel(data):
    """
    Genera un reporte Excel simple con los datos proporcionados."""
    df = pd.DataFrame(data)
    filename = "reporte.xlsx"
    df.to_excel(filename, index=False)
    return filename