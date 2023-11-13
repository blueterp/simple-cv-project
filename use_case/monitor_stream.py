from time import time
from datetime import datetime as dt
import cv2 as cv
from utils.stream_buffer import StreamBuffer
from detectors.detector_interface import Detector
from video_source.video_source_interface import VideoSource
from video_writer.video_writer_interface import VideoWriterInterface


class MonitorStream:
    def __init__(
        self,
        stream_writer: VideoWriterInterface,
        detection: bool = False,
        detection_stopped_time=None,
        timer_started: bool = False,
        seconds_to_record_after_detection: int = 5,
    ):
        self.stream_writer = stream_writer
        self.detection = detection
        self.detection_stopped_time = detection_stopped_time
        self.timer_started = timer_started
        self.seconds_to_record_after_detection = seconds_to_record_after_detection

    def timer_is_expired(self):
        return (
            time() - self.detection_stopped_time
            >= self.seconds_to_record_after_detection
        )

    def reset_monitor_writer(self):
        self.detection = False
        self.timer_started = False
        self.stream_writer.release()

    def engage_recording(self, stream_buffer=None):
        if self.is_recording():
            self.timer_started = False
        else:
            self.detection = True
            self.stream_writer.open(buffer=stream_buffer, include_timestamp=True)
            print("Started Recording!")

    def is_recording(self):
        return self.detection

    def start_timer(self):
        self.timer_started = True
        self.detection_stopped_time = time()

    def check_timer(self):
        if self.timer_started:
            if self.timer_is_expired():
                self.reset_monitor_writer()
                print("Stop Recording!")
        else:
            self.start_timer()

    def process_detection_frame(self, detector, buffer):
        if detector.detects_contours():
            self.engage_recording(buffer)
        elif self.is_recording():
            self.check_timer()

        if self.is_recording():
            detector.show_frame()
            self.stream_writer.write(detector.get_active_frame())

        buffer.add_frame(detector.get_active_frame())

    def close_open_resources(self):
        if self.stream_writer.is_open():
            self.stream_writer.release()
        cv.destroyAllWindows()

    def monitor(
        self,
        detector: Detector,
        leading_buffer_seconds: int = 1,
    ) -> None:
        stream_buffer = StreamBuffer(max_length=leading_buffer_seconds * 20)
        with detector:
            while detector.stream_frames():
                self.process_detection_frame(detector, stream_buffer)
        self.close_open_resources()
