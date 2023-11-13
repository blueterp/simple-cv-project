from video_source.video_source_interface import VideoSource
from video_source.stream_exceptions import StreamClosedError


class FakeBooleanStream(VideoSource):
    def __init__(self, frames=None):
        self.width, self.height = 0, 0
        self.is_open = False
        self.frames = self._check_frames(frames)
        self.generator = self._make_generator(self.frames)

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def stream(self):
        if not self.is_open:
            raise StreamClosedError("Cannot stream frames from closed stream.")
        try:
            return next(self.generator)
        except StopIteration:
            self.close()
            return False, False

    def _check_frames(self, frames):
        if not frames or len(frames) == 0:
            raise ValueError("Must include at least one frame in constructor.")
        return frames

    def _make_generator(self, frames):
        for frame in frames:
            yield (True, frame)
