import os
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

def generate_and_save_images(model, epoch, test_input):
    predictions = model(test_input, training=False)
    images = (predictions * 127.5 + 127.5).numpy().astype(np.uint8)
    
    output_dir = 'GAN_output'
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(images.shape[0]):
        img = Image.fromarray(images[i, :, :, 0], mode='L')
        img.save(os.path.join(output_dir, f'image_at_epoch_{epoch:04d}_{i}.png'))

def make_discriminator_model():
    model = tf.keras.Sequential()
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same',
                                     input_shape=[28, 28, 1]))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model

def make_generator_model():
    model = tf.keras.Sequential()
    model.add(layers.Dense(7*7*256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((7, 7, 256)))
    assert model.output_shape == (None, 7, 7, 256)  # Note: None is the batch size

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    assert model.output_shape == (None, 7, 7, 128)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    assert model.output_shape == (None, 14, 14, 64)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    assert model.output_shape == (None, 28, 28, 1)

    return model

if __name__ == "__main__":
    # print("The tensorflow version is: " + tf.__version__)
    noise_dim = 100
    num_examples_to_generate = 15000
    seed = tf.random.normal([num_examples_to_generate, noise_dim])
    
    generator_optimizer = tf.keras.optimizers.Adam(1e-4)
    discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

    generator = make_generator_model()
    discriminator = make_discriminator_model()


    checkpoint_dir = 'D:\PY_PROGS\AIGenerationMusic.github.io\ck'
    checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                    discriminator_optimizer=discriminator_optimizer,
                                    generator=generator,
                                    discriminator=discriminator)
    checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))


    generate_and_save_images(epoch=6300, model=checkpoint.generator, test_input=seed)