from video_source.video_source_interface import VideoSource


class FakeStream:
    def __init__(self, source_index):
        self.source_index = source_index
        self.is_streaming = False

    def __enter__(self):
        self.is_streaming = True
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.is_streaming = False


class FakeVideoSource(VideoSource):
    def __init__(self, source_index=0):
        self.source_index = source_index
        self.is_streaming = False

    def stream(self):
        return FakeStream(self.source_index)
