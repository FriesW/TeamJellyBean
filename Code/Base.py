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

init_crop = Util.Crop('Initial', 150, 85, 1620, 910, True, False)
tray_finder = Util.FindTray('Tray')

while True:
    
    if not b_freerun.get():
        e_cycle.await_remote()
    
    rv = False
    while not rv:
        rv, img = cam.read()

    img = init_crop.crop(img)
    v_orig.update(img)
    img = tray_finder.find(img)
    