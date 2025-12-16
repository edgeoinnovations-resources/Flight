
"""
Flight Routes Visualization Generator
Creates a standalone interactive HTML map with embedded data.
"""

import pandas as pd
import geopandas as gpd
import json
import os

# Data URLs
ROUTE_URL = "https://github.com/opengeos/datasets/releases/download/world/airport_routes.csv"
AIRPORT_URL = "https://github.com/opengeos/datasets/releases/download/world/airports.geojson"

def generate_html(output_file="index.html"):
    print("Loading data...")
    
    # Load Routes
    df = pd.read_csv(ROUTE_URL)
    # Keep only necessary columns to reduce size
    route_cols = ["src_airport", "dst_airport", "src_lat", "src_lon", "dst_lat", "dst_lon"]
    df = df[route_cols]
    
    # Convert to list of dicts for JSON embedding
    routes_data = df.to_dict(orient="records")
    print(f"Loaded {len(routes_data)} routes.")

    # Load Airports
    gdf = gpd.read_file(AIRPORT_URL)
    # Convert to GeoJSON structure
    airports_data = json.loads(gdf.to_json())
    print(f"Loaded {len(airports_data['features'])} airports.")
    
    # Get list of unique source airports for dropdown
    src_airports = sorted(df["src_airport"].unique().tolist())
    

    # HTML Template
    # Using placeholders instead of f-string to avoid brace escaping hell
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Global Flight Routes</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- MapLibre GL JS -->
    <script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
    <link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet" />
    
    <!-- Deck.gl -->
    <script src="https://unpkg.com/deck.gl@8.9.36/dist.min.js"></script>
    
    <!-- D3 for color scales -->
    <script src="https://d3js.org/d3.v7.min.js"></script>
    
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
        
        #control-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            width: 300px;
            backdrop-filter: blur(10px);
        }
        
        h2 { margin-top: 0; color: #333; font-size: 1.2rem; }
        
        .control-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: 600; color: #555; }
        
        select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1rem;
        }
        
        .legend { font-size: 0.9rem; margin-top: 10px; }
        .legend-item { display: flex; align-items: center; margin-bottom: 5px; }
        .color-box { width: 15px; height: 15px; margin-right: 8px; border-radius: 3px; }
        
        #stats {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-size: 0.9rem;
            color: #666;
        }
        
        #toggle-3d {
            margin-top: 10px;
            display: inline-block;
            cursor: pointer;
            color: #007bff;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>

<div id="control-panel">
    <h2>Flight Explorer</h2>
    
    <div class="control-group">
        <label for="airport-select">Select Airport</label>
        <select id="airport-select">
            <!-- Options populated by JS -->
        </select>
    </div>
    
    <div id="stats">
        Select an airport to see routes.
    </div>
    
    <div class="control-group">
        <label>Layer Controls</label>
        <div>
            <input type="checkbox" id="show-airports" checked>
            <label for="show-airports" style="display:inline; font-weight:normal;">Show Airports</label>
        </div>
        <div>
            <input type="checkbox" id="show-routes" checked>
            <label for="show-routes" style="display:inline; font-weight:normal;">Show Flight Routes</label>
        </div>
    </div>
    
    <div style="margin-top:20px; font-size: 0.8em; color: #999;">
        Hold <b>Ctrl + Drag</b> to tilt 3D<br>
        Data: OpenGeos
    </div>
</div>

<div id="map"></div>

