import os
import rasterio
import geopandas as gpd
from rasterio.mask import mask
# from keras.preprocessing import image
# from keras.applications.imagenet_utils import preprocess_input

# Specify the paths to your TIFF file and shapefile
tiff_path =r"E:\Saurabh Meena\Image_download and ortho_saurabh\Small_image_for_model\tiles_334_1_0.tif"
shapefile_path = r"E:\Saurabh Meena\bulding data\shape_335\shape_sam_335.shp"

# Read the shapefile using geopandas
shapefile = gpd.read_file(shapefile_path)

# Add a new column for predictions to the shapefile
shapefile['Prediction'] = ""

# Read the TIFF file
with rasterio.open(tiff_path) as src:
    # Make sure the coordinate reference systems (CRS) of the TIFF and shapefile match
    shapefile = shapefile.to_crs(src.crs)

    # Loop through the polygons in the shapefile
    for index, row in shapefile.iterrows():
        geom = row['geometry']
        if geom is None:
         continue
        # Convert the geometry into a list of GeoJSON-like dict
        geoms = [geom.__geo_interface__]

        # Clip the TIFF file using the polygon
        clipped_image, clipped_transform = mask(src, geoms, crop=True)

        # Save the clipped image to a temporary file
        clipped_image_path = r"E:\Saurabh Meena\Image_download and ortho_saurabh\temp\polygon.tif"
        clipped_meta = src.meta.copy()
        clipped_meta.update({
            'driver': 'GTiff',
            'height': clipped_image.shape[1],
            'width': clipped_image.shape[2],
            'transform': clipped_transform
        })
        with rasterio.open(clipped_image_path, 'w', **clipped_meta) as dst:
            dst.write(clipped_image)

        # Load and preprocess the clipped image
        img = image.load_img(clipped_image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Load the saved weights into the model
        # model.load_weights(r'C:/Users/nikhil.jadhav1/Downloads/checkpoints/my_checkpoint')

        # Make the prediction
        prediction_probs = model.predict(x)
        predicted_label_index = np.argmax(prediction_probs, axis=1)
        original_label = lb.inverse_transform([predicted_label_index])[0]

        # Update the shapefile with the prediction
        shapefile.at[index, 'Prediction'] = original_label

        # Delete the temporary clipped image
        os.remove(clipped_image_path)

# Save the updated shapefile
output_shapefile_path =r"E:\Saurabh Meena\bulding data\shape_335\Updated_Shapefile.shp"
shapefile.to_file(output_shapefile_path)
