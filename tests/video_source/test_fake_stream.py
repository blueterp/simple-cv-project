import pytest
import cv2 as cv
import os
import numpy as np
from video_source.fake_stream import FakeStream


def get_frame_dimensions(frame):
    return frame.shape


@pytest.fixture
def frames(data_directory):
    frame1 = cv.imread(os.path.join(data_directory, "frame1.png"))
    frame2 = cv.imread(os.path.join(data_directory, "frame2.png"))
    return (frame1, frame2)


def test_create_fake_stream_non_matching_frames(frames):
    frame1, frame2 = frames
    width, height, _ = get_frame_dimensions(frame1)
    frame2 = cv.resize(frame2, (0, 0), fx=0.5, fy=0.5)
    modified_frames = [frame1, frame2]

    with pytest.raises(ValueError):
        stream = FakeStream(modified_frames)


def test_create_fake_stream(frames):
    frame1, frame2 = frames
    width, height = frame1.shape[0], frame1.shape[1]
    frames = [frame1, frame2]
    stream = FakeStream(frames)

    assert stream.frames == frames
    assert stream.width == width and stream.height == height


def test_stream_without_opening_stream(frames):
    stream = FakeStream(frames)

    with pytest.raises(TypeError):
        stream.stream()


def test_stream_after_opening_stream(frames):
    stream = FakeStream(frames)
    stream.open()
    ret, frame = stream.stream()
    assert ret and np.array_equal(frame, frames[0])


def test_stream_progressed_across_frames(frames):
    stream = FakeStream(frames)
    stream.open()

    ret1, frame1 = stream.stream()
    ret2, frame2 = stream.stream()
    ret3, frame3 = stream.stream()

    assert ret1 and ret2 and not ret3
    assert np.array_equal(frame1, frames[0]) and np.array_equal(frame2, frames[1])
    assert frame3 is None
    assert stream.frame_idx == 2


def test_stream_resets_when_closed(frames):
    stream = FakeStream(frames)
    stream.open()

    ret1, frame1 = stream.stream()
    ret2, frame2 = stream.stream()
    ret3, frame3 = stream.stream()

    stream.close()
    stream.open()
    ret4, frame4 = stream.stream()

    assert not ret3
    assert ret4


def test_stream_using_context_manager(frames):
    stream = FakeStream(frames)

    with stream:
        ret, frame = stream.stream()

    assert ret and np.array_equal(frame, frames[0])


if __name__ == "__main__":
    pytest.main()
