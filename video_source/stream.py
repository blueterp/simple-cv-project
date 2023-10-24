import cv2 as cv
from time import time, sleep
from video_source.video_source_interface import VideoSource


class Stream(VideoSource):
    def __init__(self, connection_info):
        self.connection_info = connection_info
        self.is_open = False
        self.video_capture = None

        with self:
            self.width = int(self.video_capture.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
            self.height = int(self.video_capture.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)

    def __enter__(self):
        self.video_capture = cv.VideoCapture(self.connection_info)
        if not self.video_capture.isOpened():
            raise TypeError(
                "Invalid connection information. Please specify busid or video file"
            )
        self.is_open = True
        self.video_capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*"MJPG"))
        sleep(0.1)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if self.video_capture:
            self.video_capture.release()
        self.video_capture = None
        self.is_open = False

    def stream(self, show=False):
        ret, frame = self.video_capture.read()
        if not ret:
            print("stream has ended or there is an error")
            self.__exit__(None, None, None)
        if show:
            cv.imshow("frame", frame)
            cv.waitKey(1)
        return ret, frame
