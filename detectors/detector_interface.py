from abc import ABC, abstractclassmethod


class Detector(ABC):
    def __init__(self, stream):
        self.frame_idx = 0
        self.frames = []
        self.stream = stream

    @abstractclassmethod
    def stream_frames(self):
        pass

    @abstractclassmethod
    def detect(self):
        pass

    @abstractclassmethod
    def detects_contours(self, stream):
        pass

    @abstractclassmethod
    def _draw_contours(self):
        pass

    def get_active_frame(self):
        if len(self.frames) == 0 or self.frame_idx >= len(self.frames):
            return None

        return self.frames[self.frame_idx]
