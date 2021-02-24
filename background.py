from PIL import Image
from noise import pnoise2
import numpy as np

class Background:
    def __init__(self, dimensions, octaves):
        self.dimensions = dimensions
        self.octaves = octaves

    def background(self):
        texture = np.empty([self.dimensions[1], self.dimensions[0]])
        freq = 16.0 * self.octaves

        for i in range(self.dimensions[1]):
            for j in range(self.dimensions[0]):
                v = int(pnoise2(i / freq, j / freq, self.octaves) * 127.0 + 128.0)
                texture[i][j] = v 

        return Image.fromarray(texture).convert("RGB") 
        


# remove bg

# def remove_bg(self):
#         img = self.img
#         gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#         _, thresh = cv.threshold(gray_img, 127, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
#         img_contours = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]
#         img_contours = sorted(img_contours, key=cv.contourArea)
#         for i in img_contours:
#             if cv.contourArea(i) > 100:
#                 break
#         mask = np.zeros(img.shape[:2], np.uint8)
#         cv.drawContours(mask, [i],-1, 255, -1)
#         new_img = cv.bitwise_and(img, img, mask=mask)

#         cv.imwrite('masked.png', new_img)
#         self.img = new_img