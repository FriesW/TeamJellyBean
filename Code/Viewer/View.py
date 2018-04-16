import threading
import numpy as np
import cv2
import base64

class View:
    def __init__(self):
        self.lock = threading.Lock()
        self.image = np.zeros((100,100,3), np.uint8)
        self.rendered = None
        
    def update(self, image):
        self.lock.acquire()
        self.image = image.copy()
        self.rendered = None
        self.lock.release()
    
    def get_render(self):
        self.lock.acquire()
        if not self.rendered:
            self.rendered = base64.b64encode(cv2.imencode('.png', self.image)[1].tostring())
        out = self.rendered
        self.lock.release()
        return out