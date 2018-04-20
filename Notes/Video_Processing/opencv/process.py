import cv2

def show(pic, name = 'showing...'):
    cv2.imshow(name, pic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
for i in range(4): #First few are bad...
    rv, orig_img = cam.read()
cam.release()

#show(orig_img, "original")

#gray_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
gray_img = orig_img
#show(gray_img, "gray")

blur_img = cv2.GaussianBlur(gray_img, (25,25), 0)
show(blur_img, "blur")

edge_img = cv2.Canny(blur_img, 30, 50)
show(edge_img, "canny edge")

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
close_img = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)
show(close_img, "morphology close")

cont_img, contours, hierarchy = cv2.findContours(close_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
act_contour_img = orig_img.copy()
cv2.drawContours(act_contour_img, contours, -1, (0, 255, 0), 3)
show(act_contour_img, "actual contours")

#https://docs.opencv.org/3.4.0/dd/d49/tutorial_py_contour_features.html
for c in contours:
    m = cv2.moments(c)
    if m["m00"] != 0.0:
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
        cv2.circle(act_contour_img, (cX, cY), 5, (255, 0, 255), -1)
show(act_contour_img, "actual contours w/ centers")

#approx_contour_img = orig_img.copy()
#for c in contours:
#    peri = cv2.arcLength(c, True)
#    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#    cv2.drawContours(approx_contour_img, [approx], -1, (0, 255, 0), 3)
#show(approx_contour_img, "approximate contours")


import numpy as np

blank_img = np.zeros((1080,1920,3), np.uint8)
cv2.drawContours(blank_img, contours, -1, (0, 255, 0), 7)
show(blank_img, "just actual contours")

#edge_img = cv2.Canny(blank_img, 100, 255)
thres, edge_img = cv2.threshold( cv2.cvtColor(blank_img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
show(edge_img, "edges of actual contours")

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
close_img = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)
show(close_img, "morphology close")

cont_img, contours, hierarchy = cv2.findContours(close_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
act_contour_img = orig_img.copy()
cv2.drawContours(act_contour_img, contours, -1, (0, 255, 0), 3)
show(act_contour_img, "actual contours of contours")

#https://docs.opencv.org/3.4.0/dd/d49/tutorial_py_contour_features.html
for c in contours:
    m = cv2.moments(c)
    if m["m00"] != 0.0:
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
        cv2.circle(act_contour_img, (cX, cY), 3, (255, 0, 255), -1)
show(act_contour_img, "centers")
