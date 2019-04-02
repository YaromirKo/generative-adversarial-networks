from loader import Loader
import tensorflow
import numpy
import datetime
import sys
from time import sleep
import os
import matplotlib.pyplot
tensorflow.logging.set_verbosity(tensorflow.logging.ERROR)
########################################################################################################################
path_dataset_train = './train/*'
interval_save_weights = 1
epoch_for_new_bigin_train = 0
loading_weights_on_model = False
path_save_weights = 'drive/pix2pix_weights/generator_epoch_'
path_save_json_model = 'drive/pix2pix_weights/generator.json'
name_folder_for_testing = 'new_style'
loading_weights = (loading_weights_on_model, path_save_weights + str(epoch_for_new_bigin_train), epoch_for_new_bigin_train + 1)
print_info_models = True
print_info = True

########################################################################################################################
shape_img = (256, 256, 3)
# Configure data loader
if print_info:
    print("Configure data loader")
loading_img = Loader(shape_img=(shape_img[0], shape_img[1]), path_data=path_dataset_train)
########################################################################################################################
target = tensorflow.keras.layers.Input(shape=shape_img)
in_img = tensorflow.keras.layers.Input(shape=shape_img)
optimizer = tensorflow.keras.optimizers.Adam(0.0002, 0.5)
# Number of filters in the first layer of G and D
generator_filters = 64
discriminator_filters = 64
########################################################################################################################

if print_info:
    print("Build and compile the discriminator")
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

if print_info_models:
    print("DISCRIMINATOR")
    print(DISCRIMINATOR.summary())

# U-Net Generator
if print_info:
    print("Build the generator")
def generator_layers_conv(layer_input, filters, kernal, batch_normalization):
    layer = tensorflow.keras.layers.Conv2D(filters, kernel_size=kernal, strides=2, padding='same')(layer_input)
    layer = tensorflow.keras.layers.LeakyReLU(alpha=0.2)(layer)
    if batch_normalization:
        layer = tensorflow.keras.layers.BatchNormalization(momentum=0.8)(layer)
    return layer


def generator_layers_deconv(layer_input, skip_layer_input, filters, kernal, dropout_rate):
    layer = tensorflow.keras.layers.UpSampling2D(size=2)(layer_input)
    layer = tensorflow.keras.layers.Conv2D(filters, kernel_size=kernal, strides=1, padding='same', activation='relu')(layer)
    if dropout_rate:
        layer = tensorflow.keras.layers.Dropout(0.5)(layer)
    layer = tensorflow.keras.layers.BatchNormalization(momentum=0.8)(layer)
    layer = tensorflow.keras.layers.Concatenate()([layer, skip_layer_input])
    return layer


# Image input
image_input = tensorflow.keras.layers.Input(shape=shape_img)
# Downsampling
d1 = generator_layers_conv(image_input, generator_filters,     kernal=4, batch_normalization=False)
d2 = generator_layers_conv(d1,          generator_filters * 2, kernal=4, batch_normalization=True)
d3 = generator_layers_conv(d2,          generator_filters * 4, kernal=4, batch_normalization=True)
d4 = generator_layers_conv(d3,          generator_filters * 8, kernal=4, batch_normalization=True)
d5 = generator_layers_conv(d4,          generator_filters * 8, kernal=4, batch_normalization=True)
d6 = generator_layers_conv(d5,          generator_filters * 8, kernal=4, batch_normalization=True)
d7 = generator_layers_conv(d6,          generator_filters * 8, kernal=4, batch_normalization=True)
d8 = generator_layers_conv(d7,          generator_filters * 8, kernal=4, batch_normalization=True)

# Upsamplig
u0 = generator_layers_deconv(d8, d7, generator_filters * 8, kernal=4, dropout_rate=True )
u1 = generator_layers_deconv(u0, d6, generator_filters * 8, kernal=4, dropout_rate=True )
u2 = generator_layers_deconv(u1, d5, generator_filters * 8, kernal=4, dropout_rate=True )
u3 = generator_layers_deconv(u2, d4, generator_filters * 8, kernal=4, dropout_rate=False)
u4 = generator_layers_deconv(u3, d3, generator_filters * 4, kernal=4, dropout_rate=False)
u5 = generator_layers_deconv(u4, d2, generator_filters * 2, kernal=4, dropout_rate=False)
u6 = generator_layers_deconv(u5, d1, generator_filters,     kernal=4, dropout_rate=False)
u7 = tensorflow.keras.layers.UpSampling2D(size=2)(u6)
fake_output_img = tensorflow.keras.layers.Conv2D(shape_img[2], kernel_size=4, strides=1, padding='same', activation='tanh')(u7)
GENERATOR = tensorflow.keras.models.Model(image_input, fake_output_img)

