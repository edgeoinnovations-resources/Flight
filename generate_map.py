"""
Flight Routes Visualization with Leafmap MapLibre Backend
Creates an interactive 3D map showing airport connections

Requirements:
    pip install leafmap pandas geopandas

Output:
    index.html - Standalone HTML file for GitHub Pages
"""

import leafmap.maplibregl as leafmap
import pandas as pd

# Data URLs
ROUTES_URL = "https://github.com/opengeos/datasets/releases/download/world/airport_routes.csv"
AIRPORTS_URL = "https://github.com/opengeos/datasets/releases/download/world/airports.geojson"


def create_flight_map(selected_airport="ATL", src_color=[0, 255, 0], dst_color=[0, 128, 0]):
    """
    Create flight routes map for a specific airport.

    Args:
        selected_airport: 3-letter airport code (default: ATL)
        src_color: RGB list for source end of arc [R, G, B]
        dst_color: RGB list for destination end of arc [R, G, B]

    Returns:
        leafmap.Map object
    """
    # Load route data
    df = pd.read_csv(ROUTES_URL)

    # Filter for selected airport
    df_filtered = df[df['src_airport'] == selected_airport]

    # Get airport info for centering
    if len(df_filtered) > 0:
        center_lon = df_filtered['src_lon'].iloc[0]
        center_lat = df_filtered['src_lat'].iloc[0]
        airport_name = df_filtered['src_name'].iloc[0]
    else:
        center_lon, center_lat = 0, 20
        airport_name = selected_airport

    # Create map
    m = leafmap.Map(
        center=[center_lon, center_lat],
        zoom=3,
        pitch=0,
        style="dark-matter"
    )

    # Add airports layer (all airports as points)
    m.add_geojson(
        AIRPORTS_URL,
        layer_type="circle",
        paint={
            "circle-radius": 3,
            "circle-color": "#00ffff",
            "circle-opacity": 0.7
        },
        name="Airports"
    )

    # Add arc layer for selected airport's routes
    m.add_arc_layer(
        df_filtered,
        src_lat="src_lat",
        src_lon="src_lon",
        dst_lat="dst_lat",
        dst_lon="dst_lon",
        src_color=src_color,
        dst_color=dst_color,
        name=f"Routes from {selected_airport}"
    )

    # Add statistics HTML overlay
    stats_html = f"""
    <div style="
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-family: Arial, sans-serif;
        max-width: 250px;
    ">
        <h3 style="margin: 0 0 10px 0; color: #00ffff;">{selected_airport}</h3>
        <p style="margin: 5px 0; font-size: 12px;">{airport_name}</p>
        <p style="margin: 5px 0;"><strong>Destinations:</strong> {len(df_filtered)}</p>
        <p style="margin: 5px 0;"><strong>Countries:</strong> {df_filtered['dst_country'].nunique()}</p>
        <hr style="border-color: #333; margin: 10px 0;">
        <p style="margin: 5px 0; font-size: 11px; color: #aaa;">
            <strong>Controls:</strong><br>
            Ctrl + Drag: Tilt map<br>
            Right-click + Drag: Rotate
        </p>
    </div>
    """
    m.add_html(stats_html, position="top-left")

    return m


def main():
    # Create map with default airport (Atlanta - busiest US airport)
    m = create_flight_map(selected_airport="ATL")

    # Export to HTML
    m.to_html(
        "index.html",
        title="Global Flight Routes Visualization",
        width="100%",
        height="100%"
    )
    print("Map exported to index.html")


if __name__ == "__main__":
    main()
