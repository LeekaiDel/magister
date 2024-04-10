import cv2

name = 5

class FrameBreaker():
    def __init__(self):
        self.file_name = "../../TP_Videos/%d.mp4" % name
        self.dir_for_dataset = "../../plane_%d/" % name
        self.current_frame = 0
        self.img_raw = None

        cap = cv2.VideoCapture(self.file_name) 
        if(cap.isOpened() == False):
            print("Kurwa!")
            return

        self.frame_ok, self.img_raw = cap.read()

        while(self.frame_ok):
            self.frame_ok, self.img_raw = cap.read()
            self.current_frame += 1
            img_result = cv2.cvtColor(self.img_raw, cv2.COLOR_BGR2GRAY)
            cv2.imshow('result', img_result)
            cv2.imwrite(self.dir_for_dataset + "%d.jpg" % self.current_frame, img_result)

            if cv2.waitKey(1) == 27: 
                break

if __name__ == "__main__":
    FrameBreaker()
