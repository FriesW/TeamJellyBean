import cv2
import Viewer.GlobalServer as GS

cam = cv2.VideoCapture(0)
if not cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920):
    raise Exception('Camera error: can\'t set width.')
if not cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080):
    raise Exception('Camera error: can\'t set height.')

v = GS.new_view('Raw camera')
crop_x = GS.new_int('Crop X', min = 0, initial = 150)
crop_x.set_hidden(True)
crop_x.set_editable(False)
crop_w = GS.new_int('Crop width', min = 1, initial = 1620)
crop_w.set_hidden(True)
crop_w.set_editable(False)
crop_y = GS.new_int('Crop Y', min = 0, initial = 85)
crop_y.set_hidden(True)
crop_y.set_editable(False)
crop_h = GS.new_int('Crop height', min = 1, initial = 910)
crop_h.set_hidden(True)
crop_h.set_editable(False)

while True:
    
    rv = False
    while not rv:
        rv, img = cam.read()
    
    x = crop_x.get()
    y = crop_y.get()
    w = crop_w.get()
    h = crop_h.get()
    crop = img[y:y+h, x:x+w]
    v.update(crop)
    