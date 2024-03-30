#!/usr/bin/env python3

import cv2
# from sympy import Q 
import time
import threading
import numpy as np 

class HighlightColor():
    def __init__(self):
        self.file_name = "../samples/3.mp4"
        # Global variables
        self.img_raw = None
        self.img_result = None

        self.ret = False
        self.play_state = False

        self.min_th = 0
        self.max_th = 0
        # Создаем подписку на топик
        # Создаем панель фейдеров для подбора значений выделения цвета
        # Создам пустое окно с именем result
        cv2.namedWindow('result')
        # Создаём в окне result бегунки для задания порогов цвета
        cv2.createTrackbar('MinTh', 'result', 0, 255, self.min_th_cb)
        cv2.createTrackbar('MaxTh', 'result', 0, 255, self.max_th_cb)

        cv2.createButton('Play', self.play_cb)
        cv2.createButton('Stop', self.stop_cb)

        # self.get_frame_thread = threading.Thread(target    = self.get_frame_heandler, args = (), daemon = True)
        # self.get_frame_thread.start()          # Запускаем опрос СТЗ

        # Главный цикл
        # cap = cv2.VideoCapture("/dev/video0")    #stereo elp >> /dev/video2, /dev/video4
        # cap.set(cv2.CAP_PROP_FPS, 24) # Частота кадров
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Ширина кадров в видеопотоке.
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Высота кадров в видеопотоке.

        # Захватываем избражение
        cap = cv2.VideoCapture(self.file_name) 
        if(cap.isOpened() == False):
            print("Kurwa!")
            return

        while(True):
            # Проверяем приходила ли картинка через флажок ret
            if self.play_state:
                self.ret, self.img_raw = cap.read()

                if self.ret: 
                    self.img_result = cv2.cvtColor(self.img_raw, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('Raw', self.img_result)

            if self.img_result is not None:
                img_result = cv2.blur(self.img_result, (3, 3))   
                ret, img_result = cv2.threshold(img_result, self.min_th, 255, cv2.THRESH_BINARY)
                # Увеличиваем контуры белых объектов (Делаем противоположность функции erode) - делаем две итерации
                maskDi = cv2.dilate(img_result, None, iterations=1)
                maskEr = cv2.erode(maskDi, None, iterations=1)

                cv2.imshow('result', maskEr)

            if cv2.waitKey(1) == 27: 
                break
            time.sleep(1 / 25)


    # Эта функция ничего не делает (Логично блять)
    def min_th_cb(self, x):
        self.min_th = x
        # print(x)
    

    def max_th_cb(self, x):
        self.max_th = x
        # print(x)


    def play_cb(self, i, j):
        self.play_state = True
        print("Press Play")


    def stop_cb(self, i, j):
        self.play_state = False
        print("Press Stop")


if __name__ == "__main__":
    HighlightColor()
