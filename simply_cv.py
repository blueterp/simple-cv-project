from time import sleep
import numpy as np
import cv2

cap = cv2.VideoCapture("vtest.avi")
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)
print(size)
# fourcc = cv2.VideoWriter_fourcc(*"XVID")
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, size)
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
    out.write(frame)
    cv2.imshow("frame", frame)
    if cv2.waitKey(50) == ord("q"):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
