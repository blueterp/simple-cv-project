import cv2
from datetime import datetime


class VideoWriter:
    def __init__(
        self,
        video_width,
        video_height,
        buffer=None,
        frame_rate=20.0,
        fourcc=cv2.VideoWriter_fourcc(*"MJPG"),
        file_name_preface="",
    ):
        self.frame_rate = frame_rate
        self.width = video_width
        self.height = video_height
        self.fourcc = fourcc
        self.writer = None
        self.buffer = buffer
        self.file_name_preface = file_name_preface

    def write(self, frame):
        if not self.writer:
            raise Exception("Cannot write to file. Writer is Closed")
        self.writer.write(frame)

    # def __enter__(self):
    #     self.writer = cv2.VideoWriter(
    #         self.file_name,
    #         self.fourcc,
    #         self.frame_rate,
    #         (self.width, self.height),
    #     )
    #     if self.buffer:
    #         for frame in self.buffer:
    #             self.writer.write(frame)
    #         self.buffer = None

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.writer.release()
    #     self.writer = None

    def open(self, file_name=None, buffer=None):
        if not file_name:
            file_preface = (
                "" if len(self.file_name_preface) == 0 else f"{self.file_name_preface}_"
            )
            file_name = f"{file_preface}{datetime.now().strftime('%Y%m%d_%H:%M:%S')}"
        self.writer = cv2.VideoWriter(
            file_name,
            cv2.VideoWriter_fourcc(*"MJPG"),
            self.frame_rate,
            (self.width, self.height),
        )

        if buffer:
            for item in buffer:
                self.writer.write(item)

    def release(self):
        self.writer.release()
        self.writer = None

    def is_open(self):
        return self.writer is not None
