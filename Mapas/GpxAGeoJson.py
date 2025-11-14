import xml.etree.ElementTree as ET
import json

"""
Waypoints: Estos serían los puntos que uno va dejando con los botones de la
aplicación.

Trackpoints: Estos serían la traza o el recorrido que aplicamos directamente
con la aplicación
"""

tree = ET.parse("C:/Users/bryan/Downloads/prueba.gpx") # Este debe ser cambiado de manera automática para que agarre el de github
root = tree.getroot()

namespace = root.tag.split("}")[0].strip("{") #Obtención de la etiqueta xmlns para que solo tome la información de ese archivo
ns = {"gpx": namespace}
print("Namespace detectado:", namespace) #Para debug


#Estructura normal de un geoJson
geojson = {
    "type": "FeatureCollection",
    "features": []
}

#Estos son los botones que se van agregando al mapa
#En general los recorremos y los vamos guardando dentro de la misma
#estructura del geoJson
waypoints = root.findall("gpx:wpt", ns)

for w in waypoints:
    lat = float(w.get("lat"))
    lon = float(w.get("lon"))

    ele_elem = w.find("gpx:ele", ns)
    ele = float(ele_elem.text) if ele_elem is not None else None

    name_elem = w.find("gpx:name", ns)
    name = name_elem.text if name_elem is not None else "Waypoint"

    feature = {
        "type": "Feature",
        "properties": {
            "name": name
        },
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat, ele]
        }
    }

    geojson["features"].append(feature)

#Lista de coordenadas para toda el rastro que hayamos guardado
#Con el uso del GPS
coords_track = []

trackpoints = root.findall(".//gpx:trkpt", ns)

for t in trackpoints:
    latT = t.get("lat") #obtenemos latitud 
    lonT = t.get("lon") #obtenemos longitud
    coords_track.append([float(lonT), float(latT)]) #Las agregamos a la lista

    #Esto es solo para observar si se guardan bien los datos
    print("Trackpoint:")
    print("  lat:", latT)
    print("  lon:", lonT)
    print()

#Agregamos la lista completa del rastro que generamos
track_feature = {
    "type": "Feature",
    "properties": {
        "type": "track"
    },
    "geometry": {
        "type": "LineString",
        "coordinates": coords_track
    }
}

geojson["features"].append(track_feature)

print("Waypoints encontrados:", len(waypoints))
print("Trackpoints encontrados:", len(trackpoints))


#Aquí igual cambiar por el de github
with open("C:/Users/bryan/Documents/resultado.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=4)
