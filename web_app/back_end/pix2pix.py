from PIL import Image
import imageio
import numpy
import skimage
import tensorflow as tf
from tensorflow import keras

tf.logging.set_verbosity(tf.logging.ERROR)


def load_generator_model():
    path = 'pix2pix_json_model.json'
    open_json_model = open(path)
    read_json_model = open_json_model.read()
    open_json_model.close()
    model = keras.models.model_from_json(read_json_model)
    return model


class Pix2Pix:
    def __init__(self):
        self.path = './weights/'
        self.generator = load_generator_model()
        self.img_res = (256, 256)

    def set_weight(self, id_style):
        self.generator.load_weights(self.path + id_style + '.h5')

    def load_img(self, path):
        input_img = imageio.imread(path).astype(numpy.float)
        input_img = skimage.transform.resize(
            input_img,
            self.img_res,
            anti_aliasing=True,
            anti_aliasing_sigma=None,
            mode='constant'
        )
        input_img = numpy.array(input_img) / 127.5 - 1.

        return numpy.reshape(input_img, (1, 256, 256, 3))

    def predict(self, path):
        input_img = self.load_img(path)
        target_img = self.generator.predict(input_img)
        target_img = Image.fromarray(((target_img[0] + 1) * 127.5).astype(numpy.uint8), mode="RGB")
        target_img.resize((512, 512))
        target_img.save(path[:-4] + 'stylized.jpg', format="JPEG")
        return path[:-4] + 'stylized.jpg'


# l = Pix2Pix()
# l.set_weight(str(0))
# l.predict('./static/3.jpg')
