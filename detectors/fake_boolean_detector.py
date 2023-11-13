from .detector_interface import Detector
from video_source import VideoSource


class FakeBooleanDetector(Detector):
    """
    Used for unit testing components that require a detector.
    Detector relies on a FakeBooleanStream where the streamed
    frame indicates if something is detected.
    """

    def __init__(self, stream):
        self.stream = self._validate_stream(stream)
        self.frame = None

    def _validate_stream(self, stream):
        if not stream or not isinstance(stream, VideoSource):
            raise ValueError("Stream must be of type VideoSource")
        return stream

    def stream_frames(self):
        ret, boolean = self.stream.stream()
        self.frame = boolean if ret else None
        return ret, boolean

    def detect(self):
        ret, boolean = self.stream_frames()

    def detects_contours(self):
        return self.frame

    def _draw_contours(self):
        pass

    def get_active_frame(self):
        return self.frame

    def __enter__(self):
        self.stream.is_open = True
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.stream.is_open = False
