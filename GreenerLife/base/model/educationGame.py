import os
import pathlib
import random

import cv2
import time
import numpy as np
from .HandTrackingModule import handDector
# import HandTrackingModule as htm
import math


class EudcationGame:

    def __init__(self, path=None, detectionCon=0.8):
        # hand track model
        self.detector = handDector(detectionCon=detectionCon)
        self.path = pathlib.Path(str(path))
        self.bin_image = cv2.imread(self.path + "bin.png", cv2.IMREAD_UNCHANGED)
        self.bin_image = cv2.resize(self.bin_image, (540, 80), interpolation=cv2.INTER_AREA)
        # self.path = self.path / "images"
        self.image_list = self.read_directory(self.path)
        self.ix, self.iy, self.cla = self.randomLocationAndIndex()
        self.image = self.image_list[str(self.cla)][0]
        self.rewardArea = {"0": (50, 180 + 50, 400, 480), "1": (180 + 50, 180 + 50 + 180, 400, 480),
                           "2": (180 + 50 + 180, 180 + 50 + 180 + 180, 400, 480)}
        self.cx_before, self.cy_before = 0, 0
        self.score = 0
        self.flag = False


    def updateLocation(self):
        self.ix, self.iy, self.cla = self.randomLocationAndIndex()

    def read_directory(self, directory_name):

        img_list = {}
        for filename in os.listdir(self.path + "images"):
            temp = filename.split("_")
            temp_path = self.path + "images"
            temp_path = temp_path + "/" + str(filename)
            img = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, (100, 100), interpolation=cv2.INTER_AREA)
            if temp[0] in img_list:
                img_list[temp[0]].append(img)
            else:
                img_list[temp[0]] = []
                img_list[temp[0]].append(img)
        return img_list

    def randomLocationAndIndex(self):
        return random.randint(100, 500), random.randint(100, 150), random.randint(0, 2)

    def overlayPNG(self, imgBack, imgFront, pos=[0, 0]):
        hf, wf, cf = imgFront.shape
        hb, wb, cb = imgBack.shape
        *_, mask = cv2.split(imgFront)
        maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
        maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        imgRGBA = cv2.bitwise_and(imgFront, maskBGRA)
        imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)

        imgMaskFull = np.zeros((hb, wb, cb), np.uint8)
        imgMaskFull[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = imgRGB
        imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
        maskBGRInv = cv2.bitwise_not(maskBGR)
        imgMaskFull2[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = maskBGRInv

        imgBack = cv2.bitwise_and(imgBack, imgMaskFull2)
        imgBack = cv2.bitwise_or(imgBack, imgMaskFull)

        return imgBack

    def run(self, img):
        img = cv2.flip(img, 1)
        img = self.detector.findHands(img, False)
        lmList, bbox = self.detector.findPosition(img)
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x1 - x2, y1 - y2)
            if length < 20:
                if self.ix < cx < self.ix + 100 and self.iy < cy < self.iy + 100 and self.iy + 50 < img.shape[
                    0] and self.ix + 50 < img.shape[1]:
                    self.ix, self.iy = cx - 50, cy - 50

        if 100 < self.ix + 100 < img.shape[1] and 100 < self.iy + 100 < img.shape[0]:
            if self.image.any() is not None:
                img = self.overlayPNG(img, self.image, [self.ix, self.iy])
        # get reward
        if self.rewardArea[str(self.cla)][2] < self.iy + 50 < self.rewardArea[str(self.cla)][3]:
            if self.rewardArea[str(self.cla)][0] < self.ix + 50 < self.rewardArea[str(self.cla)][1]:
                self.score += 1
                self.ix, self.iy, self.cla = self.randomLocationAndIndex()
                self.image = self.image_list[str(self.cla)][0]
            else:
                self.flag = True
        if len(lmList) != 0:
            if length < 20:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        img = cv2.rectangle(img, (50, 50), (590, 400), (0, 255, 0), 2)
        img = self.overlayPNG(img, self.bin_image, [50, 400])
        return img

# if __name__ == '__main__':
#     cap = cv2.VideoCapture(0)
#     model = Eudcation_Game()
#     while True:
#         success, img = cap.read()
#
#         img,flag = model.run(img)
#         print(flag)
#         cv2.imshow("image", img)
#         cv2.waitKey(1)
