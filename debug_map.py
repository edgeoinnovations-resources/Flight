
import leafmap.maplibregl as leafmap
import pandas as pd
import geopandas as gpd

def debug():
    print("Initializing Map...")
    m = leafmap.Map(center=[0, 20], zoom=2)
    
    print(f"Initial calls: {len(m.calls)}")
    
    print("Adding layer control...")
    m.add_layer_control()
    
    print(f"Calls after adding control: {len(m.calls)}")
    print(f"Call details: {m.calls}")
    
    # Try adding a dummy layer
    print("Adding dummy layer...")
    try:
        m.add_marker([0, 0])
        print(f"Calls after marker: {len(m.calls)}")
    except Exception as e:
        print(f"Error adding marker: {e}")

if __name__ == "__main__":
    debug()
