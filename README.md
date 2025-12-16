# Global Flight Routes Visualization

Interactive 3D visualization of global airport connections using Leafmap and MapLibre GL JS. Based on Dr. Qiusheng Wu's Leafmap tutorial on arc layers.

## View the Map

**Live Demo:** https://edgeoinnovations-resources.github.io/Flight/

## Features

- **Interactive Airport Selection**: Choose any major airport from the dropdown menu
- **Global Routes**: Visualizes 30,000+ flight routes
- **Arc Layer**: 3D arcs showing connections from the selected airport
- **Statistics**: View number of routes and destinations for each airport
- **Layer Control**: Toggle airports and routes on/off
- **Navigation**: 3D tilt (Ctrl+Drag), Rotate (Right-click+Drag), and zoom controls

## Statistics

- **Routes from ATL**: 205 destinations
- **Connected Airports**: 206 worldwide

## Technology

- [Leafmap](https://leafmap.org/) - Python mapping library by Dr. Qiusheng Wu
- [MapLibre GL JS](https://maplibre.org/) - Open-source map rendering
- Data: [OpenGeos Datasets](https://github.com/opengeos/datasets)

## Data Sources

| Dataset | URL |
|---------|-----|
| Airport Routes CSV | https://github.com/opengeos/datasets/releases/download/world/airport_routes.csv |
| Airports GeoJSON | https://github.com/opengeos/datasets/releases/download/world/airports.geojson |

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

This creates `index.html` which can be opened in a browser.

## Generate Map for Different Airport

Edit `generate_map.py` and change the airport code:

```python
# Available airports include:
# ATL (Atlanta), JFK (New York), LAX (Los Angeles),
# ORD (Chicago), DFW (Dallas), DEN (Denver),
# LHR (London), CDG (Paris), DXB (Dubai),
# HND (Tokyo), SIN (Singapore), HKG (Hong Kong)

create_flight_map(selected_airport="JFK")  # Change to any 3-letter code
```

Then run:
```bash
python generate_map.py
```

## Credits

- Based on Dr. Qiusheng Wu's [Leafmap Arc Layer Tutorial](https://leafmap.org/maplibre/arc_layer/)
- Data from [OpenGeos Datasets](https://github.com/opengeos/datasets)
