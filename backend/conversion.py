from PIL import Image
import numpy as np
import cv2
from potrace import Bitmap, POTRACE_TURNPOLICY_BLACK

"""
SOME FUNCTIONS JUST USED TO FIX SOME PROBLEMS WITH VIDEO

No need to use all of them depending on the image
"""
# i wanted to convert some white lines to black
def white2black(input_img, ceiling=200):
    img_arr = np.array(input_img)
    img_arr[img_arr > ceiling] = 0
    im = Image.fromarray(img_arr)
    return im

# the were some frames with black background and white lines
def reverse(input_img, ceiling=200, floor=100):
    img_arr = np.array(input_img)
    img_arr[img_arr > ceiling] = 150
    img_arr[img_arr < floor] = 255
    img_arr[img_arr == 150] = 0
    im = Image.fromarray(img_arr)
    return im

# apply canny to frames
def canny(input_img, tresh_lower=120, tresh_upper=200):
    """
    i played around with this values, found which one fits you best
    """
    canny = cv2.Canny(input_img, tresh_lower, tresh_upper)
    return canny

# got it from the documentation ^-^
def img2svg(imgPath: str):
    img = Image.open(imgPath)
    bm = Bitmap(img, blacklevel=0.5)
    path = bm.trace(
        turdsize=2,
        turnpolicy=POTRACE_TURNPOLICY_BLACK,
        alphamax=1,
        opticurve=False,
        opttolerance=0.2,
    )
    return path

