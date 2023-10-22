import cv2


class VideoWriter:
    def __init__(self, file_name, frame_rate=20.0, width=768, height=576):
        self.file_name = file_name
        self.frame_rate = frame_rate
        self.width = width
        self.height = height
        self.writer = None

    def write(self, frame):
        if not self.writer:
            raise Exception("Cannot write to file. Writer is Closed")
        self.writer.write(frame)

    def __enter__(self):
        self.writer = cv2.VideoWriter(
            self.file_name,
            cv2.VideoWriter_fourcc(*"MJPG"),
            self.frame_rate,
            (self.width, self.height),
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.release()
        self.writer = None
