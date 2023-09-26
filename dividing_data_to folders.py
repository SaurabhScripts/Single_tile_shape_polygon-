import os
import shutil
import random

def split_data(source_images, source_masks, destination, train_ratio=0.7, val_ratio=0.2):
    all_images = os.listdir(source_images)
    all_masks = os.listdir(source_masks)
    
    # Shuffle the images to get a random distribution for splitting
    random.shuffle(all_images)

    num_images = len(all_images)
    num_train = int(num_images * train_ratio)
    num_val = int(num_images * val_ratio)
    num_test = num_images - num_train - num_val

    # Split images into train, test, and val sets
    train_images = all_images[:num_train]
    val_images = all_images[num_train:num_train+num_val]
    test_images = all_images[num_train+num_val:]

    datasets = {'train': train_images, 'val': val_images, 'test': test_images}
    
    # Create directories if they don't exist
    for dataset_name in datasets:
        os.makedirs(os.path.join(destination, dataset_name), exist_ok=True)
        os.makedirs(os.path.join(destination, f"{dataset_name}_labels"), exist_ok=True)

        # Copy images and masks to the respective directories
        for image_name in datasets[dataset_name]:
            shutil.copy(os.path.join(source_images, image_name), os.path.join(destination, dataset_name, image_name))
            
            # Generate the mask name by replacing the image extension with ".png"
            mask_name = os.path.splitext(image_name)[0] + '.png'
            shutil.copy(os.path.join(source_masks, mask_name), os.path.join(destination, f"{dataset_name}_labels", mask_name))

if __name__ == "__main__":
    SOURCE_IMAGES_DIR =r'E:\Saurabh Meena\Habitation\habitation custom dat\images'
    SOURCE_MASKS_DIR =  r'E:\Saurabh Meena\Habitation\habitation custom dat\mask'
    DESTINATION_DIR = r'E:\Saurabh Meena\Habitation\habitation custom dat\divided'

    split_data(SOURCE_IMAGES_DIR, SOURCE_MASKS_DIR, DESTINATION_DIR)
