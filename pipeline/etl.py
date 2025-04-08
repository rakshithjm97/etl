import geopandas as gpd
from sqlalchemy import create_engine
from pipeline.config import DB_URI
import fiona
import os

def sanitize_name(name):
    """Make table and layer names safe and lowercase."""
    return name.lower().replace(" ", "_")

def load_gdb_all_layers_separate_tables(gdb_paths, table_prefix=""):
    print(f"🔗 Connecting to DB: {DB_URI}")
    engine = create_engine(DB_URI)

    for gdb_path in gdb_paths:
        if not os.path.exists(gdb_path):
            print(f"⚠️ GDB not found: {gdb_path}")
            continue

        gdb_name = sanitize_name(os.path.splitext(os.path.basename(gdb_path))[0])
        layers = fiona.listlayers(gdb_path)
        print(f"\n📂 Reading GDB: {gdb_path}")
        print(f"   🧭 Found layers: {layers}")

        for layer in layers:
            try:
                print(f"   🔄 Loading layer: {layer}")
                gdf = gpd.read_file(gdb_path, layer=layer)
                gdf.columns = [col.lower() for col in gdf.columns]

                table_name = f"{table_prefix}{gdb_name}_{sanitize_name(layer)}"

                gdf.to_postgis(table_name, con=engine, if_exists='replace', index=False)
                print(f"   ✅ Loaded into table: {table_name}")
            except Exception as e:
                print(f"   ❌ Failed to load layer {layer} from {gdb_name}: {e}")

    print("\n✅ All layers loaded into separate tables.")

if __name__ == "__main__":
    gdb_paths = [
        r"D:\New\db\data\alabama\Aladama.gpkg",
        r"D:\New\db\data\arizona\Arizona.gpkg"
    ]

    load_gdb_all_layers_separate_tables(gdb_paths, table_prefix="nwi_")
