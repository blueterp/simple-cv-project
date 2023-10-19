from time import sleep
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# fourcc = cv2.VideoWriter_fourcc(*"MJPG")
# out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
sleep(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # out.write(frame)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
