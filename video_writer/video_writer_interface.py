from abc import ABC, abstractclassmethod


class VideoWriterInterface(ABC):
    @abstractclassmethod
    def __enter__(self):
        pass

    @abstractclassmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractclassmethod
    def open(self, file_name=None, buffer=None, include_timestamp=True):
        pass

    @abstractclassmethod
    def release(close):
        pass

    @abstractclassmethod
    def write(self, frame):
        pass

    @abstractclassmethod
    def is_open(self):
        pass