<script>
    // Embedded Data
    const ROUTES_DATA = __ROUTES_DATA__;
    const AIRPORTS_GEOJSON = __AIRPORTS_GEOJSON__;
    const SRC_AIRPORTS = __SRC_AIRPORTS__;
    
    // Initial State
    let currentAirport = "ATL";
    
    // DOM Elements
    const select = document.getElementById('airport-select');
    const statsDiv = document.getElementById('stats');
    
    // Populate Dropdown
    SRC_AIRPORTS.forEach(code => {
        const option = document.createElement('option');
        option.value = code;
        option.text = code;
        if (code === currentAirport) option.selected = true;
        select.appendChild(option);
    });
    
    // Initialize MapLibre
    const map = new maplibregl.Map({
        container: 'map',
        style: 'https://tiles.openfreemap.org/styles/liberty',
        center: [-84.4, 33.75], // ATL
        zoom: 3,
        pitch: 0,
        bearing: 0
    });
    
    map.addControl(new maplibregl.NavigationControl());
    
    // Initialize Deck.gl overlay variable
    let deckOverlay = null;

    function getAirportName(code) {
        // Find name in GeoJSON
        const feature = AIRPORTS_GEOJSON.features.find(f => f.properties.id === code);
        return feature ? feature.properties.name : code;
    }

    function updateLayers() {
        const selectedCode = select.value;
        const showRoutes = document.getElementById('show-routes').checked;
        const showAirports = document.getElementById('show-airports').checked;
        
        // Filter Routes
        const filteredRoutes = ROUTES_DATA.filter(d => d.src_airport === selectedCode);
        
        // Filter Connected Airports (Destination + Source)
        const connectedCodes = new Set(filteredRoutes.map(d => d.dst_airport));
        connectedCodes.add(selectedCode);
        
        const filteredAirports = AIRPORTS_GEOJSON.features.filter(f => 
            connectedCodes.has(f.properties.id)
        );
        
        // Update Stats
        statsDiv.innerHTML = `
            <strong>${selectedCode}</strong><br>
            ${getAirportName(selectedCode)}<br><br>
            Routes: ${filteredRoutes.length}<br>
            Destinations: ${connectedCodes.size - 1}
        `;
        
        // Deck.gl Layers
        const layers = [];
        
        if (showRoutes) {
            layers.push(new deck.ArcLayer({
                id: 'arc-layer',
                data: filteredRoutes,
                getSourcePosition: d => [d.src_lon, d.src_lat],
                getTargetPosition: d => [d.dst_lon, d.dst_lat],
                getSourceColor: [0, 255, 128],  // Greenish
                getTargetColor: [255, 200, 0],  // Orange/Yellow
                getWidth: 2,
                pickable: true,
                autoHighlight: true
            }));
        }
        
        if (showAirports) {
            layers.push(new deck.ScatterplotLayer({
                id: 'airport-layer',
                data: filteredAirports,
                getPosition: d => d.geometry.coordinates,
                getFillColor: d => d.properties.id === selectedCode ? [255, 0, 0] : [0, 128, 255],
                getRadius: d => d.properties.id === selectedCode ? 10000 : 5000,
                pickable: true,
                autoHighlight: true,
                onClick: (info) => {
                    if (info.object) {
                        // Optional: Click to select airport if it's a source airport
                        const clickedCode = info.object.properties.id;
                        if (SRC_AIRPORTS.includes(clickedCode)) {
                            select.value = clickedCode;
                            updateLayers();
                        }
                    }
                },
                getTooltip: ({object}) => object && `${object.properties.name} (${object.properties.id})`
            }));
        }
        
        // Create or Update Overlay
        if (!deckOverlay) {
            deckOverlay = new deck.MapboxOverlay({
                interleaved: true,
                layers: layers,
                getTooltip: ({object}) => object && object.src_airport ? 
                    `${object.src_airport} -> ${object.dst_airport}` : 
                    (object && object.properties ? object.properties.name : null)
            });
            map.addControl(deckOverlay);
        } else {
            deckOverlay.setProps({ layers: layers });
        }
    }
    
    // Event Listeners
    select.addEventListener('change', updateLayers);
    document.getElementById('show-routes').addEventListener('change', updateLayers);
    document.getElementById('show-airports').addEventListener('change', updateLayers);
    
    // Initial Render
    map.on('load', () => {
        updateLayers();
    });

</script>

</body>
</html>
    """
    
    # Inject data
    html_content = html_content.replace("__ROUTES_DATA__", str(routes_data))
    html_content = html_content.replace("__AIRPORTS_GEOJSON__", json.dumps(airports_data))
    html_content = html_content.replace("__SRC_AIRPORTS__", json.dumps(src_airports))

    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Successfully generated {output_file} ({len(html_content)/1024/1024:.2f} MB)")

if __name__ == "__main__":
    generate_html()
