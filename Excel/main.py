import xml.etree.ElementTree as ET
import sys
import os
from excel_append import append_to_excel

# =========================================================
# Diccionario: label del GPX → campo del censo
# =========================================================
BUTTON_MAP = {
    # Tipo avistamiento
    "Tortuga": "tipo_avistamiento",
    "Huella": "tipo_avistamiento",

    # Actividad
    "Saliendo del Agua": "actividad",
    "Bañándose": "actividad",
    "Excavando": "actividad",
    "Desovando": "actividad",
    "Camuflándose": "actividad",
    "Regresando": "actividad",
    "No se vio Tortuga": "actividad",

    # Especies
    "Baula": "especie",
    "Verde": "especie",
    "Carey": "especie",
    "Cabezona": "especie",

    # Pedúnculo
    "Completo": "estado_pedunculo",
    "Incompleto": "estado_pedunculo",

    # Dirección
    "Norte": "direccion",
    "Sur": "direccion",
    "Bosque": "direccion",
    "Mar": "direccion",

    # Hallazgos
    "Marcas": "hallazgos",
    "Cicatrices": "hallazgos",
    "Mordeduras": "hallazgos",
    "Ectoparásitos": "hallazgos",

    # Zona actividad
    "Olas": "zona_actividad",
    "Marea Baja": "zona_actividad",
    "Marea Alta": "zona_actividad",
    "Vegetación": "zona_actividad",

    # Destino del nido
    "In Situ": "destino_nido",
    "Robado": "destino_nido",
    "Reubicado en Playa": "destino_nido",
    "Vivero": "destino_nido",

    # Causa de reubicación
    "Vegetación": "causa_reubicacion",
    "Ola": "causa_reubicacion",
    "Huevero": "causa_reubicacion",
    "Erosión": "causa_reubicacion",
    "Manto Freático": "causa_reubicacion",

    # Pit tag
    "No Pit Tag": "pit_tag",
    "No Scanner": "pit_tag",

    # Tipo vivero
    "Ex Situ (Cajas)": "tipo_vivero",
    "In Situ (Playa)": "tipo_vivero",
}

def parse_gpx(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    censo = {
        "lat": None,
        "lon": None,
        "hora": None,
        "tipo_avistamiento": None,
        "actividad": None,
        "especie": None,
        "estado_pedunculo": None,
        "direccion": None,
        "zona_actividad": None,
        "destino_nido": None,
        "causa_reubicacion": None,
        "tipo_vivero": None,
        "pit_tag": None,
        "hallazgos": []
    }
    for i, wpt in enumerate(root.findall("g:wpt", ns)):
        if i == 0:
            censo["lat"] = float(wpt.get("lat"))
            censo["lon"] = float(wpt.get("lon"))

            t = wpt.find("g:time", ns)
            censo["hora"] = t.text if t is not None else None
        name = wpt.find("g:name", ns)
        if name is None or not name.text:
            continue
        label = name.text.strip()
        campo = BUTTON_MAP.get(label)
        if campo is None:
            continue  # botón desconocido, ignorar

        if campo == "hallazgos":
            censo["hallazgos"].append(label)
        else:
            censo[campo] = label
    return censo

if __name__ == "__main__":
    # Validar que se proporcionó argumento
    if len(sys.argv) < 2:
        print("Error: Se requiere la ruta del archivo GPX")
        print("Uso: python main.py <archivo.gpx>")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe")
        sys.exit(1)
    
    try:
        print(f"📍 Procesando archivo: {archivo}")
        datos = parse_gpx(archivo)
        print(f" Datos extraídos correctamente")
        print(f"   - Especie: {datos['especie']}")
        print(f"   - Actividad: {datos['actividad']}")
        print(f"   - Hallazgos: {datos['hallazgos']}")
        
        append_to_excel(datos)
        print(" Datos agregados a censo_tortugas.xlsx")
        
    except Exception as e:
        print(f" Error al procesar archivo: {str(e)}")
        sys.exit(1)
    
    # Solo pide input si está siendo ejecutado localmente (con terminal interactiva)
    if sys.stdin.isatty():
        input("Presione enter para salir")

