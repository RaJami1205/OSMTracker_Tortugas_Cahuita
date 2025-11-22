# 🐢 Procesador de Censos de Tortugas desde GPX  
Este programa permite **leer archivos GPX exportados desde aplicaciones de campo**, interpretar los puntos y botones presionados, y **generar automáticamente un registro en un archivo Excel (`censo_tortugas.xlsx`)** con los datos del avistamiento o nido.

## 📂 Archivos del proyecto
### `main.py`
- Lee un archivo GPX.
- Interpreta los nombres de los waypoints según un mapa de botones (`BUTTON_MAP`).
- Construye un diccionario con los datos del censo.
- Lo envía a `excel_append.py` para guardarlo.

### `excel_append.py`
- Verifica o crea el archivo `censo_tortugas.xlsx`.
- Crea encabezados si el Excel no existe.
- Valida que los encabezados coincidan con los datos recibidos.
- Añade una nueva fila con la información procesada.

---

# 📌 ¿Qué información extrae el programa del GPX?
Cada botón presionado en el GPS/app se interpreta según `BUTTON_MAP` y se asigna a un campo del censo:

- **Coordenadas**: latitud, longitud  
- **Hora**: del primer punto del GPX  
- **Tipo de avistamiento**: Tortuga, Huella  
- **Actividad**: Saliendo del Agua, Desovando, Regresando, etc.  
- **Especie**: Baula, Verde, Carey, Cabezona  
- **Estado del pedúnculo**  
- **Dirección**  
- **Zona de actividad**  
- **Destino del nido**  
- **Causa de reubicación**  
- **Tipo de vivero**  
- **Pit tag** (si/no scanner/no pit tag)  
- **Hallazgos (lista)**: Marcas, Cicatrices, Mordeduras, etc.  

El campo **hallazgos** conserva múltiples valores en forma de lista.

---

# 🚀 Cómo usar el programa

## 1. Instalar dependencias
El único paquete necesario es `openpyxl`:

## 2. Tener los archivos en una misma carpeta

## 3. Ejecutar el programa con un archivo GPX
```python
python main.py archivo.gpx
```


