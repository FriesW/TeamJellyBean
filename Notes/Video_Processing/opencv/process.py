import cv2

def show(pic):
    cv2.imshow('showing...', pic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
for i in range(4): #First few are bad...
    rv, orig_img = cam.read()
cam.release()

#show(orig_img)

#gray_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
gray_img = orig_img
#show(gray_img)

blur_img = cv2.GaussianBlur(gray_img, (25,25), 0)
show(blur_img)

edge_img = cv2.Canny(blur_img, 30, 50)
show(edge_img)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
close_img = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)
show(close_img)

cont_img, contours, hierarchy = cv2.findContours(close_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
act_contour_img = orig_img.copy()
cv2.drawContours(act_contour_img, contours, -1, (0, 255, 0), 3)
show(act_contour_img)

#https://docs.opencv.org/3.4.0/dd/d49/tutorial_py_contour_features.html
for c in contours:
    m = cv2.moments(c)
    if m["m00"] != 0.0:
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
        cv2.circle(act_contour_img, (cX, cY), 7, (255, 0, 255), -1)
show(act_contour_img)

approx_contour_img = orig_img.copy()
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    cv2.drawContours(approx_contour_img, [approx], -1, (0, 255, 0), 3)
show(approx_contour_img)
