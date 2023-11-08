from video_source.video_source_interface import VideoSource


class FakeStream(VideoSource):
    def __init__(self, frames, width=None, height=None):
        if frames is None or len(frames) == 0:
            raise ValueError("Frames must include at least one frame")
        self.frames = self._verify_frames(frames)
        self.is_streaming = False
        self.frame_idx = 0
        self.width, self.height = self._get_frame_dimensions(width, height)

    def _get_frame_dimensions(self, width, height):
        if width is None and height is None:
            width, height, _ = self.frames[0].shape
        return width, height

    def _verify_frames(self, frames):
        if not frames or len(frames) == 0:
            raise ValueError("Frames cannot be None or empty")
        return frames

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def open(self):
        self.is_streaming = True
        self.frame_idx = 0

    def close(self):
        self.is_streaming = False
        self.frame_idx = 0

    def stream(self):
        if not self.is_streaming:
            raise TypeError("Cannot Stream from closed stream.")

        if self.frame_idx >= len(self.frames):
            return (False, None)

        frame = self.frames[self.frame_idx]
        self.frame_idx += 1
        return (True, frame)
