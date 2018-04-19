import cv2
import numpy as np
import Viewer.GlobalServer as GS

cam = cv2.VideoCapture(0)
if not cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920):
    raise Exception('Camera error: can\'t set width.')
if not cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080):
    raise Exception('Camera error: can\'t set height.')

e_cycle = GS.new_event('Single')
b_freerun = GS.new_bool('Freerun')

v_raw = GS.new_view('Cropped raw')
v_grey = GS.new_view('Greyscale')
v_thres = GS.new_view('Threshold')
v_thres_morph = GS.new_view('Threshold morphology')
v_contours = GS.new_view('Contours')
v_warp = GS.new_view('Cutout tray')

crop_x = GS.new_int('Crop X', min=0, initial=150)
crop_x.set_hidden(True)
crop_x.set_editable(False)
crop_w = GS.new_int('Crop width', min=1, initial=1620)
crop_w.set_hidden(True)
crop_w.set_editable(False)
crop_y = GS.new_int('Crop Y', min=0, initial=85)
crop_y.set_hidden(True)
crop_y.set_editable(False)
crop_h = GS.new_int('Crop height', min=1, initial=910)
crop_h.set_hidden(True)
crop_h.set_editable(False)

thres_lvl = GS.new_int('Threshold', min=0, max=255, initial=70)

approx_contor_thres = GS.new_float('Contour approximation threshold', min=0, initial=10)

while True:
    
    if not b_freerun.get():
        e_cycle.await_remote()
    
    rv = False
    while not rv:
        rv, i_raw = cam.read()
    
    x = crop_x.get()
    y = crop_y.get()
    w = crop_w.get()
    h = crop_h.get()
    i_crop = i_raw[y:y+h, x:x+w]
    v_raw.update(i_crop)
    
    i_grey = cv2.cvtColor(i_crop, cv2.COLOR_BGR2GRAY)
    v_grey.update(i_grey)
    
    rv, i_thres = cv2.threshold(i_grey, thres_lvl.get(), 255, cv2.THRESH_BINARY)
    v_thres.update(i_thres)
    i_thres_morph = cv2.morphologyEx(i_thres, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, (11,11)))
    v_thres_morph.update(i_thres_morph)
    
    tray_corners = []
    
    discard, contours, hierarchy = \
        cv2.findContours(i_thres_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    i_contours = i_crop.copy()
    cv2.drawContours(i_contours, contours, -1, (0, 255, 0), 2)
    if len(contours):
        #Get largest contour
        tray_contour = contours[0]
        for c in contours[1:]:
            if cv2.contourArea(tray_contour) < cv2.contourArea(c):
                tray_contour = c
        #Approximate it
        approx = cv2.approxPolyDP(tray_contour, approx_contor_thres.get(), True)
        #Draw it
        cv2.drawContours(i_contours, [approx], -1, (255, 0, 0), 3)
        for n in approx:
            cv2.circle(i_contours, (n[0][0], n[0][1]), 8, (0, 0, 255), -1)
            tray_corners.append([float(n[0][0]), float(n[0][1])])
    v_contours.update(i_contours)
    
    if len(tray_corners) == 4:
        tray_corners = np.asarray(tray_corners, np.float32)
        dest_size = np.array([ [0,0],[1449,0],[1449,1449],[0,1449] ],np.float32)
        transform = cv2.getPerspectiveTransform(tray_corners, dest_size)
        i_warp = cv2.warpPerspective(i_crop, transform, (1450,1450))
        v_warp.update(i_warp)
