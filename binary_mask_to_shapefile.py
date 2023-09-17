import numpy as np
from keras.models import load_model
from skimage.io import imread
from skimage.transform import resize
import matplotlib.pyplot as plt

# Custom loss and metric functions
def dice_coef(y_true, y_pred, smooth=1):
    intersection = K.sum(y_true * y_pred, axis=[1,2,3])
    union = K.sum(y_true, axis=[1,2,3]) + K.sum(y_pred, axis=[1,2,3])
    return K.mean((2. * intersection + smooth) / (union + smooth), axis=0)

def dice_p_bce(in_gt, in_pred):
    return 0.05 * binary_crossentropy(in_gt, in_pred) - dice_coef(in_gt, in_pred)

def true_positive_rate(y_true, y_pred):
    return K.sum(K.flatten(y_true) * K.flatten(K.round(y_pred))) / K.sum(y_true)

# Load the trained model
model_path = '/content/full_best_model.h5'
model = load_model(model_path, custom_objects={'dice_p_bce': dice_p_bce, 'dice_coef': dice_coef, 'true_positive_rate': true_positive_rate})

def preprocess_image(image_path, target_size=(300, 300)):
    """Preprocess the image to be ready for model prediction."""
    img = imread(image_path)
    img = resize(img, target_size, mode='constant', preserve_range=True)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_on_image(model, image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    return prediction.squeeze()

# Predict on a single image
image_path = '/content/tiles20_6_3.tif'
predicted_mask = predict_on_image(model, image_path)

# Display the original image and the predicted mask
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.imshow(imread(image_path))
ax1.set_title("Original Image")
ax2.imshow(predicted_mask, cmap='gray')
ax2.set_title("Predicted Mask")
plt.show()
