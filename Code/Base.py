import cv2
import Viewer.GlobalServer as GS

cam = cv2.VideoCapture(0)
if not cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920):
    raise Exception('Camera error: can\'t set width.')
if not cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080):
    raise Exception('Camera error: can\'t set height.')

v_raw = GS.new_view('Cropped raw')
v_grey = GS.new_view('Greyscale')
v_thres = GS.new_view('Threshold')
v_thres_morph = GS.new_view('Threshold morphology')

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

while True:
    
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
