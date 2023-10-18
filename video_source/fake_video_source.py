from video_source.video_source_interface import VideoSource


class FakeVideoSource(VideoSource):
    def __init__(self, source_index=0):
        self.source_index = source_index
