from loader import Loader
import tensorflow

path_dataset_train = './train/*'
loading_weights = (False, './w_')
shape_img = (256, 256, 3)
# Configure data loader
loading_img = Loader(shape_img=(shape_img[0], shape_img[1]), path_data=path_dataset_train)
# Number of filters in the first layer of G and D
generator_filters = 64
discriminator_filters = 64

target = tensorflow.keras.layers.Input(shape=shape_img)
in_img = tensorflow.keras.layers.Input(shape=shape_img)
optimizer = tensorflow.keras.optimizers.Adam(0.0002, 0.5)


def discriminator_layers(layer_input, filtres, kernal, batch_normalization):
    layer = tensorflow.keras.layers.Conv2D(filtres, kernel_size=kernal, strides=2, padding='same')(layer_input)
    layer = tensorflow.keras.layers.LeakyReLU(alpha=0.2)(layer)
    if batch_normalization:
        layer = tensorflow.keras.layers.BatchNormalization(momentum=0.8)(layer)
    return layer


concatenate_layers = tensorflow.keras.layers.Concatenate(axis=-1)([target, in_img])
d1 = discriminator_layers(concatenate_layers, discriminator_filters,     kernal=4, batch_normalization=False)
d2 = discriminator_layers(d1,                 discriminator_filters * 2, kernal=4, batch_normalization=True)
d3 = discriminator_layers(d2,                 discriminator_filters * 4, kernal=4, batch_normalization=True)
d4 = discriminator_layers(d3,                 discriminator_filters * 8, kernal=4, batch_normalization=True)
validity = tensorflow.keras.layers.Conv2D(1, kernel_size=4, strides=1, padding='same')(d4)
DISCRIMINATOR = tensorflow.keras.models.Model([target, in_img], validity)
DISCRIMINATOR.compile(loss='mse', optimizer=optimizer, metrics=['accuracy'])
