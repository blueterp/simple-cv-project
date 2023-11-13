import pytest
import os
from video_source import Stream
import cv2 as cv


@pytest.fixture
def sample_video(data_directory):
    return os.path.join(data_directory, "vtest.avi")


@pytest.fixture
def stream(sample_video):
    stream = Stream(sample_video)
    yield stream
    stream.close()


def test_instantiate_stream_with_no_source():
    with pytest.raises(TypeError) as e:
        stream = Stream()


@pytest.mark.parametrize(
    "source_info", [10, "btest.avi"], ids=["webcamera", "sample_video"]
)
def test_fail_to_instantiate_stream_with_invalid_sources(source_info):
    """
    parameterized values are invalid, either because the file does not
    exist or the camera index is out of bounds.
    """
    with pytest.raises(TypeError):
        stream = Stream(source_info)


def test_stream_is_closed_if_open_not_called(stream):
    assert not stream.is_open


def test_open_stream_with_valid_video_source(stream):
    stream.open()
    assert stream.is_open


def test_can_close_stream_if_stream_not_opened(stream):
    stream.close()
    assert not stream.is_open


def test_can_close_stream_if_stream_opened(stream):
    stream.open()
    stream.close()
    assert not stream.is_open


def test_successfully_instantiate_stream_with_valid_video_source(stream, sample_video):
    cap = cv.VideoCapture(sample_video)
    gt_width, gt_height = (
        int(cap.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5),
        int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5),
    )
    assert stream.width == gt_width and stream.height == gt_height


def test_raises_exception_if_stream_called_when_closed(stream):
    with pytest.raises(AttributeError):
        stream.stream()


def test_successfully_stream_frame(stream):
    with stream:
        ret, _ = stream.stream(show=False)
    assert ret


@pytest.mark.skip
def test_create_stream_from_webcamera():
    """
    index 0 is the default index for the webcamera on the computer
    """
    webcamera_idx = 0
    stream = Stream(webcamera_idx)

    with stream:
        ret, _ = stream.stream(show=False)

    assert ret


if __name__ == "__main__":
    pytest.main()
