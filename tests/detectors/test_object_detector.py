import pytest
import numpy as np
from detectors.object_detector import ObjectDetector
from video_source.fake_stream import FakeStream
import cv2 as cv
import os


@pytest.fixture
def stream(frames):
    return FakeStream(frames)


def test_create_object_detector(stream):
    detector = ObjectDetector(stream)
    assert detector.stream == stream
    assert detector.frame == None
    assert detector.contours == []


def test_stream_frames(stream, frames):
    detector = ObjectDetector(stream)
    with stream:
        detector.stream_frames()
    assert np.array_equal(detector.frame, frames[0])


def test_stream_frames_when_no_more_frames_available(stream, frames):
    detector = ObjectDetector(stream)
    with stream:
        stream.stream()
        stream.stream()
        detector.stream_frames()
    assert detector.frame == None


def test_detect_object_blank_frame(frames):
    frames[0][:] = 0
    stream = FakeStream([frames[0]])

    detector = ObjectDetector(stream)
    with stream:
        detector.stream_frames()
        detector.detect()

    assert len(detector.contours) == 0


def test_detect_object_objects_in_frame(frames):
    stream = FakeStream([frames[0]])

    detector = ObjectDetector(stream)
    with stream:
        detector.stream_frames()
        detector.detect()
    assert len(detector.contours) > 0


def test_detects_contours_correctly_identifies_when_contours_present(frames):
    frames[0][:] = 0
    stream = FakeStream(frames)
    detector = ObjectDetector(stream)
    with stream:
        detector.stream_frames()
        detector.detect()
        assert not detector.detects_contours()

        detector.stream_frames()
        detector.detect()
        assert detector.detects_contours()


def test_get_active_frame_when_no_frames_left(stream):
    detector = ObjectDetector(stream)

    with stream:
        detector.stream_frames()
        detector.stream_frames()
        detector.stream_frames()

    assert detector.get_active_frame() is None


def test_get_active_frame_when_frame_present(stream, frames):
    detector = ObjectDetector(stream)

    with stream:
        detector.stream_frames()

    assert np.array_equal(detector.get_active_frame(), (frames[0]))


def test_draw_frames_no_contours_detected(frames):
    frames[0][:] = 0
    stream = FakeStream([frames[0]])

    detector = ObjectDetector(stream)
    with stream:
        detector.stream_frames()
        detector.detect()
        detector._draw_contours()

    assert np.array_equal(detector.frame, frames[0])


def test_draw_frames_contours_detected(stream, data_directory, frames):
    drawn_objects = cv.imread(os.path.join(data_directory, "frame1_drawn_objects.png"))
    detector = ObjectDetector(stream)
    with stream:
        detector.stream_frames()
        detector.detect()
        detector._draw_contours()

    assert np.array_equal(drawn_objects, frames[0])


if __name__ == "__main__":
    pytest.main()
