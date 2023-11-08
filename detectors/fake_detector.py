from detectors.detector_interface import Detector


class FakeDetector(Detector):
    def __init__(self, stream):
        self.stream = stream
        self.frame = False

    def stream_frames(self):
        ret, self.frame = self.stream.stream()
        return ret

    def detect(self):
        return self.frame

    def detects_contours(self):
        return self.frame

    def _draw_contours(self):
        pass

    def get_active_frame(self):
        return self.frame

    def open(self):
        self.stream.open()

    def close(self):
        self.stream.close()

    def __enter__(self):
        self.stream.open()

    def __exit__(self, exc_type, exc_value, tb):
        self.stream.close()
