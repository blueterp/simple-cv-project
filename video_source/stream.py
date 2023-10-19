import cv2 as cv
from time import time, sleep


class Stream:
    def __init__(self, connection_info=0):
        self.connection_info = connection_info
        self.is_open = False
        self.video_capture = None

    def __enter__(self):
        self.video_capture = cv.VideoCapture(self.connection_info)
        self.is_open = self.video_capture.isOpened() if self.video_capture else False
        self.video_capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*"MJPG"))
        sleep(0.1)
        if not self.video_capture.isOpened():
            print("Cannot open camera")
            exit()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.video_capture.release()
        self.video_capture = None
        self.is_open = self.video_capture.isOpened() if self.video_capture else False

    def stream(self, duration_seconds=10, show=True):
        t_end = time() + duration_seconds

        while time() < t_end:
            ret, frame = self.video_capture.read()
            if show:
                cv.imshow("frame", frame)
                if cv.waitKey(1) == ord("q"):
                    break
        return ret, frame
