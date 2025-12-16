"""
Flight Routes Visualization with Leafmap MapLibre Backend
Based on Dr. Qiusheng Wu's arc layer tutorial

This script generates a standalone HTML file showing flight routes
from a selected airport. The HTML can be hosted on GitHub Pages.

Requirements:
    pip install leafmap pandas geopandas

Output:
    index.html - Standalone HTML file for GitHub Pages
"""

import pandas as pd
import geopandas as gpd
import leafmap.maplibregl as leafmap

# Official data URLs from leafmap documentation
ROUTE_URL = "https://github.com/opengeos/datasets/releases/download/world/airport_routes.csv"
AIRPORT_URL = "https://github.com/opengeos/datasets/releases/download/world/airports.geojson"


def create_flight_map(selected_airport="ATL"):
    """
    Create flight routes map for a specific airport.

    Args:
        selected_airport: 3-letter airport code (default: ATL - Atlanta)

    Returns:
        Exported HTML file path
    """

    # Load data
    print(f"Loading route data from {ROUTE_URL}...")
    df = pd.read_csv(ROUTE_URL)
    print(f"Total routes in dataset: {len(df)}")

    print(f"Loading airport data from {AIRPORT_URL}...")
    gdf = gpd.read_file(AIRPORT_URL)
    print(f"Total airports: {len(gdf)}")

    # Filter routes for selected airport
    selected_df = df[df["src_airport"] == selected_airport]
    print(f"Routes from {selected_airport}: {len(selected_df)}")

    if len(selected_df) == 0:
        print(f"WARNING: No routes found for airport {selected_airport}")
        print(f"Available airports: {df['src_airport'].unique()[:20]}...")
        return

    # Get destination airports + source airport for point layer
    dst_airports = selected_df["dst_airport"].unique().tolist() + [selected_airport]
    selected_gdf = gdf[gdf["id"].isin(dst_airports)]
    print(f"Connected airports: {len(selected_gdf)}")

    # Create map centered on US (good for ATL default)
    m = leafmap.Map(
        center=[-98, 39],
        zoom=3,
        pitch=0,
        style="liberty"
    )

    # Add satellite basemap (hidden by default, can toggle)
    m.add_basemap(
        "Esri.WorldImagery",
        visible=False,
        before_id=m.first_symbol_layer_id
    )

    # Add airport points (only connected airports)
    m.add_gdf(
        selected_gdf,
        name="Airports",
        fit_bounds=False
    )

    # Add arc layer - column names must match exactly
    m.add_arc_layer(
        selected_df,
        src_lon="src_lon",
        src_lat="src_lat",
        dst_lon="dst_lon",
        dst_lat="dst_lat",
        src_color=[0, 255, 0],       # Green at source
        dst_color=[255, 255, 0],     # Yellow at destination
        name=f"Routes from {selected_airport}"
    )

    # Add layer control for toggling layers
    m.add_layer_control()

    # Export to HTML
    output_file = "index.html"
    m.to_html(
        output_file,
        title=f"Flight Routes from {selected_airport}",
        width="100%",
        height="100%"
    )

    print(f"\n✅ Map exported to {output_file}")
    print(f"   Routes shown: {len(selected_df)}")
    print(f"   Airports shown: {len(selected_gdf)}")
    return output_file


def main():
    """Generate the map with Atlanta as default airport."""

    # You can change this to any airport code:
    # ATL (Atlanta), JFK (New York), LAX (Los Angeles),
    # ORD (Chicago), DFW (Dallas), DEN (Denver), etc.

    create_flight_map(selected_airport="ATL")

    print("\n📍 To deploy:")
    print("   1. git add .")
    print("   2. git commit -m 'Update flight routes map'")
    print("   3. git push origin main")
    print("   4. Enable GitHub Pages in repository settings")


if __name__ == "__main__":
    main()
