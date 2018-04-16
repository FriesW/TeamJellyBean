import threading
import numpy as np
import cv2
import base64

class View:
    def __init__(self, encoding = 'png', default_scale = 1.0, interpolation = cv2.INTER_LINEAR):
        self.encoding = encoding
        self.def_scale = default_scale
        self.interpolation = interpolation
        
        self.lock = threading.Lock()
        self.image = np.zeros((72,455,3), np.uint8)
        cv2.putText(self.image, '! Unset View !', (5, 55), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
        self.rendered = None
        
        self.get_render()
    
    def update(self, image, scale = None):
        if not scale:
            scale = self.def_scale
        self.lock.acquire()
        self.image = image.copy()
        if scale != 1.0:
            self.image = \
             cv2.resize(self.image, None, fx=scale, fy=scale, interpolation = self.interpolation)
        self.rendered = None
        self.lock.release()
    
    #'png', 'jpg'
    def _set_encoding(self, new_enc):
        self.encoding = new_enc
    
    def _set_default_scale(self, new_scale):
        self.def_scale = new_scale
    
    #cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_AREA
    def _set_interpolation(self, new_inter):
        self.interpolation = new_inter
    
    def get_render(self):
        self.lock.acquire()
        if not self.rendered:
            self.rendered = str.encode('data:image/'+self.encoding+';base64,') + \
             base64.b64encode(cv2.imencode('.'+self.encoding, self.image)[1].tostring())
        out = self.rendered
        self.lock.release()
        return out