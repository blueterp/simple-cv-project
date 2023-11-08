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
            time.time() - self.detection_stopped_time
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
            if self.timer_is_expired:
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
            self.stream_writer.write(detector.get_active_frame())

        buffer.add_frame(detector.get_active_frame())

    def close_open_resources(self):
        if self.stream_writer.is_open():
            self.stream_writer.release()
        cv.destroyAllWindows()

    def monitor_detector(
        self,
        detector: Detector,
        show_stream: bool = True,
        leading_buffer_seconds: int = 5,
    ) -> None:
        stream_buffer = StreamBuffer(max_length=leading_buffer_seconds * 20)
        with detector:
            while detector.stream_frames():
                self.process_detection_frame(detector, stream_buffer)
        self.close_open_resources()

        with detector:
            while detector.stream_frames():
                self.process_detection_frame(detector, stream_buffer)
        self.close_open_resources()


# def capture_motion(stream: Stream, video_writer: VideoWriter) -> str:
#     with stream:
#         queue = Queue(max_length=60)
#         start_time = time()
#         _, frame0 = stream.stream()
#         ret1, frame1 = stream.stream()

#         while True:
#             if not ret1:
#                 print("Stream has ended")
#                 break

#             contours = detect_motion(frame0, frame1)
#             if contours:
#                 start_time = time()
#                 frame0 = draw_contours(frame0, contours)

#                 if not video_writer.is_open():
#                     file_name = dt.now().strftime("%Y%m%d_%H:%M:%S")
#                     print(f"Opening {file_name} to write")
#                     video_writer.open(file_name=f"{file_name}.avi", buffer=queue)

#                 video_writer.write(frame0)
#                 cv.imshow("frame", frame0)
#                 if cv.waitKey(50) == ord("q"):
#                     break
#             elif start_time + 5 > time() and video_writer.is_open():
#                 video_writer.write(frame0)
#                 cv.imshow("frame", frame0)
#                 if cv.waitKey(50) == ord("q"):
#                     break
#             else:
#                 if video_writer.is_open():
#                     print(f"Closing {file_name}")
#                     cv.destroyAllWindows()
#                     video_writer.release()
#             queue.enque(frame0)
#             frame0 = frame1
#             ret1, frame1 = stream.stream()

#         if video_writer.is_open():
#             print(f"Closing {file_name}")

#             cv.destroyAllWindows()
#             video_writer.release()

#         return
