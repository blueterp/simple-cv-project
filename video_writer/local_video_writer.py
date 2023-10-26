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
        file_name=None,
        include_timestamp=True,
    ):
        self.frame_rate = frame_rate
        self.width = video_width
        self.height = video_height
        self.fourcc = fourcc
        self.writer = None
        self.buffer = buffer
        self.file_name = file_name
        self.include_timestamp = include_timestamp

    def write(self, frame):
        if not self.writer:
            raise AttributeError("Cannot write to file. Writer is Closed")
        self.writer.write(frame)

    def __enter__(self):
        self.open(
            buffer=self.buffer,
            file_name=self.file_name,
            include_timestamp=self.include_timestamp,
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

        return f"{file_name}_{timestamp}".rstrip("_")

    def open(self, file_name=None, buffer=None, include_timestamp=True):
        file_name = self._generate_file_name(file_name, include_timestamp)
        print("filename", file_name)
        self.writer = cv2.VideoWriter(
            file_name,
            self.fourcc,
            self.frame_rate,
            (self.width, self.height),
        )

        if buffer:
            for item in buffer:
                self.writer.write(item)
            self.buffer = None

    def release(self):
        self.writer.release()
        self.writer = None

    def is_open(self):
        return self.writer is not None
