import pytest
from video_source import FakeBooleanStream
from detectors.fake_boolean_detector import FakeBooleanDetector
from video_source.stream_exceptions import StreamClosedError


def test_create_detector_with_no_stream():
    with pytest.raises(ValueError):
        detector = FakeBooleanDetector(None)


def test_create_detector_with_incorrect_object_for_stream():
    with pytest.raises(ValueError):
        detector = FakeBooleanDetector("my_fake_stream")


def test_create_detector_with_boolean_stream():
    stream = FakeBooleanStream([True, True])
    detector = FakeBooleanDetector(stream)

    assert detector.stream == stream


def test_detect_frame_when_stream_closed():
    stream = FakeBooleanStream([True, True])
    detector = FakeBooleanDetector(stream)

    with pytest.raises(StreamClosedError):
        detector.stream_frames()


def test_detect_frame_when_using_context_manager():
    stream = FakeBooleanStream([True, True])
    detector = FakeBooleanDetector(stream)

    with detector:
        ret = detector.stream_frames()

    assert ret
    assert not detector.stream.is_open


def test_get_active_frame_when_frame_streams_successfully():
    stream = FakeBooleanStream([True, True])
    detector = FakeBooleanDetector(stream)

    with detector:
        ret = detector.stream_frames()

    assert detector.get_active_frame() == True


def test_get_active_frame_is_none_if_stream_closes():
    stream = FakeBooleanStream([True, True])
    detector = FakeBooleanDetector(stream)

    with detector:
        ret = detector.stream_frames()
        ret = detector.stream_frames()
        ret = detector.stream_frames()

    assert detector.get_active_frame() is None


@pytest.mark.parametrize("frames, detection", [([True], True), ([False], False)])
def test_detector_returns_correct_detection(frames, detection):
    stream = FakeBooleanStream(frames)
    detector = FakeBooleanDetector(stream)

    with detector:
        ret = detector.stream_frames()

    assert detector.detects_contours() == detection


@pytest.mark.parametrize("frames, detection", [([True], True), ([False], False)])
def test_detect_call_detects_contour(frames, detection):
    stream = FakeBooleanStream(frames)
    detector = FakeBooleanDetector(stream)

    with detector:
        detector.detect()
    assert detector.detects_contours() == detection


if __name__ == "__main__":
    pytest.main()
