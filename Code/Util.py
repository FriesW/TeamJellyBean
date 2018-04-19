import cv2
import numpy as np
import Viewer.GlobalServer as GS



class Crop:
    def __init__(self, name, x=0, y=0, w=100, h=100, hidden=False, editable=True):
        self.__name = name
        self.__x = GS.new_int(name+' crop X', min=0, initial=x)
        self.__x.set_hidden(hidden)
        self.__x.set_editable(editable)
        self.__w = GS.new_int(name+' crop width', min=1, initial=w)
        self.__w.set_hidden(hidden)
        self.__w.set_editable(editable)
        self.__y = GS.new_int(name+' crop Y', min=0, initial=y)
        self.__y.set_hidden(hidden)
        self.__y.set_editable(editable)
        self.__h = GS.new_int(name+' crop height', min=1, initial=h)
        self.__h.set_hidden(hidden)
        self.__h.set_editable(editable)
        self.__view = GS.new_view(name+' crop')
        self.__view.set_hidden(hidden)
    
    def crop(self, img):
        x = self.__x.get()
        y = self.__y.get()
        w = self.__w.get()
        h = self.__h.get()
        crop = img[y:y+h, x:x+w]
        self.__view.update(crop)
        return crop



class FindTray:
    def __init__(self, name, hidden=False, editable=True):
        
        self.__hw_proportion = 5.33/6.62
        self.__out_w = int(1500)
        self.__out_h = int( self.__out_w * self.__hw_proportion )
        
        self.__v_process = GS.new_view(name+': Pre-processed')
        self.__v_process.set_hidden(hidden)
        self.__v_thres = GS.new_view(name+': Threshold')
        self.__v_thres.set_hidden(hidden)
        self.__v_morph = GS.new_view(name+': Threshold morphology')
        self.__v_morph.set_hidden(hidden)
        self.__v_contours = GS.new_view(name+': Contours')
        self.__v_contours.set_hidden(hidden)
        self.__v_warp = GS.new_view(name+': Cutout tray')
        
        self.__blur = GS.new_int(name+': Blur', min=-1, max=100, initial=-1, step=2)
        self.__blur.set_hidden(hidden)
        self.__blur.set_editable(editable)
        self.__t_lvl = GS.new_int(name+': Threshold', min=0, max=255, initial=70)
        self.__t_lvl.set_hidden(hidden)
        self.__t_lvl.set_editable(editable)
        self.__c_approx = GS.new_float(name+': Contour approximation level', min=0, initial=10)
        self.__c_approx.set_hidden(hidden)
        self.__c_approx.set_editable(editable)
    
    def find(self, img):
        orig = img.copy()
        
        #Preprocess
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.__blur.get() != -1:
            img = cv2.GaussianBlur(img, (self.__blur.get(),self.__blur.get()), 0)
        self.__v_process.update(img)
        
        #Threshold image
        rv, img = cv2.threshold(img, self.__t_lvl.get(), 255, cv2.THRESH_BINARY)
        self.__v_thres.update(img)
        
        #Fill gaps
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_RECT, (11,11)))
        self.__v_morph.update(img)
        
        #Find contours / edges
        img, contours, hierarchy = \
            cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_img = orig.copy()
        cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
        
        #Failure if no contours
        if len(contours) == 0:
            return (False, None)
        
        #Find largest area contour
        candidate_contour = contours[0]
        for c in contours[1:]:
            if cv2.contourArea(candidate_contour) < cv2.contourArea(c):
                candidate_contour = c
        
        #Approximate contour
        approx = cv2.approxPolyDP(candidate_contour, self.__c_approx.get(), True)
        #Draw it
        cv2.drawContours(contour_img, [approx], -1, (255, 0, 0), 3)
        for p in approx:
            cv2.circle(contour_img, (p[0][0], p[0][1]), 8, (0, 0, 255), -1)
        
        #Show all contours
        self.__v_contours.update(contour_img)
        
        #Build new edge array, sorta hackish
        corners = []
        for p in approx:
            corners.append([float(p[0][0]), float(p[0][1])])
        
        #Failure if not 4 points
        if len(corners) != 4:
            return (False, None)
        
        #Find minimal rotation
        min_i = 0
        min_d = 100000
        for i in range(len(corners)):
            p = corners[i]
            d = ( p[0]**2 + p[1]**2 ) ** 0.5
            if d < min_d:
                min_i = i
                min_d = d
        #Rotate
        offset = 3
        slice = (min_i + offset) % len(corners)
        corners = corners[slice:] + corners[:slice]
        
        #Convert edge array
        corners = np.asarray(corners, np.float32)
        
        #Make output
        dest_size = np.array([ [0,0],[self.__out_w,0],[self.__out_w,self.__out_h],[0,self.__out_h] ],np.float32)
        transform = cv2.getPerspectiveTransform(corners, dest_size)
        img = cv2.warpPerspective(orig, transform, (self.__out_w,self.__out_h))
        img = cv2.flip(img, 1)
        self.__v_warp.update(img)
        
        return (True, img)
        