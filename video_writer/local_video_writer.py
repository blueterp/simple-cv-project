import cv2
from datetime import datetime
from video_writer.video_writer_interface import VideoWriterInterface


class LocalVideoWriter(VideoWriterInterface):
    def __init__(
        self,
        video_width,
        video_height,
        buffer=None,
        frame_rate=20.0,
        fourcc=cv2.VideoWriter_fourcc(*"MJPG"),
    ):
        self.frame_rate = frame_rate
        self.width = video_width
        self.height = video_height
        self.fourcc = fourcc
        self.writer = None
        self.buffer = buffer

    def write(self, frame):
        if not self.writer:
            raise AttributeError("Cannot write to file. Writer is Closed")
        self.writer.write(frame)

    def __call__(self, file_name=None, include_timestamp=False):
        self.file_name = self._generate_file_name(file_name, include_timestamp)
        print("FILENAME")
        print(self.file_name)
        return self

    def __enter__(self):
        self.open(
            buffer=self.buffer,
            file_name=self.file_name,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.release()
        self.writer = None

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

    def open(self, file_name=None, buffer=None, include_timestamp=False):
        self.__call__(file_name, include_timestamp)
        self.writer = cv2.VideoWriter(
            self.file_name,
            self.fourcc,
            self.frame_rate,
            (self.width, self.height),
        )

        if buffer:
            for item in buffer:
                self.writer.write(item)
            self.buffer.clear_buffer()

    def release(self):
        self.writer.release()
        self.writer = None

    def is_open(self):
        return self.writer is not None
