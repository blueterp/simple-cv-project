import pytest
import os
from utils.stream_buffer import StreamBuffer
from video_writer.fake_video_writer import FakeVideoWriter
from video_source import FakeBooleanStream
from detectors.fake_boolean_detector import FakeBooleanDetector
from use_case.monitor_stream import MonitorStream
from time import sleep, time


def make_frames(fps, lead_dead_time, motion_time, trailing_dead_time, cycles):
    """
    helper function for creating the number of frames which are equivalent to a streaming
    video in seconds.
    """
    lead = [False] * lead_dead_time * fps
    detection = [True] * motion_time * fps
    trailing = [False] * trailing_dead_time * fps

    chunk = lead + detection + trailing
    return chunk * cycles


def test_create_monitor_stream_use_case():
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(writer)
    assert monitor.stream_writer == writer


def test_close_monitor_resources():
    stream = FakeBooleanStream([True])
    detector = FakeBooleanDetector(stream)
    writer = FakeVideoWriter()
    monitor = MonitorStream(writer)

    monitor.stream_writer.open("fake_video.avi")

    monitor.close_open_resources()
    assert not monitor.stream_writer.is_open()


@pytest.mark.parametrize(
    "seconds_to_record, wait_time, expected_result",
    [
        (3, 5, True),
        (3, 1, False),
    ],
)
def test_timer_is_expired(seconds_to_record, wait_time, expected_result):
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=seconds_to_record,
    )

    sleep(wait_time)
    assert monitor.timer_is_expired() == expected_result


def test_reset_monitor_writer():
    writer = FakeVideoWriter()
    monitor = MonitorStream(writer, detection=True, timer_started=True)

    monitor.stream_writer.open(include_timestamp=True)
    monitor.reset_monitor_writer()

    assert (
        not monitor.detection
        and not monitor.timer_started
        and not monitor.stream_writer.is_open()
    )


def test_engage_recording_when_not_already_recording():
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(
        writer,
        detection=False,
    )

    monitor.engage_recording()

    assert monitor.detection == True


def test_engage_recording_when_already_recording():
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(writer, timer_started=True, detection=True)

    monitor.engage_recording()

    assert monitor.timer_started == False


def test_is_recording_when_detection():
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(writer, timer_started=True, detection=True)

    assert monitor.is_recording()


def test_is_recording_when_no_detection():
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(writer, timer_started=True, detection=False)

    assert not monitor.is_recording()


def test_start_timer():
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(writer, timer_started=False, detection=False)

    monitor.start_timer()
    assert monitor.timer_started == True


@pytest.mark.parametrize("sleep_time, expired", [(0.1, True), (0.3, False)])
def test_check_timer_expired(sleep_time, expired):
    stream = FakeBooleanStream([True])
    writer = FakeVideoWriter()
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=0.25,
    )
    monitor.engage_recording()
    monitor.timer_started = True
    sleep(sleep_time)
    monitor.check_timer()
    assert monitor.timer_started == expired


def test_process_detection_frame_no_detection_not_recording():
    stream = FakeBooleanStream([False])
    detector = FakeBooleanDetector(stream)
    writer = FakeVideoWriter()
    buffer = StreamBuffer(1)
    monitor = MonitorStream(
        writer,
        detection=False,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=0.25,
    )
    with detector:
        # print(detector.stream.is_open)
        while detector.stream_frames():
            monitor.process_detection_frame(detector, buffer)

    assert not monitor.is_recording()
    assert writer.memory == []
    assert len(buffer.queue) == 1


def test_process_detection_frame_has_detection_not_recording():
    stream = FakeBooleanStream([True])
    detector = FakeBooleanDetector(stream)
    writer = FakeVideoWriter()
    buffer = StreamBuffer(1)
    monitor = MonitorStream(
        writer,
        detection=False,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=0.25,
    )
    with detector:
        while detector.stream_frames():
            monitor.process_detection_frame(detector, buffer)

    assert monitor.is_recording()
    assert writer.memory == [True]
    assert len(buffer.queue) == 1


def test_process_detection_frame_captures_no_detection_following_detection():
    stream = FakeBooleanStream([True, False])
    detector = FakeBooleanDetector(stream)
    writer = FakeVideoWriter()
    buffer = StreamBuffer(1)
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=1,
    )
    with detector:
        while detector.stream_frames():
            monitor.process_detection_frame(detector, buffer)

    assert monitor.is_recording()
    assert writer.memory == [True, False]
    assert len(buffer.queue) == 2


def test_process_detection_frame_does_not_capture_frame_after_timeout():
    stream = FakeBooleanStream([True, False, False])
    detector = FakeBooleanDetector(stream)
    writer = FakeVideoWriter()
    buffer = StreamBuffer(1)
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=0.75,
    )
    with detector:
        while detector.stream_frames():
            monitor.process_detection_frame(detector, buffer)
            sleep(1)

    assert not monitor.is_recording()
    assert writer.memory == []
    assert len(buffer.queue) == 2


def test_monitor_stream_no_detections(tmp_path):
    stream = FakeBooleanStream([False, False, False])
    detector = FakeBooleanDetector(stream)
    writer = FakeVideoWriter(directory=tmp_path)
    buffer = StreamBuffer(1)
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=0.75,
    )

    monitor.monitor(detector, leading_buffer_seconds=1)
    print(os.listdir(tmp_path))
    assert len(os.listdir(tmp_path)) == 0


def test_monitor_stream_single_detection(tmp_path):
    frames = make_frames(20, 1, 1, 1, 1)
    stream = FakeBooleanStream(frames)
    detector = FakeBooleanDetector(stream, show_stream=True)
    writer = FakeVideoWriter(directory=tmp_path)
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=1,
    )

    monitor.monitor(detector, leading_buffer_seconds=1)
    print(os.listdir(tmp_path))
    assert len(os.listdir(tmp_path)) == 1


def test_monitor_stream_two_detection(tmp_path):
    frames = make_frames(20, 1, 1, 2, 2)
    print(frames)
    stream = FakeBooleanStream(frames)
    detector = FakeBooleanDetector(stream, show_stream=True)
    writer = FakeVideoWriter(directory=tmp_path)
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=1,
    )

    monitor.monitor(detector, leading_buffer_seconds=1)
    print(os.listdir(tmp_path))
    assert len(os.listdir(tmp_path)) == 2


def test_monitor_stream_one_detection(tmp_path):
    frame_set_1 = make_frames(20, 1, 1, 0, 1)
    frame_set_2 = make_frames(20, 1, 1, 0, 1)
    frames = frame_set_1 + frame_set_2
    print(frames)
    stream = FakeBooleanStream(frames)
    detector = FakeBooleanDetector(stream, show_stream=True)
    writer = FakeVideoWriter(directory=tmp_path)
    monitor = MonitorStream(
        writer,
        detection_stopped_time=time(),
        seconds_to_record_after_detection=3,
    )

    monitor.monitor(detector, leading_buffer_seconds=1)
    print(os.listdir(tmp_path))
    assert len(os.listdir(tmp_path)) == 1


if __name__ == "__main__":
    pytest.main()
