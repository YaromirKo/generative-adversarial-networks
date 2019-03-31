import imageio
import skimage.transform
import numpy
from glob import glob

class Loader:
    def __init__(self, shape_img=(128, 128), path_data='./*'):
        self.img_res = shape_img
        self.paths_data = glob(path_data)
        self.batch_num = 0

    def load_data(self, batch_size=1):
        path = self.paths_data

        batch_images = numpy.random.choice(path, size=batch_size)

        imgs_A = []
        imgs_B = []
        for img_path in batch_images:
            img = imageio.imread(img_path).astype(numpy.float)

            h, w, _ = img.shape
            _w = int(w / 2)
            img_A, img_B = img[:, :_w, :], img[:, _w:, :]

            img_A = skimage.transform.resize(img_A, self.img_res)
            img_B = skimage.transform.resize(img_B, self.img_res)
            imgs_A.append(img_A)
            imgs_B.append(img_B)

        imgs_A = numpy.array(imgs_A) / 127.5 - 1.
        imgs_B = numpy.array(imgs_B) / 127.5 - 1.
        return imgs_A, imgs_B

    def load_batch(self, batch_size=1):
        path = self.paths_data
        self.batch_num = int(len(path) / batch_size)

        for i in range(self.batch_num):
            batch = path[i * batch_size:(i + 1) * batch_size]
            imgs_A, imgs_B = [], []
            for img in batch:
                img = imageio.imread(img).astype(numpy.float)
                h, w, _ = img.shape
                half_w = int(w / 2)
                img_A = img[:, :half_w, :]
                img_B = img[:, half_w:, :]
                img_A = skimage.transform.resize(img_A, self.img_res)
                img_B = skimage.transform.resize(img_B, self.img_res)
                imgs_A.append(img_A)
                imgs_B.append(img_B)

            imgs_A = numpy.array(imgs_A) / 127.5 - 1.
            imgs_B = numpy.array(imgs_B) / 127.5 - 1.

            yield imgs_A, imgs_B
