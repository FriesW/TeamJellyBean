import traceback
import cv2

def freerun(cam):
    while True:
        rv, img = cam.read()
        if not rv:
            print("Camera read error")
            break
        size = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('Freerun', size)
        if cv2.waitKey(1) != -1:
            break
    cv2.destroyAllWindows()

try:
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    freerun(cam)
    cam.release()
except Exception as e:
    traceback.print_exc()

input("Done")