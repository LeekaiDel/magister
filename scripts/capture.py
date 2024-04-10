import cv2
import numpy as np

file_name = '../samples/1.mp4'

class DraftMethods():
    def __init__(self):
        # Захватываем избражение
        cap = cv2.VideoCapture(file_name) 
        if(cap.isOpened() == False):
            print("Kurwa!")

        while(cap.isOpened()):
            self.ret, self.frame = cap.read()
            if self.ret:
                # Конвертируем изображение в оттенки серого
                frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

                # frame_res = self.first_method(frame_gray)
                frame_res = self.second_hybrid_method(frame_gray)

                cv2.imshow("Frame_Orig", frame_gray)
                cv2.imshow("Frame_Res", frame_res)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows() 



    # Функция возвращает изображение обработанное градиентом
    def first_method(self, frame_gray):
        # Выделяем края по градиенту или эффекту Собеля
        frame_y = cv2.Sobel(frame_gray, cv2.CV_8UC1, 0, 1)
        frame_x = cv2.Sobel(frame_gray, cv2.CV_8UC1, 1, 0)
        frame_res = cv2.add(frame_x, frame_y)

        # Находим контуры
        # frame_copy = frame.copy()
        # contours, hierarchy = cv2.findContours(image=frame_res, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        # рисуем контуры на исходном изображении
        # cv2.drawContours(image=frame_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        return frame_res
    

    def second_method(self, frame_gray):
        frame_res = cv2.Canny(frame_gray, 50, 200)
        return frame_res
    

    def second_hybrid_method(self, frame_gray):

        # Выделяем края по градиенту или эффекту Собеля
        frame_y = cv2.Sobel(frame_gray, cv2.CV_8UC1, 0, 1)
        frame_x = cv2.Sobel(frame_gray, cv2.CV_8UC1, 1, 0)
        frame_res = cv2.add(frame_x, frame_y)

        ret, thresh = cv2.threshold(frame_res, 100, 255, cv2.THRESH_TOZERO)

        # frame_res = cv2.Canny(frame_res, 50, 200)
        return thresh


if __name__ == "__main__":
    DraftMethods()