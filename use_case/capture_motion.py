from time import time
from time import sleep
from datetime import datetime as dt
import cv2
from collections import deque
from video_writer.video_writer import VideoWriter
from video_source.stream import Stream
from detectors.motion_detection import detect_motion, draw_contours


class Queue:
    def __init__(self, max_length):
        self.queue = deque()
        self.max_length = max_length

    def __iter__(self):
        yield from list(self.queue)

    def enque(self, item):
        if len(self.queue) > self.max_length:
            self.queue.popleft()
        self.queue.append(item)

    def clear_queue(self):
        self.queue = deque()

    def dequeue(self):
        if len(self.queue) > 0:
            self.queue.popleft()


def capture_motion(stream: Stream, video_writer: VideoWriter) -> str:
    with stream:
        queue = Queue(max_length=60)
        start_time = time()
        _, frame0 = stream.stream()
        ret1, frame1 = stream.stream()

        while True:
            if not ret1:
                print("Stream has ended")
                break

            contours = detect_motion(frame0, frame1)
            if contours:
                start_time = time()
                frame0 = draw_contours(frame0, contours)

                if not video_writer.is_open():
                    file_name = dt.now().strftime("%Y%m%d_%H:%M:%S")
                    print(f"Opening {file_name} to write")
                    video_writer.open(file_name=f"{file_name}.avi", buffer=queue)

                video_writer.write(frame0)
                cv2.imshow("frame", frame0)
                if cv2.waitKey(50) == ord("q"):
                    break
            elif start_time + 5 > time() and video_writer.is_open():
                video_writer.write(frame0)
                cv2.imshow("frame", frame0)
                if cv2.waitKey(50) == ord("q"):
                    break
            else:
                if video_writer.is_open():
                    print(f"Closing {file_name}")
                    cv2.destroyAllWindows()
                    video_writer.release()
            queue.enque(frame0)
            frame0 = frame1
            ret1, frame1 = stream.stream()

        if video_writer.is_open():
            print(f"Closing {file_name}")

            cv2.destroyAllWindows()
            video_writer.release()

        return
