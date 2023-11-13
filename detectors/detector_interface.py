from abc import ABC, abstractclassmethod


class Detector(ABC):
    def __init__(self, stream, show_stream=False):
        self.stream = stream
        self.show_stream = False

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

    @abstractclassmethod
    def __enter__(self):
        pass

    @abstractclassmethod
    def __exit__(self, exc_type, exc_value, tb):
        pass

    @abstractclassmethod
    def show_frame(self):
        pass
