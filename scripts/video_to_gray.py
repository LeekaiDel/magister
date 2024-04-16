import cv2

origin_filename = "/home/leekai/Workspaces/TP_Videos/a.mp4"

target_filename = "../../flying_plane.avi"
target_width    = 640   # TP: 640
target_height   = 512   # TP: 512
target_fps      = 25

class VideoToGray():
    def __init__(self):
        self.cap = cv2.VideoCapture(origin_filename)
        self.out = cv2.VideoWriter(target_filename, cv2.VideoWriter_fourcc(*'XVID'), target_fps, (target_width, target_height))

        if(self.cap.isOpened() == False):
            print("Kurwa!")
            return

        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))   # Находим количество кадров во всем файле
        print("Количество кадров в файле: ", self.frame_count)

        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

                self.out.write(frame)
                cv2.imshow("Frame", frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break


if __name__ == "__main__":
    VideoToGray()
