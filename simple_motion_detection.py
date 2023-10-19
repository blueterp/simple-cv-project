from time import sleep
import numpy as np
import cv2

# for web camera
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

cap = cv2.VideoCapture("vtest.avi")

if cap.isOpened():
    _, frame1 = cap.read()
    _, frame2 = cap.read()
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame1,
            f"Status: Movement",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3,
        )
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    cv2.imshow("frame", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    if cv2.waitKey(17) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()


# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
# # fourcc = cv2.VideoWriter_fourcc(*"XVID")
# # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
# # out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
# sleep(1)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     # out.write(frame)
#     cv2.imshow("frame", frame)
#     if cv2.waitKey(1) == ord("q"):
#         break
# cap.release()
# cv2.destroyAllWindows()
