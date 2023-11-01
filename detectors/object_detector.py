from detectors.detector_interface import Detector
import random

import cv2 as cv
import numpy as np
from ultralytics import YOLO
from video_source.video_source_interface import VideoSource


class ObjectDetector(Detector):
    def __init__(
        self,
        video_source: VideoSource,
        model="models/yolov8n.pt",
        class_list="models/coco.txt",
        confidence=0.45,
        save=False,
    ) -> None:
        self.frame = None
        self.stream = video_source
        self.contours = []
        self.boxes = None
        self.class_list = self._get_classes_from_list(class_list)
        self.detection_colors = self._generate_detection_colors()
        self.model = YOLO(model)
        self.confidence = confidence
        self.save = save

    def _get_classes_from_list(self, class_list):
        with open(class_list, "r") as f:
            data = f.read().split("\n")
        return data

    def _generate_detection_colors(self):
        detection_colors = []
        for i in range(len(self.class_list)):
            r = i  # random.randint(0, 255)
            g = i  # random.randint(0, 255)
            b = i  # random.randint(0, 255)
            detection_colors.append((b, g, r))

        return detection_colors

    def stream_frames(self):
        ret, frame = self.stream.stream()
        self.frame = frame if ret else None
        if self.frame is None:
            print("No more frames to stream. Closing detector.")
        else:
            self.detect()
        return self.frame

    def detect(self):
        if self.frame is None:
            raise ValueError("No frame present. Cannot detect objects.")
        if not self.frame is None:
            self.contours = []

        detect_params = self.model.predict(
            source=[self.frame], conf=self.confidence, save=self.save
        )
        self.boxes = detect_params[0].boxes
        self.contours = detect_params[0].numpy()
        self._draw_contours()

        return self.contours

    def detects_contours(self):
        return len(self.contours) > 0

    def _draw_contours(self):
        if self.detects_contours():
            for i in range(len(self.contours)):
                box = self.boxes[i]  # returns one box
                clsID = box.cls.numpy()[0]
                conf = box.conf.numpy()[0]
                bb = box.xyxy.numpy()[0]

                cv.rectangle(
                    self.frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    self.detection_colors[int(clsID)],
                    3,
                )
                font = cv.FONT_HERSHEY_COMPLEX
                cv.putText(
                    self.frame,
                    self.class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )

    def get_active_frame(self):
        return self.frame
