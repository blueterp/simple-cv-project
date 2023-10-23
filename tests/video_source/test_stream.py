import pytest
import os
from video_source.stream import Stream


def test_instantiate_stream_with_no_source():
    with pytest.raises(TypeError) as e:
        stream = Stream()


@pytest.mark.parametrize(
    "source_info", [10, "btest.avi"], ids=["webcamera", "sample_video"]
)
def test_fail_to_instantiate_stream_with_invalid_sources(source_info):
    with pytest.raises(TypeError):
        stream = Stream(source_info)


def test_successfully_instantiate_stream_with_valid_video_source(data_directory):
    test_video = os.path.join(data_directory, "vtest.avi")
    stream = Stream(test_video)


def test_raises_exception_if_stream_called_without_context_manager(data_directory):
    test_video = os.path.join(data_directory, "vtest.avi")
    stream = Stream(test_video)
    with pytest.raises(AttributeError):
        stream.stream()


def test_successfully_stream_frame(data_directory):
    test_video = os.path.join(data_directory, "vtest.avi")
    stream = Stream(test_video)
    with stream:
        ret, frame = stream.stream(show=False)

    assert ret


if __name__ == "__main__":
    pytest.main()
