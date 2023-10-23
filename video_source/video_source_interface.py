from abc import ABC, abstractclassmethod


class VideoSource(ABC):
    pass

    @abstractclassmethod
    def __enter__(self):
        pass

    @abstractclassmethod
    def __exit__(self, exc_type, exc_value, tb):
        pass

    @abstractclassmethod
    def stream(self):
        pass
