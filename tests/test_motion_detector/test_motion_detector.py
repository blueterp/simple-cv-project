import pytest
import cv2 as cv
import os

from detectors.motion_detection import detect_motion, draw_contours

file_path = os.path.dirname(os.path.abspath(__file__))


def test_detects_motion():
    frame1 = cv.imread(os.path.join(file_path, "frame1.png"))
    frame2 = cv.imread(os.path.join(file_path, "frame1.png"))
    is_motion = detect_motion(frame1, frame2)
    assert not is_motion


def test_detects_motion():
    frame1 = cv.imread(os.path.join(file_path, "frame1.png"))
    frame2 = cv.imread(os.path.join(file_path, "frame2.png"))
    contours = detect_motion(frame1, frame2)
    assert contours


def test_draw_contours():
    frame1 = cv.imread(os.path.join(file_path, "frame1.png"))
    frame2 = cv.imread(os.path.join(file_path, "frame2.png"))
    drawn_contours_ground_truth = cv.imread(
        (os.path.join(file_path, "contours_ground_truth.png"))
    )
    contours = detect_motion(frame1, frame2)

    drawn_contours = draw_contours(frame1, contours)
    print(drawn_contours)

    assert (drawn_contours == (drawn_contours_ground_truth)).all()


if __name__ == "__main__":
    pytest.main()
