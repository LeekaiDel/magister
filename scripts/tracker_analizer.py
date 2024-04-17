#!/usr/bin/env python3
"""
Построить графиг зависимости расхождения от кадра
"""


import cv2
import time
import threading
import numpy as np 
import os
import time
import matplotlib.pyplot as plt

from parser_bbox import getListBboxes 

# Путь к вафлам разметки
bb_path = "../marks/tp_drone_x4"                # bb - bounding box
add_prefix = "frame_"
# Настройки трекера и трешолда
index = 0
trsh = 92                   # trsh - treshold
# Настройки видео
fr_width   = 640             # fr - frame
fr_height  = 512
fps_control = False

def drawTarget(img, target_point: tuple, f_yellow: int):  
    cv2.ellipse(img, 
            center=target_point, 
            axes=(10, 10),
            angle=0,
            startAngle=0,
            endAngle=360,
            color=(0, f_yellow * 255, 255),
            thickness=2)


def drawTargetBBox(img, bbox_array, bb_number: int):
    target_x = int(fr_width * (bbox_array[bb_number][1]) )   #  + bbox_array[bb_number][3] / 2)
    target_y = int(fr_height * (bbox_array[bb_number][2]) )  # + bbox_array[bb_number][4] / 2)
    # print("id: ", bb_number, " ", target_x, "/", target_y)
    drawTarget(img, (target_x, target_y), 0)

class HighlightColor():
    def __init__(self):
        self.tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT'] #   , 'GOTURN'
        
        # Global variables
        self.tracker_type       = self.tracker_types[index]
        self.tracker            = None
        self.iter_duration      = -1
        # Params
        self.start_bbox               = (356, 15, 182, 87)
        self.file_name          = "../../samples/draft.mp4"
        self.dir_for_dataset    = "../../dataset_1/"
        self.frame_count        = -1
        self.current_frame      = 0
        self.fps                = 25
        # Imgs
        self.img_raw            = None
        self.img_result         = None
        self.img_prepared       = None
        # States    
        self.frame_ok           = False
        self.tracker_init         = False
        self.play_state         = False
        # Configs
        self.min_th = 0
        self.max_th = 0

        cv2.namedWindow('result')
        # Создаём в окне result бегунки для задания порогов цвета
        cv2.createTrackbar('MinTh', 'result', 0, 255, self.min_th_cb)
        cv2.createTrackbar('MaxTh', 'result', 0, 255, self.max_th_cb)

        cv2.createButton('Play', self.play_cb)
        cv2.createButton('Stop', self.stop_cb)
        cv2.createButton('Set BBox', self.setBboxCb)
        cv2.createButton('Track', self.track_cb)

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
        self.bbox_arr = getListBboxes(bb_path, self.frame_count, add_prefix)
        print("Количество баундинбоксов в списке: ", self.bbox_arr.shape[0])

        # Читаем первый кадр
        self.frame_ok, self.img_raw = cap.read()

        while(True):
            # Читаем новые кадры только если включен плей
            if self.play_state:
                self.frame_ok, self.img_raw = cap.read()
                if self.frame_ok:
                    self.current_frame += 1

            if self.frame_ok: 
                self.img_result = cv2.cvtColor(self.img_raw, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('Raw', self.img_result)

                if self.img_result is not None:
                    img_result = cv2.blur(self.img_result, (3, 3))                                          
                    ret, img_result = cv2.threshold(img_result, trsh, 255, cv2.THRESH_BINARY) #self.min_th   // 100, 120, 140 // эталон: 124
                    # Увеличиваем контуры белых объектов (Делаем противоположность функции erode) - делаем две итерации
                    maskDi = cv2.dilate(img_result, None, iterations=1)
                    maskEr = cv2.erode(maskDi, None, iterations=1)
                    self.img_result = cv2.cvtColor(maskEr, cv2.COLOR_GRAY2RGB)  # maskEr
                
                    if self.tracker_init:
                        start_t = time.time()
                        update_ok, self.start_bbox = self.tracker.update(self.img_result)
                        self.iter_duration = time.time() - start_t

                        # Draw bounding box
                        if update_ok:
                            # Tracking success
                            p1 = (int(self.start_bbox[0]), int(self.start_bbox[1]))
                            p2 = (int(self.start_bbox[0] + self.start_bbox[2]), int(self.start_bbox[1] + self.start_bbox[3]))

                            tracker_x = int(self.start_bbox[0]) + int(self.start_bbox[2] // 2) 
                            tracker_y = int(self.start_bbox[1]) + int(self.start_bbox[3] // 2)

                            cv2.rectangle(self.img_result, p1, p2, (255, 0, 0), 2, 1)
                            drawTarget(self.img_result, (tracker_x, tracker_y), 1)

                            if(self.current_frame < self.bbox_arr.shape[0]):
                                drawTargetBBox(self.img_result, self.bbox_arr, self.current_frame)  


                        else :
                            # Tracking failure
                            cv2.putText(self.img_result, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0, 0, 255), 2)
                            # print("Object Lost!   >> ", self.current_frame, "/", self.frame_count, "|", int((self.current_frame / self.frame_count) * 100))
                    else:
                        self.tracker_init = self.tracker.init(self.img_result, self.start_bbox)

                    cv2.imshow('result', self.img_result)

            # os.system("clear    ")
            # print("Duration iter  >>", round(self.iter_duration, 2), "c")
            # print("Percent point  >> ", int((self.current_frame / self.frame_count) * 100), "%", "/", 100, "%" )
            # print("Frame point    >> ", self.current_frame, "/", self.frame_count )

            if cv2.waitKey(1) == 27: 
                break
            if(fps_control):
                time.sleep(1 / self.fps)



    def setBboxCb(self, i, j):
        # self.start_bbox = cv2.selectROI(self.img_result, False)
        # self.tracker_init = self.tracker.init(self.img_result, self.start_bbox)
        print("self.tracker_init ", self.tracker_init)

    # Эта функция ничего не делает (Логично блять)
    def min_th_cb(self, x):
        self.min_th = x

    def max_th_cb(self, x):
        self.max_th = x


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