if print_info_models:
    print("GENERATOR")
    print(GENERATOR.summary())

if loading_weights[0]:
    GENERATOR.load_weights(loading_weights[1])

fake_img_gen = GENERATOR(in_img)
# For the combined model we will only train the generator
DISCRIMINATOR.trainable = False
# Discriminators determines validity of translated images / condition pairs
valid = DISCRIMINATOR([fake_img_gen, in_img])
GAN = tensorflow.keras.models.Model(inputs=[target, in_img], outputs=[valid, fake_img_gen])
GAN.compile(loss=['mse', 'mae'], loss_weights=[1, 100], optimizer=optimizer)

if print_info_models:
    print("GAN")
    print(GAN.summary())
########################################################################################################################


def test_function_gen_img(epoch_, batch_s=3):
    os.makedirs('./%s' % name_folder_for_testing, exist_ok=True)
    r, c = batch_s, batch_s
    target_test, in_img_test = loading_img.load_data(batch_size=batch_s)
    fake_img_gen_test = GENERATOR.predict(in_img_test)
    imgs = numpy.concatenate([in_img_test, fake_img_gen_test, target_test])
    imgs = 0.5 * imgs + 0.5
    titles = ['Condition', 'Generated', 'Original']
    fig, axs = matplotlib.pyplot.subplots(r, c)
    index = 0
    for i in range(r):
        for j in range(c):
            axs[i, j].imshow(imgs[index])
            axs[i, j].set_title(titles[i])
            axs[i, j].axis('off')
            index += 1
    fig.savefig("./" + name_folder_for_testing + "/%d.png" % epoch_)
    matplotlib.pyplot.close()


# train
if print_info:
    print("start train")
epochs = 200
batch_size = 1
# Calculate output shape of D (PatchGAN)
patch = int(shape_img[0] / 2 ** 4)
valid = numpy.ones((batch_size, ) + (patch, patch, 1))
fake = numpy.zeros((batch_size, ) + (patch, patch, 1))

start_time = datetime.datetime.now()
for epoch in range(epochs - loading_weights[2]):
    steps = 0
    test_function_gen_img(epoch)
    for batch_index, (target, in_img) in enumerate(loading_img.load_batch(batch_size=batch_size)):
        # Train Discriminator
        # Condition on B and generate a translated version
        fake_img = GENERATOR.predict(in_img)
        # Train the discriminators (original images = real / generated = Fake)
        d_loss_real = DISCRIMINATOR.train_on_batch([target, in_img], valid)
        d_loss_fake = DISCRIMINATOR.train_on_batch([fake_img, in_img], fake)
        d_loss = 0.5 * numpy.add(d_loss_real, d_loss_fake)
        # Train Generator
        # Train the generators

        g_loss = GAN.train_on_batch([target, in_img], [valid, target])
        elapsed_time = datetime.datetime.now() - start_time
        if batch_index % int((loading_img.batch_num / 50)) == 0:
            steps += 1
        sys.stdout.write('\r')
        sys.stdout.write("[Epoch %d/%d] [%-51s] [Batch %d/%d] [D loss: %f, acc: %d%%] [G loss: %f] time: %s"
                         % (epoch + loading_weights[2], epochs, '=' * steps, batch_index, loading_img.batch_num, d_loss[0], 100*d_loss[1], g_loss[0], elapsed_time))
        sys.stdout.flush()
        sleep(0.25)
    print('\n')
    if epoch % interval_save_weights == 0:
        GENERATOR.save_weights(path_save_weights + str(epoch + loading_weights[2]) + ".h5")
    if epoch_for_new_bigin_train == 0:
        json_file = open(path_save_json_model, "w")
        json_file.write(GENERATOR.to_json())
        json_file.close()
