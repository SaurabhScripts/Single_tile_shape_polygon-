
# for deleting images 
import os

# Define paths to the image and mask folders
image_folder = r'E:\Saurabh Meena\Habitation\habitation custom dat\mask'
mask_folder = r'E:\Saurabh Meena\Habitation\habitation custom dat\images'

# Get the list of image files in the image folder
image_files = os.listdir(image_folder)

# Get the list of mask files in the mask folder
mask_files = os.listdir(mask_folder)

# Iterate through the mask files and delete those not present in the image folder
for mask_file in mask_files:
    # Extract the base filename without the extension
    base_filename, _ = os.path.splitext(mask_file)
    
    # Check if the corresponding image file exists
    if base_filename not in [os.path.splitext(image)[0] for image in image_files]:
        # Construct the full path to the mask file
        mask_file_path = os.path.join(mask_folder, mask_file)
        
        # Delete the mask file
        os.remove(mask_file_path)
        print(f"Deleted: {mask_file_path}")
