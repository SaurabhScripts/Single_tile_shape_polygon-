import geopandas as gpd

# Load the shapefile
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Regularize the polygons to their convex hulls
gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.convex_hull)
gdf.to_file('convex_hulls.shp')

# Reload the original shapefile
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Regularize the polygons to their minimum bounding rectangles
gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.minimum_rotated_rectangle)
gdf.to_file('min_bounding_rectangles.shp')
