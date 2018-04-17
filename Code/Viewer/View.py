from BridgeElement import BridgeElement
import threading
import numpy as np
import cv2
import base64

class View(BridgeElement):
    def __init__(self, name, listener, encoding = 'png', default_scale = 1.0, interpolation = cv2.INTER_LINEAR):
        super(View, self).__init__(name, listener)
        self.__encoding = encoding #'png', 'jpg'
        self.__scale = default_scale
        self.__interpolation = interpolation
        
        self.__lock = threading.Lock()
        self.__image = None
        self.__update_render = True
        self.__render_str = None
        
        self.__reset('! Unset View !')
    
    def announce(self):
        super(View, self).announce()
    
    def __reset(self, text = '! Reset View !'):
        image = np.zeros((72,455,3), np.uint8)
        cv2.putText(self.__image, text, (5, 55), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
        self.update(image, 1.0)
    
    def reset(self):
        self.__reset()
    
    def update(self, image, scale = None):
        self.__lock.acquire()
        self.__image = image.copy()
        self.__update_render = True
        self.__lock.release()
        if not self.is_frozen():
            self._notify_listener({'event':'update'})
        
    def _on_notify(self, data):
        if 'request' in data:
            self._notify_listener({
              'encoding': self.__encoding,
              'data': self.__render()
            })
    
    def set_frozen(self, status):
        super(View, self).set_frozen(status)
            
    def __render(self):
        #render if not initialized, or if update ready and not frozen
        if self.__render_str is None or (not self.is_frozen() and self.__update_render):
            self.__lock.acquire()
            tmp_image = self.__image.copy()
            self.__update_render = False
            self.__lock.release()
            scale = self.__scale
            if scale != 1.0:
                tmp_image = cv2.resize(tmp_image, None,
                                       fx = self.__scale, fy = self.__scale,
                                       interpolation = self.__interpolation)
            
            self.__render_str = base64.b64encode(
                                  cv2.imencode('.'+self.__encoding, tmp_image)[1].tostring()
                                ).decode('utf-8')
        
        return self.__render_str
    
    def set_default_scale(self, new_scale):
        self.__scale = new_scale
    
    #cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_AREA
    def _set_interpolation(self, new_inter):
        self.interpolation = new_inter
