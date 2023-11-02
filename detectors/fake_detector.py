from detectors.detector_interface import Detector


class FakeDetector(Detector):
    def __init__(self, stream):
        self.stream = stream
        self.frame = False

    def stream_frames(self):
        self.frame = self.stream.stream()

    def detect(self):
        return self.frame

    def detects_contours(self):
        return self.frame

    def _draw_contours(self):
        pass

    def get_active_frame(self):
        return self.frame
