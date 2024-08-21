import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import shutil

# Path to the folder containing images to classify
image_folder = r'D:\PY_PROGS\AIGenerationMusic.github.io\GAN_output'  # Update this path

# Path to the folder where classified images will be saved
output_folder = r'D:\PY_PROGS\AIGenerationMusic.github.io\classified'  # Update this path

# Load your trained model
model = load_model('D:\PY_PROGS\AIGenerationMusic.github.io\custom_cnn_model.h5')  # Update with your model file

# Define the target image size (should match what your model expects)
target_size = (28, 28)  # Update this if your images are different size

# Number of classes (update based on your model's classes)
num_classes = 20

# Set the confidence threshold
confidence_threshold = 0.99  # Only save images with a prediction confidence above this value

# counting the number of successful saves.
count = 0

# Ensure class folders exist
for i in range(num_classes):
    class_folder = os.path.join(output_folder, f'class_{i}')
    os.makedirs(class_folder, exist_ok=True)

# Load, classify, and save images
for img_name in os.listdir(image_folder):
    img_path = os.path.join(image_folder, img_name)
    
    if os.path.isfile(img_path):
        # Load and preprocess the image
        img = load_img(img_path, color_mode='grayscale', target_size=target_size)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = img_array / 255.0  # Normalize to [0, 1]

        # Predict the class
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        prediction_confidence = predictions[0][predicted_class]

        # Check if the confidence is above the threshold
        if prediction_confidence >= confidence_threshold:
            count += 1
            # Define the destination folder
            class_folder = os.path.join(output_folder, f'class_{predicted_class}')

            # Define the destination path
            destination_path = os.path.join(class_folder, img_name)

            # Copy the image to the appropriate class folder
            shutil.copy(img_path, destination_path)

            print(f'Image {img_name} classified as class {predicted_class} with confidence {prediction_confidence:.2f} and saved to {class_folder}')
        else:
            print(f'Image {img_name} classified as class {predicted_class} with confidence {prediction_confidence:.2f}, below the threshold and not saved.')

print("The number of images saved are: " + str(count))
