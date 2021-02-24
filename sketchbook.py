import cv2 as cv
import numpy as np
import random
from edges import Edges
# from png2svg import Vectorize
from background import Background
from PIL import Image, ImageOps
from matplotlib import pyplot as plt


filename = "screenshot.png"

class Sketch:
    def __init__(self, image):
        self.img = image

    def sketch(self):
        grey = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        inv = 255 - grey
        blur = cv.GaussianBlur(inv, (13,13), 0)
        return cv.divide(grey, 255-blur, scale=256)

# img = Image.open(filename)








# img = cv.imread(filename,0)
# img = cv.medianBlur(img,5)

# ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
# th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
#             cv.THRESH_BINARY,11,2)
# th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv.THRESH_BINARY,11,2)
# titles = ['Original Image', 'Global Thresholding (v = 127)',
#             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]

# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()