import os
import pytest
import cv2 as cv

test_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(test_dir, "test_data")


@pytest.fixture
def test_directory():
    return test_dir


@pytest.fixture
def data_directory():
    return data_dir


@pytest.fixture
def frames(data_directory):
    frame1 = cv.imread(os.path.join(data_directory, "frame1.png"))
    frame2 = cv.imread(os.path.join(data_directory, "frame2.png"))
    return (frame1, frame2)
