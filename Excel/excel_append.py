import os
from openpyxl import Workbook, load_workbook

def append_to_excel(diccionario, ruta_excel="censo_tortugas.xlsx"):
    if not os.path.exists(ruta_excel):
        wb = Workbook()
        ws = wb.active
        ws.title = "Datos"
        ws.append(list(diccionario.keys()))
        wb.save(ruta_excel)
    wb = load_workbook(ruta_excel)
    ws = wb.active
    headers = list(diccionario.keys())
    excel_headers = [cell.value for cell in ws[1]]
    if headers != excel_headers:
        raise Exception(
            "Encabezados no coinciden con el Excel.\n"
            f"Excel: {excel_headers}\n"
            f"Datos: {headers}"
        )
    valores = []
    for h in headers:
        valor = diccionario[h]
        if isinstance(valor, list):
            valor = ", ".join(valor)
        valores.append(valor)
    ws.append(valores)
    wb.save(ruta_excel)
    print("Datos agregados correctamente a", ruta_excel)
