import pytest
from time import sleep
from video_source.webcamera import WebCamera
from video_source.stream import Stream
import cv2 as cv


def test_create_webcamera():
    stream = Stream(0)
    camera = WebCamera(stream)
    assert camera is not None
    assert camera.stream == stream


def test_create_webcamera_stream():
    camera = WebCamera(Stream(0))

    with camera.stream as stream:
        i = 0
        while i < 100:
            stream.stream()
            i += 1
        assert stream.is_open

    assert not stream.is_open


# def test_detect_motion_in_stream():
#     camera = WebCamera(Stream(0))

#     with camera.stream as stream:
#         capture_motion(stream.stream())
#         assert stream.is_open


if __name__ == "__main__":
    pytest.main()
