import imageio
import skimage.transform
import numpy
from glob import glob


class Loader:
    def __init__(self, shape_img=(128, 128), path_data='./*.jpg'):
        self.shape_img = shape_img
        self.paths_data = glob(path_data)

    def load_img(self, batch_size=1, mode='train'):
        global target, in_img
        if mode == 'ones':
            batch_num = 1
        else:
            batch_num = int(len(self.paths_data) / batch_size)
        for i in range(batch_num):
            batch = self.paths_data[i * batch_size:(i + 1) * batch_size]
            target_, in_img_ = [], []
            for img in batch:
                img = imageio.imread(img).astype(numpy.float)
                h, w, _ = img.shape
                target = img[:, :int(w / 2), :]
                in_img = img[:, int(w / 2):, :]
                target = skimage.transform.resize(target, self.shape_img)
                in_img = skimage.transform.resize(in_img, self.shape_img)
                if mode == 'train' and numpy.random.random() > 0.5:
                    target = numpy.fliplr(target)
                    in_img = numpy.fliplr(in_img)
                target_.append(target)
                in_img_.append(in_img)
            target_ = numpy.array(target_) / 127.5 - 1.
            in_img_ = numpy.array(in_img_) / 127.5 - 1.
            yield target_, in_img_
