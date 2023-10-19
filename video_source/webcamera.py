from video_source.video_source_interface import VideoSource
from video_source.stream import Stream


class WebCamera(VideoSource):
    def __init__(self, stream):
        self.stream = stream

    def stream(self):
        return self.stream
