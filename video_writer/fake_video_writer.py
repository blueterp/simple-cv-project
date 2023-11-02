from datetime import datetime
from video_writer.video_writer_interface import VideoWriterInterface


class FakeVideoWriter(VideoWriterInterface):
    def __init__(self):
        self.frames = False

    def __call__(self, file_name=None, include_timestamp=False, buffer=None):
        self.file_name = self._generate_file_name(
            file_name=file_name, include_timestamp=include_timestamp
        )
        self.buffer = buffer
        return self

    def __enter__(self):
        self.open(file_name=self.file_name, buffer=self.buffer)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def open(self, file_name=None, buffer=None, include_timestamp=False):
        self.__call__(
            file_name=file_name, buffer=buffer, include_timestamp=include_timestamp
        )
        self.frames = True

    def release(self):
        self.frames = False
        with open(self.file_name, "w"):
            pass

    def write(self, frame):
        if not self.is_open():
            raise AttributeError("Cannot write if writer is not open.")

    def is_open(self):
        return self.frames

    def _generate_file_name(self, file_name, include_timestamp):
        if not file_name and not include_timestamp:
            raise ValueError("Must provide file_name or set include_timestampt to True")
        file_name = file_name + "_" if file_name else ""
        timestamp = (
            datetime.now().strftime("%Y%m%d_%H:%M:%S") + "_"
            if include_timestamp
            else ""
        )

        return f"{file_name}_{timestamp}".strip("_")
