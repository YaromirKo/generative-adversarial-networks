from loader import Loader

path_dataset_train = './train/*'
shape_img = (256, 256, 3)

loading_img = Loader(shape_img=(shape_img[0], shape_img[1]), path_data=path_dataset_train)
