import pytest
import cv2 as cv
import os

from detectors.motion_detection import detect_motion, draw_contours


@pytest.fixture
def frame1(data_directory):
    return cv.imread(os.path.join(data_directory, "frame1.png"))


@pytest.fixture
def frame2(data_directory):
    return cv.imread(os.path.join(data_directory, "frame2.png"))


def test_no_motion_detected(frame1):
    is_motion = detect_motion(frame1, frame1)
    assert not is_motion


def test_detects_motion(frame1, frame2):
    contours = detect_motion(frame1, frame2)
    assert contours


def test_draw_contours(frame1, frame2, data_directory):
    drawn_contours_ground_truth = cv.imread(
        (os.path.join(data_directory, "contours_ground_truth.png"))
    )
    contours = detect_motion(frame1, frame2)
    drawn_contours = draw_contours(frame1, contours)

    assert (drawn_contours == (drawn_contours_ground_truth)).all()


def test_draw_no_contours_no_motion_detected(frame1, frame2):
    contours = detect_motion(frame1, frame2)

    drawn_contours = draw_contours(frame1, contours)

    assert (drawn_contours == (frame1)).all()


if __name__ == "__main__":
    pytest.main()
