import pytest
from video_writer.fake_video_writer import FakeVideoWriter
import cv2 as cv
import os
import numpy as np


@pytest.fixture
def frames(data_directory):
    frame1 = cv.imread(os.path.join(data_directory, "frame1.png"))
    frame2 = cv.imread(os.path.join(data_directory, "frame2.png"))
    return (frame1, frame2)


def test_initialize_fake_writer():
    writer = FakeVideoWriter()
    assert writer.frames is False


def test_raises_error_when_writer_not_open(frames):
    writer = FakeVideoWriter()
    frame, _ = frames
    with pytest.raises(AttributeError):
        writer.write(frame)


def test_writes_successfully_when_writer_is_open(frames, tmp_path):
    writer = FakeVideoWriter()
    frame, _ = frames
    writer.open(file_name=os.path.join(tmp_path, "fake.avi"))
    writer.write(frame)
    writer.release()
    assert os.path.isfile(os.path.join(tmp_path, "fake.avi"))


def test_writer_using_context_manager(frames, tmp_path):
    writer = FakeVideoWriter()
    frame, _ = frames
    with writer(file_name=os.path.join(tmp_path, "fake.avi")):
        writer.write(frame)

    assert os.path.isfile(os.path.join(tmp_path, "fake.avi"))


if __name__ == "__main__":
    pytest.main()
