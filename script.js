const owner = "RaJami1205";
const repo = "OSMTracker_Tortugas_Cahuita";
const folder = "geojson";

const apiUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${folder}`;

const select = document.getElementById("geojsonList");
const details = document.getElementById("details");

let map = L.map('map').setView([9.9, -84.1], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let layerGroup = L.layerGroup().addTo(map);


// ========================================
// LISTA DE ARCHIVOS DEL REPO
// ========================================

async function loadList() {
  const res = await fetch(apiUrl);
  const data = await res.json();

  const geojsonFiles = data.filter(f => f.name.endsWith(".geojson"));

  geojsonFiles.forEach(f => {
    const opt = document.createElement("option");
    opt.value = f.download_url;
    opt.textContent = f.name;
    select.appendChild(opt);
  });

  if (geojsonFiles.length > 0) {
    loadGeoJSON(geojsonFiles[0].download_url);
  }
}


// ========================================
// CARGA DEL GEOJSON SELECCIONADO
// ========================================

async function loadGeoJSON(url) {
  const res = await fetch(url);
  const geo = await res.json();

  layerGroup.clearLayers(); 

  let trackFeature = null;

  // Primero se separan las features
  geo.features.forEach(f => {
    // PUNTO (waypoint)
    if (f.geometry.type === "Point") {
      const [lon, lat, ele] = f.geometry.coordinates;

      const marker = L.marker([lat, lon]).addTo(layerGroup);

      marker.bindTooltip(`
        <b>${f.properties.name}</b><br>
        Elevación: ${ele ?? "N/A"} m<br>
        Tiempo: ${f.properties.time ?? "N/A"}
      `);
    }

    // LINESTRING (track)
    if (f.geometry.type === "LineString") {
      trackFeature = f;

      const coords = f.geometry.coordinates.map(c => [c[1], c[0]]);
      const line = L.polyline(coords, { weight: 4 }).addTo(layerGroup);

      map.fitBounds(line.getBounds());
    }
  });

  // Mostrar detalles
  showTrackDetails(trackFeature);
}


// ========================================
// PANEL DE DETALLES
// ========================================

function showTrackDetails(track) {
  if (!track) {
    details.innerHTML = "No se encontraron datos del recorrido.";
    return;
  }

  const p = track.properties;

  const distanceKm = (p.distance_m / 1000).toFixed(2);
  const durationMin = (p.duration_s / 60).toFixed(1);

  details.innerHTML = `
    <b>Fecha:</b> ${formatDate(p.start_time)}<br>
    <b>Distancia:</b> ${distanceKm} km<br>
    <b>Duración:</b> ${durationMin} min<br>
    <b>Velocidad promedio:</b> ${p.avg_speed_kmh?.toFixed(2)} km/h<br>
    <b>Elevación mínima:</b> ${p.min_ele} m<br>
    <b>Elevación máxima:</b> ${p.max_ele} m<br>
    <b>Hora inicio:</b> ${formatTime(p.start_time)}<br>
    <b>Hora fin:</b> ${formatTime(p.end_time)}<br>
  `;
}

function formatTime(fechaISO) {
  const f = new Date(fechaISO);
  const hora = f.getHours().toString().padStart(2, "0");
  const min = f.getMinutes().toString().padStart(2, "0");

  return `${hora}:${min}`;
}

function formatDate(fechaISO) {
  const f = new Date(fechaISO);
  const dia = f.getDate().toString().padStart(2, "0");
  const mes = (f.getMonth() + 1).toString().padStart(2, "0");
  const año = f.getFullYear();

  return `${dia}/${mes}/${año}`;
}

// ========================================
// EVENTO AL SELECCIONAR
// ========================================
select.addEventListener("change", e => {
  loadGeoJSON(e.target.value);
});

loadList();
