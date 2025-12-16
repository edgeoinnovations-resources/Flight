# Global Flight Routes Visualization

Interactive 3D visualization of global airport connections using Leafmap and MapLibre GL JS.

## Features

- View flight routes from any major airport
- 3D tilt view (Ctrl + drag)
- Globe projection mode
- Layer toggle controls
- Airport statistics overlay

## View the Map

Visit: https://edgeoinnovations-resources.github.io/Flight/

## Technology

- [Leafmap](https://leafmap.org/) - Python mapping library
- [MapLibre GL JS](https://maplibre.org/) - Open-source map rendering
- Data: [OpenGeos Datasets](https://github.com/opengeos/datasets)

## Usage

**Map Controls:**
- **Ctrl + Drag**: Tilt the map for 3D perspective
- **Right-click + Drag**: Rotate the map
- **Scroll**: Zoom in/out
- **Click globe icon**: Switch to 3D globe view

## Local Development

```bash
# Clone the repository
git clone https://github.com/edgeoinnovations-resources/Flight.git
cd Flight

# Install dependencies
pip install -r requirements.txt

# Generate the map
python generate_map.py
```

This will create `index.html` which can be opened in a browser.

## Regenerating the Map

To regenerate the map with a different airport:

```python
from generate_map import create_flight_map

# Create map for JFK airport with custom colors
m = create_flight_map(
    selected_airport="JFK",
    src_color=[255, 0, 0],   # Red source
    dst_color=[128, 0, 0]    # Dark red destination
)
m.to_html("index.html")
```

## Data Sources

- **Airport Routes**: [airport_routes.csv](https://github.com/opengeos/datasets/releases/download/places/airport_routes.csv)
- **Airport Locations**: [airports.geojson](https://github.com/opengeos/datasets/releases/download/places/airports.geojson)

## Credits

Based on Dr. Qiusheng Wu's Leafmap tutorial on arc layers for transportation route visualization.
