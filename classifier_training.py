import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# # Set the path to your dataset directory
# data_dir = r'D:\PY_PROGS\AIGenerationMusic.github.io\Classifier_training_dataset'  # Update this path

# # Load images and labels
# images = []
# labels = []

# for class_name in os.listdir(data_dir):
#     class_dir = os.path.join(data_dir, class_name)
#     if os.path.isdir(class_dir):
#         for img_name in os.listdir(class_dir):
#             img_path = os.path.join(class_dir, img_name)
#             img = load_img(img_path, color_mode='grayscale', target_size=(28, 28))
#             img_array = img_to_array(img)
#             images.append(img_array)
#             labels.append(class_name)

# # Convert to numpy arrays
# images = np.array(images)
# labels = np.array(labels)

# # Encode the labels as integers
# label_map = {label: idx for idx, label in enumerate(np.unique(labels))}
# encoded_labels = np.array([label_map[label] for label in labels])

# # Perform train-test split
# train_images, test_images, train_labels, test_labels = train_test_split(
#     images, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
# )

# # Normalize the images to the [0, 1] range
# train_images = train_images / 255.0
# test_images = test_images / 255.0

# # Define the CNN model
# model = models.Sequential([
#     layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.Flatten(),
#     layers.Dense(64, activation='relu'),
#     layers.Dense(len(label_map), activation='softmax')  # Adjust output layer for the number of classes
# ])

# # Compile the model
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# # Train the model
# history = model.fit(train_images, train_labels, epochs=100, 
#                     validation_data=(test_images, test_labels))

# # Evaluate the model
# test_loss, test_acc = model.evaluate(test_images, test_labels)
# print(f'\nTest accuracy: {test_acc}')

# # Save the model
# model.save('custom_cnn_model.h5')

# # Plot training history
# plt.plot(history.history['accuracy'], label='accuracy')
# plt.plot(history.history['val_accuracy'], label='val_accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.ylim([0, 1])
# plt.legend(loc='lower right')
# plt.show()
