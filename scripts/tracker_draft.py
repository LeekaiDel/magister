#!/usr/bin/env python3

import cv2
import time
import threading
import numpy as np 
import os
import time
import matplotlib.pyplot as plt

index = 6
trsh = 92
write_dataset = False

class HighlightColor():
    def __init__(self):
        self.tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT'] #   , 'GOTURN'
        
        # Global variables
        self.tracker_type = self.tracker_types[index]
        self.tracker = None
        self.iter_duration = -1
        # Params
        self.bbox = (356, 15, 182, 87)
        self.file_name = "../../samples/draft.mp4"
        self.dir_for_dataset = "../../dataset_1/"
        self.frame_count = -1
        self.current_frame = 0
        self.fps = 25
        # Imgs
        self.img_raw = None
        self.img_result = None
        self.img_prepared = None
        # States
        self.frame_ok = False
        self.tracker_ok = False
        self.play_state = False
        # Configs
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
        cv2.createButton('Set BBox', self.setBboxCb)
        cv2.createButton('Track', self.track_cb)

        # self.get_frame_thread = threading.Thread(target = self.getBBox, args = (), daemon = True)
        # self.get_frame_thread.start()    

        # Главный цикл
        # cap = cv2.VideoCapture("/dev/video0")    #stereo elp >> /dev/video2, /dev/video4
        # cap.set(cv2.CAP_PROP_FPS, 24) # Частота кадров
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Ширина кадров в видеопотоке.
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Высота кадров в видеопотоке.

        # Создаем Трекер
        if self.tracker_type == 'BOOSTING':
           self.tracker = cv2.legacy.TrackerBoosting_create()
        if self.tracker_type == 'MIL':
            self.tracker = cv2.legacy.TrackerMIL.create()
        if self.tracker_type == 'KCF':
            self.tracker = cv2.legacy.TrackerKCF_create()
        if self.tracker_type == 'TLD':
            self.tracker = cv2.legacy.TrackerTLD_create()
        if self.tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.legacy.TrackerMedianFlow_create()
        # if tracker_type == 'GOTURN':
        #     self.tracker = cv2.legacy.TrackerGOTURN_create()
        if self.tracker_type == 'MOSSE':
            self.tracker = cv2.legacy.TrackerMOSSE_create()
        if self.tracker_type == "CSRT":
            self.tracker = cv2.legacy.TrackerCSRT_create()


        # Захватываем избражение
        cap = cv2.VideoCapture(self.file_name) 
        if(cap.isOpened() == False):
            print("Kurwa!")
            return

        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   # Находим количество кадров во всем файле
        print("Количество кадров в файле: ", self.frame_count)

        # Читаем первый кадр
        self.frame_ok, self.img_raw = cap.read()

        while(True):
            # Читаем новые кадры только если включен плей
            if self.play_state:
                self.frame_ok, self.img_raw = cap.read()
                self.current_frame += 1
                # Записать датасет из отдельных кадров
                if(write_dataset):
                    cv2.imwrite(self.dir_for_dataset + "frame_%d.jpg" % self.current_frame, self.img_raw)

            if self.frame_ok: 
                self.img_result = cv2.cvtColor(self.img_raw, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('Raw', self.img_result)

            if self.img_result is not None:
                img_result = cv2.blur(self.img_result, (3, 3))                                          
                ret, img_result = cv2.threshold(img_result, trsh, 255, cv2.THRESH_BINARY) #self.min_th   // 100, 120, 140 // эталон: 124
                # Увеличиваем контуры белых объектов (Делаем противоположность функции erode) - делаем две итерации
                maskDi = cv2.dilate(img_result, None, iterations=1)
                maskEr = cv2.erode(maskDi, None, iterations=1)

                self.img_result = cv2.cvtColor(maskEr, cv2.COLOR_GRAY2RGB)

                if self.tracker_ok:
                    start_t = time.time()
                    tracker_ok, self.bbox = self.tracker.update(self.img_result)
                    self.iter_duration = time.time() - start_t
                    # Draw bounding box
                    if tracker_ok:
                        # Tracking success
                        p1 = (int(self.bbox[0]), int(self.bbox[1]))
                        p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                        cv2.rectangle(self.img_result, p1, p2, (255, 0, 0), 2, 1)
                    else :
                        # Tracking failure
                        cv2.putText(self.img_result, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0, 0, 255), 2)
                        print("Object Lost!   >> ", self.current_frame, "/", self.frame_count, "|", int((self.current_frame / self.frame_count) * 100))
                        # return

                # self.findBBox(maskEr)

                cv2.imshow('result', self.img_result)

            os.system("clear    ")
            print("Duration iter  >>", round(self.iter_duration, 2), "c")
            print("Percent point  >> ", int((self.current_frame / self.frame_count) * 100), "%", "/", 100, "%" )
            print("Frame point    >> ", self.current_frame, "/", self.frame_count )

            if cv2.waitKey(1) == 27: 
                break
            time.sleep(1 / self.fps)


    # def findBBox(self, frame):
    #     contours, hierarchy = cv2.findContours(image = frame, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_SIMPLE)
    #     contours = sorted(contours, key = cv2.contourArea, reverse = True)
    #     print(len(contours))
    #     # cv2.drawContours(image = frame, contours = contours, contourIdx = -1, color = (0, 255, 0), thickness = 2, lineType = cv2.LINE_AA)
    #     # pass


    # def getBBox(self):
    #     while(True):
    #         if self.img_prepared is not None:
    #             self.bbox = cv2.selectROI(self.img_prepared, False)
    #           print(5)


    def setBboxCb(self, i, j):
        # self.bbox = cv2.selectROI(self.img_result, False)
        self.tracker_ok = self.tracker.init(self.img_result, self.bbox)
        print("self.tracker_ok ", self.tracker_ok)


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


    def track_cb(self, i, f):
        self.start_track = True
        print("Press Track")


if __name__ == "__main__":
    HighlightColor()
