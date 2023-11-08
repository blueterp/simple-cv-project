import pytest
import os
from video_writer.fake_video_writer import FakeVideoWriter
from video_source.fake_stream import FakeStream
from detectors.fake_detector import FakeDetector
from use_case.monitor_stream import MonitorStream


# def test_no_motion_detected(tmp_path):
#     # writer = FakeWriter()
#     # stream = FakeStream()
#     assert len(os.listdir(tmp_path)) == 0


def make_frames(fps, lead_dead_time, motion_time, trailing_dead_time, cycles):
    lead = [False] * lead_dead_time * fps
    detection = [True] * motion_time * fps
    trailing = [False] * trailing_dead_time * fps

    chunk = lead + detection + trailing
    return chunk * cycles


def test_single_detection_observed(tmp_path):
    frames = make_frames(20, 6, 2, 0, 1)
    writer = FakeVideoWriter()
    stream = FakeStream(frames, 0, 0)
    detector = FakeDetector(stream)
    monitor = MonitorStream(writer)

    monitor.monitor_detector(detector=detector)

    assert len(os.listdir(tmp_path)) == 1


if __name__ == "__main__":
    pytest.main()
