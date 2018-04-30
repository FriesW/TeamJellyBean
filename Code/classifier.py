import cv2
import numpy as np
import Viewer.GlobalServer as GS
import Util
import UtilTF

cam = cv2.VideoCapture(0)
if not cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920):
    raise Exception('Camera error: can\'t set width.')
if not cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080):
    raise Exception('Camera error: can\'t set height.')

v_orig = GS.new_view('Image')
e_cycle = GS.new_event('Single')
b_freerun = GS.new_bool('Freerun')

rate = Util.Timer(' per frame')
expo_1 = Util.Exposure('Exposure general', hidden=True)
expo_2 = Util.Exposure('Exposure tray')
init_crop = Util.Crop('Initial', 150, 85, 1620, 910, True, False)
tray_finder = Util.FindTray('Tray', True)
bean_slicer = Util.BeanSlicer('Beans', True)

v_out = GS.new_view('Classified')
classify = UtilTF.Classifier()

calibrate_btn = GS.new_event('Calibrate bean slicer')
calibrate_btn.set_hidden(True)

while True:
    
    rate.cycle()
    while not b_freerun.get() and not e_cycle.get():
        e_cycle.await_remote(0.2)
    if b_freerun.get():
        e_cycle.set(0)
    
    rv = False
    while not rv:
        rv, img = cam.read()
    expo_1.measure(img)
    img = init_crop.crop(img)
    v_orig.update(img)
    success, img = tray_finder.find(img)
    if success:
        expo_2.measure(img)
        if calibrate_btn.get():
            bean_slicer.calibrate(img)
        else:
            sliced = bean_slicer.slice(img)
            for i in sliced:
                label = classify.classify(i[1])
                p = list(i[0])
                p[1] += 30
                cv2.putText(img, label, tuple(p), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            v_out.update(img)
                
    
