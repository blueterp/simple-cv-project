from video_writer.video_writer_interface import VideoWriterInterface


class FakeVideoWriter(VideoWriterInterface):
    def __init__(self, file_name=None, buffer=None):
        self.file_name = file_name
        self.buffer = buffer
        self.frames = False

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def open(self, file_name=None, buffer=None):
        self.frames = True

        self.file_name = file_name if file_name else self.file_name
        self.buffer = buffer if buffer else self.buffer

    def release(self):
        self.frames = False
        with open(self.file_name, "w"):
            pass

    def write(self, frame):
        if not self.is_open():
            raise AttributeError("Cannot write if writer is not open.")

    def is_open(self):
        return self.frames
