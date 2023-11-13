import pytest
from video_source import FakeBooleanStream
from video_source.stream_exceptions import StreamClosedError


def test_create_boolean_stream_with_no_frames():
    boolean_frames = []
    with pytest.raises(ValueError):
        stream = FakeBooleanStream(boolean_frames)


def test_create_boolean_stream():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)
    assert stream.frames == boolean_frames


def test_create_boolean_stream_has_width_height_0():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)

    assert stream.width == 0 and stream.height == 0


def test_stream_frame_when_closed_fails():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)
    with pytest.raises(StreamClosedError):
        _, _ = stream.stream()


def test_stream_frame_when_open():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)
    stream.open()
    ret, bool = stream.stream()

    assert ret


def test_stream_frame_when_after_closing_fails():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)
    stream.open()
    stream.close()
    with pytest.raises(StreamClosedError):
        _, _ = stream.stream()


def test_stream_closes_when_all_frames_have_been_streamed():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)
    stream.open()
    _, _ = stream.stream()
    ret, bool = stream.stream()

    assert not stream.is_open


def test_stream_using_context_manager():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)
    with stream:
        ret, bool = stream.stream()

    assert ret


def test_stream_using_context_manager_closes_when_done():
    boolean_frames = [True]
    stream = FakeBooleanStream(boolean_frames)
    with stream:
        ret, bool = stream.stream()

    assert not stream.is_open


if __name__ == "__main__":
    pytest.main()
