import pytest
from video_source import FakeBooleanStream
from video_source.stream_exceptions import StreamClosedError


@pytest.fixture
def true_frames():
    return [True, True]


@pytest.fixture(name="stream")
def boolean_stream(true_frames):
    return FakeBooleanStream(true_frames)


def test_create_boolean_stream_with_no_frames():
    boolean_frames = []
    with pytest.raises(ValueError):
        stream = FakeBooleanStream(boolean_frames)


def test_create_boolean_stream(stream, true_frames):
    assert stream.frames == true_frames


def test_create_boolean_stream_has_width_height_0(stream):
    assert stream.width == 0 and stream.height == 0


def test_stream_frame_when_closed_fails(stream):
    with pytest.raises(StreamClosedError):
        _, _ = stream.stream()


def test_stream_frame_when_open(stream):
    stream.open()
    ret, bool = stream.stream()

    assert ret


def test_stream_frame_when_after_closing_fails(stream):
    stream.open()
    stream.close()
    with pytest.raises(StreamClosedError):
        _, _ = stream.stream()


def test_stream_closes_when_all_frames_have_been_streamed(stream):
    stream.open()
    _, _ = stream.stream()
    _, _ = stream.stream()
    ret, bool = stream.stream()

    assert not ret and not stream.is_open


def test_stream_using_context_manager(stream):
    with stream:
        ret, bool = stream.stream()

    assert ret


def test_stream_using_context_manager_closes_when_done(stream):
    with stream:
        ret, bool = stream.stream()

    assert not stream.is_open


if __name__ == "__main__":
    pytest.main()
