from time import time
from datetime import datetime as dt
import cv2 as cv
from utils.stream_buffer import StreamBuffer
from detectors.detector_interface import Detector
from video_source.video_source_interface import VideoSource
from video_writer.video_writer_interface import VideoWriterInterface

def monitor_stream(stream:VideoSource, detector:Detector, stream_writer:VideoWriterInterface, show_stream:bool=True, leading_buffer_seconds:int)->None:
    detection = False
    detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 5

    with stream as s:
        stream_buffer = StreamBuffer(max_length=leading_buffer_seconds*20)

        while True:
            detector.stream_frames(s)

            if detector.get_active_frame() is None:
                print("No frames to stream. Closing stream down.")
                break

            detector.detect()

            if detector.detects_contours():
                if detection:
                    timer_started = False
                else:
                    detection = True
                    stream_writer.open(buffer=stream_buffer, include_timestamp=True)
                    print("Started Recording!")
            elif detection:
                if timer_started:
                    if (
                        time.time() - detection_stopped_time
                        >= SECONDS_TO_RECORD_AFTER_DETECTION
                    ):
                        detection = False
                        timer_started = False
                        stream_writer.release()
                        print("Stop Recording!")
                else:
                    timer_started = True
                    detection_stopped_time = time()

            if detection:
                # leading_frame = detector.draw_contours(leading_frame, contours)
                stream_writer.write(detector.get_active_frame())

            stream_buffer.enque(detector.get_active_frame())

        if stream_writer.is_open():
            stream_writer.release()

    cv.destroyAllWindows()


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
