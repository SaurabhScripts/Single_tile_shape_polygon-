import os
import geopandas as gpd
import numpy as np
from rasterio.features import geometry_mask
from rasterio.transform import from_bounds
import matplotlib.pyplot as plt

def generate_mask_from_shapefile(shapefile_path, width=2200, height=2200, value_col='value'):
    """Generate a mask from a given shapefile with NaN handling."""
    gdf = gpd.read_file(shapefile_path)
    
    # Treat NaN values in 'id' as 0 and update the 'value' column accordingly
    gdf.loc[gdf['id'].isna(), value_col] = 0
    
    # Compute the bounding box of the GeoDataFrame
    bounds = gdf.total_bounds
    
    # Calculate the transform from the bounds and the desired dimensions
    transform = from_bounds(bounds[0], bounds[1], bounds[2], bounds[3], width, height)
    
    # Extract the geometries for values 0 and 1
    geoms_0 = gdf[gdf[value_col] == 0]['geometry'].tolist()
    geoms_1 = gdf[gdf[value_col] == 1]['geometry'].tolist()

    # Create masks using the calculated transform
    mask_0 = geometry_mask(geoms_0, transform=transform, invert=True, out_shape=(height, width))
    mask_1 = geometry_mask(geoms_1, transform=transform, invert=False, out_shape=(height, width))

    # Combine the masks: 0 where value=1 and 1 where value=0
    final_mask = np.where(mask_1, 0, 1)
    
    return final_mask

def process_directory_and_save_masks(directory_path, output_dir, mask_prefix="polygon"):
    """Process all shapefiles in a directory, generate masks, and save them with a specified prefix."""
    
    # List all shapefiles in the directory
    shapefiles = [f for f in os.listdir(directory_path) if f.endswith('.shp')]
    
    # Process each shapefile and save the mask
    for idx, shp in enumerate(shapefiles, start=1):
        try:
            mask = generate_mask_from_shapefile(os.path.join(directory_path, shp))
            output_file = os.path.join(output_dir, f"{mask_prefix}_{idx}.png")
            plt.imsave(output_file, mask, cmap='gray')
        except Exception as e:
            print(f"Error processing {shp}: {e}")

if __name__ == "__main__":
    directory_path = r"C:\Users\nikhil.jadhav1\individual_shapefiles2"
    output_directory = r"E:\Saurabh Meena\Habitation\habitation custom dat\mask"

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    process_directory_and_save_masks(directory_path, output_directory)
