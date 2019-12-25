from .backend import run_backend, include

if include("opencv"):
    import cv2
if include("skimage"):
    from skimage import transform
# if include("scipy"):
#     from scipy import ndimage
# if include("numpy"):
#     import numpy as np
if include("pillow"):
    from PIL import Image


def resize(im, output_shape, antialias=False):
    def run_skimage():
        return transform.resize(im, output_shape)

    def run_opencv():
        return cv2.resize(im, dsize=output_shape)

    def run_pillow():
        if antialias:
            # 开启抗锯齿，耗时增加8倍左右
            resample = Image.ANTIALIAS
        else:
            resample = Image.NEAREST
        im.resize(output_shape, resample)

    return run_backend(
            func_skimage=run_skimage,
            func_opencv=run_opencv,
            func_pillow=run_pillow
        )()

def rescale(im, scale):
    """ scale could be float or tuple like [0.2, 0.3] """
    def run_skimage():
        return transform.rescale(im, scale)

    def run_opencv():
        try:
            fx, fy = scale
        except TypeError:
            fx = fy = scale
        return cv2.resize(im, None, fx, fy)

    return run_backend(
            func_skimage=run_skimage,
            func_opencv=run_opencv
        )()

def rotate(im, angle):
    def run_skimage():
        return transform.rotate(im, angle)

    def run_opencv():
        # cv2.flip(im, flipCode)  # 翻转

        cols, rows = im.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        return cv2.warpAffine(im, M, (cols, rows))

    return run_backend(
            func_skimage=run_skimage,
        )()

def pyramid(im, downscale, method="gaussian"):
    def run_skimage():
        map_func = {
            "gaussian": transform.pyramid_gaussian,
            "laplacian": transform.pyramid_laplacian
        }
        return map_func[method](im, downscale)

    return run_backend(
            func_skimage=run_skimage,
        )()
