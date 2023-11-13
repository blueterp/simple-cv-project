from .detector_interface import Detector
from video_source import VideoSource


class FakeBooleanDetector(Detector):
    """
    Used for unit testing components that require a detector.
    Detector relies on a FakeBooleanStream where the streamed
    frame indicates if something is detected.
    """

    def __init__(self, stream, show_stream=False):
        self.stream = self._validate_stream(stream)
        self.frame = None
        self.show_stream = show_stream

    def _validate_stream(self, stream):
        if not stream or not isinstance(stream, VideoSource):
            raise ValueError("Stream must be of type VideoSource")
        return stream

    def stream_frames(self):
        ret, boolean = self.stream.stream()
        self.frame = boolean if ret else None
        return ret

    def detect(self):
        ret = self.stream_frames()

    def detects_contours(self):
        return self.frame

    def _draw_contours(self):
        pass

    def get_active_frame(self):
        return self.frame

    def __enter__(self):
        self.stream.open()
        print(self.stream.is_open)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.stream.close()

    def show_frame(self):
        if self.show_stream:
            print(f"Showing Frame: {self.get_active_frame()}")
