import cv2
import numpy as np
import Viewer.GlobalServer as GS
import Util

cam = cv2.VideoCapture(0)
if not cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920):
    raise Exception('Camera error: can\'t set width.')
if not cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080):
    raise Exception('Camera error: can\'t set height.')

v_orig = GS.new_view('Image')
e_cycle = GS.new_event('Single')
b_freerun = GS.new_bool('Freerun')

rate = Util.Timer(' per frame')
init_crop = Util.Crop('Initial', 150, 85, 1620, 910, True, False)
tray_finder = Util.FindTray('Tray', True)
bean_slicer = Util.BeanSlicer('Beans', True)

while True:
    
    rate.cycle()
    while not b_freerun.get() and not e_cycle.get():
        e_cycle.await_remote(0.2)
    if b_freerun.get():
        e_cycle.set(0)
    
    rv = False
    while not rv:
        rv, img = cam.read()

    img = init_crop.crop(img)
    v_orig.update(img)
    success, img = tray_finder.find(img)
    if success:
        for i in bean_slicer.slice(img):
    #        Util.save('imgs', i[1])
            pass
    
