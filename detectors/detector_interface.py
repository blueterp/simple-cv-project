from abc import ABC, abstractclassmethod


class Detector(ABC):
    def __init__(self, stream):
        self.stream = stream

    @abstractclassmethod
    def stream_frames(self):
        pass

    @abstractclassmethod
    def detect(self):
        pass

    @abstractclassmethod
    def detects_contours(self):
        pass

    @abstractclassmethod
    def _draw_contours(self):
        pass

    @abstractclassmethod
    def get_active_frame(self):
        pass
