import pytest
import numpy as np
import os
import cv2 as cv
from video_writer.video_writer import VideoWriter


def test_write_video(tmp_path, data_directory):
    frame = cv.imread(os.path.join(data_directory, "frame1.png"))
    frame2 = cv.imread(os.path.join(data_directory, "frame2.png"))
    writer = VideoWriter(os.path.join(tmp_path, "test_save.avi"))

    with writer:
        writer.write(frame)
        writer.write(frame2)

    assert os.path.isfile(os.path.join(tmp_path, "test_save.avi"))


if __name__ == "__main__":
    pytest.main()
