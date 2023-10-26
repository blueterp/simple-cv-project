import pytest
import numpy as np
import os
import cv2 as cv
from video_writer.video_writer import VideoWriter

# test writing when writer is closed
# test written frames were what was specified


@pytest.fixture
def frames(data_directory):
    frame1 = cv.imread(os.path.join(data_directory, "frame1.png"))
    frame2 = cv.imread(os.path.join(data_directory, "frame2.png"))
    return (frame1, frame2)


@pytest.fixture
def frame_size(frames):
    frame, _ = frames

    return (frame.shape[0], frame.shape[1])


def test_write_video_when_writer_closed(frames, frame_size, tmp_path):
    frame1, _ = frames
    height, width = frame_size
    writer = VideoWriter(
        width,
        height,
        file_name=os.path.join(tmp_path, "test_save.avi"),
    )
    with pytest.raises(AttributeError):
        writer.write(frame1)


def test_write_video(tmp_path, frames, frame_size):
    frame1, frame2 = frames
    height, width = frame_size
    writer = VideoWriter(
        width,
        height,
        file_name=os.path.join(tmp_path, "test_save.avi"),
        include_timestamp=False,
    )

    with writer:
        writer.write(frame1)
        writer.write(frame2)
    assert os.path.isfile(os.path.join(tmp_path, "test_save.avi"))


def test_write_with_buffer(frames, frame_size, tmp_path):
    buffer = []
    frame1, frame2 = frames
    width, height = frame_size
    for i in range(100):
        buffer.append(frame2)
    writer = VideoWriter(
        height,
        width,
        file_name=os.path.join(tmp_path, "test_save_buffer.avi"),
        include_timestamp=False,
    )
    with writer:
        writer.write(frame1)
        writer.write(frame2)

    assert os.path.isfile(os.path.join(tmp_path, "test_save_buffer.avi"))


if __name__ == "__main__":
    pytest.main()
