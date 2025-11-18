import xml.etree.ElementTree as ET
import json
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

BASE = r"C:\Users\dylan\OneDrive\Escritorio\TEC\2025\Computación y Sociedad\OSMTracker_Tortugas_Cahuita"

input_gpx  = f"{BASE}\\gpx\\test.gpx"
output_geojson = f"{BASE}\\geojson\\test.geojson"

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # metros
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# ============================
# CARGA GPX
# ============================

tree = ET.parse(input_gpx)
root = tree.getroot()

namespace = root.tag.split("}")[0].strip("{")
ns = {"gpx": namespace}

# ============================
# Estructura GeoJSON
# ============================

geojson = {
    "type": "FeatureCollection",
    "features": []
}

# ======================================================
# WAYPOINTS (PUNTOS MARCADOS)
# ======================================================

waypoints = root.findall("gpx:wpt", ns)

for w in waypoints:
    lat = float(w.get("lat"))
    lon = float(w.get("lon"))

    ele_elem = w.find("gpx:ele", ns)
    ele = float(ele_elem.text) if ele_elem is not None else None

    name_elem = w.find("gpx:name", ns)
    name = name_elem.text if name_elem is not None else "Waypoint"

    time_elem = w.find("gpx:time", ns)
    timestamp = time_elem.text if time_elem is not None else None

    desc_elem = w.find("gpx:desc", ns)
    description = desc_elem.text if desc_elem is not None else None

    feature = {
        "type": "Feature",
        "properties": {
            "name": name,
            "elevation": ele,
            "time": timestamp,
            "description": description
        },
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat, ele]
        }
    }

    geojson["features"].append(feature)

# ======================================================
# TRACKPOINTS (RECORRIDO)
# ======================================================

coords_track = []
track_times = []
track_elevations = []

trackpoints = root.findall(".//gpx:trkpt", ns)

for t in trackpoints:
    lat = float(t.get("lat"))
    lon = float(t.get("lon"))

    ele_elem = t.find("gpx:ele", ns)
    ele = float(ele_elem.text) if ele_elem is not None else None

    time_elem = t.find("gpx:time", ns)
    timestamp = None
    if time_elem is not None:
        timestamp = datetime.fromisoformat(time_elem.text.replace("Z", "+00:00"))

    coords_track.append([lon, lat, ele])
    track_elevations.append(ele)
    track_times.append(timestamp)

# ============================
# CALCULOS DEL RECORRIDO
# ============================

total_distance = 0
for i in range(1, len(coords_track)):
    lon1, lat1, _ = coords_track[i-1]
    lon2, lat2, _ = coords_track[i]
    total_distance += haversine(lat1, lon1, lat2, lon2)

start_time = track_times[0] if track_times[0] else None
end_time = track_times[-1] if track_times[-1] else None

duration_seconds = (end_time - start_time).total_seconds() if start_time and end_time else None
duration_hours = duration_seconds / 3600 if duration_seconds else None

avg_speed = (total_distance / 1000) / duration_hours if duration_hours else None

# ============================
# AGREGAR TRACK COMO FEATURE
# ============================

track_feature = {
    "type": "Feature",
    "properties": {
        "type": "track",
        "distance_m": total_distance,
        "duration_s": duration_seconds,
        "start_time": start_time.isoformat() if start_time else None,
        "end_time": end_time.isoformat() if end_time else None,
        "avg_speed_kmh": avg_speed,
        "min_ele": min(track_elevations) if track_elevations else None,
        "max_ele": max(track_elevations) if track_elevations else None,
    },
    "geometry": {
        "type": "LineString",
        "coordinates": coords_track
    }
}

geojson["features"].append(track_feature)

# ============================
# GUARDAR GEOJSON
# ============================

with open(output_geojson, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=4)

print("Waypoints:", len(waypoints))
print("Trackpoints:", len(trackpoints))
print("Distancia total:", total_distance/1000, "km")
print("Duración:", duration_seconds, "segundos")
