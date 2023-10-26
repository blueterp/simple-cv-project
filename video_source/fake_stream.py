from video_source.video_source_interface import VideoSource


class FakeStream(VideoSource):
    def __init__(self, frames):
        if frames is None or len(frames) == 0:
            raise ValueError("Frames must include at least one frame")
        self.frames = self._verify_frames(frames)
        self.is_streaming = False
        self.width = frames[0].shape[0]
        self.height = frames[0].shape[1]
        self.frame_idx = 0

    def _verify_frames(self, frames):
        if not frames or len(frames) == 0:
            raise ValueError("Frames cannot be None or empty")

        # All frames must be of the same dimension
        width_set, height_set, color_set = set(), set(), set()
        for frame in frames:
            w, h, c = frame.shape
            width_set.add(w)
            height_set.add(h)
            color_set.add(c)

        if len(width_set) > 1 or len(height_set) > 1 or len(color_set) > 1:
            raise ValueError("All frames must have same dimensions")

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
