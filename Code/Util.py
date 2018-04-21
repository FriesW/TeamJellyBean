import cv2
import numpy as np
import Viewer.GlobalServer as GS
import os
import re
import time

def p_dist(x1, y1, x2, y2):
    return ( (x1-x2)**2 + (y1-y2)**2 ) ** 0.5

def crop(img, x, y, w, h):
    return img[y:y+h, x:x+w]

def save(path, img):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
        break
    max_num = 0
    for f in files:
        s = re.findall('\d+\.png$', f)
        if s:
            max_num = max(max_num, int(s[0][:-4]))
    path = os.path.join(path, str(max_num+1).zfill(5)+'.png' )
    print('Saving image:', path)
    cv2.imwrite(path, img)



class Timer:
    def __init__(self, name='Timer', hidden=False):
        self.__l = GS.new_int('ms '+name)
        self.__l.set_hidden(hidden)
        self.__l.set_editable(False)
        self.__lt = time.time()
    
    def cycle(self):
        tt = time.time()
        self.__l.set(int( (tt - self.__lt) * 1000 ))
        self.__lt = tt



class Crop:
    def __init__(self, name='Crop', x=0, y=0, w=100, h=100, hidden=False, editable=True):
        self.__name = name
        self.__x = GS.new_int(name+': crop X', min=0, initial=x)
        self.__x.set_hidden(hidden)
        self.__x.set_editable(editable)
        self.__w = GS.new_int(name+': crop width', min=1, initial=w)
        self.__w.set_hidden(hidden)
        self.__w.set_editable(editable)
        self.__y = GS.new_int(name+': crop Y', min=0, initial=y)
        self.__y.set_hidden(hidden)
        self.__y.set_editable(editable)
        self.__h = GS.new_int(name+': crop height', min=1, initial=h)
        self.__h.set_hidden(hidden)
        self.__h.set_editable(editable)
        self.__view = GS.new_view(name+': crop')
        self.__view.set_hidden(hidden)
    
    def crop(self, img):
        x = self.__x.get()
        y = self.__y.get()
        w = self.__w.get()
        h = self.__h.get()
        out = crop(img, x, y, w, h)
        self.__view.update(out)
        return out



class FindTray:
    def __init__(self, name='FindTray', hidden=False, editable=True):
        
        #Changing these numbers may break BeanSlicer
        self.__hw_proportion = 5.33/6.62
        self.__out_w = int(1500)
        self.__out_h = int( self.__out_w * self.__hw_proportion )
        
        self.__v_process = GS.new_view(name+': pre-processed')
        self.__v_process.set_hidden(hidden)
        self.__v_thres = GS.new_view(name+': threshold')
        self.__v_thres.set_hidden(hidden)
        self.__v_morph = GS.new_view(name+': threshold morphology')
        self.__v_morph.set_hidden(hidden)
        self.__v_contours = GS.new_view(name+': contours')
        self.__v_contours.set_hidden(hidden)
        self.__v_warp = GS.new_view(name+': cutout tray')
        
        self.__blur = GS.new_int(name+': blur', min=-1, max=100, initial=-1, step=2)
        self.__blur.set_hidden(hidden)
        self.__blur.set_editable(editable)
        self.__t_lvl = GS.new_int(name+': threshold', min=0, max=255, initial=70)
        self.__t_lvl.set_hidden(hidden)
        self.__t_lvl.set_editable(editable)
        self.__c_approx = GS.new_float(name+': contour approximation level', min=0, initial=10)
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
            d = p_dist(p[0], p[1], 0, 0)
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



class BeanSlicer:
    def __init__(self, name='BeanSlicer', hidden=False, editable=True):
        self.__name = name
        self.__canny = GS.new_view(name+': canny')
        self.__canny.set_hidden(hidden)
        self.__morph = GS.new_view(name+': morphology')
        self.__morph.set_hidden(hidden)
        self.__pass_1 = GS.new_view(name+': pass one, contour')
        self.__pass_1.set_hidden(hidden)
        self.__pass_2 = GS.new_view(name+': pass two, contour')
        self.__pass_2.set_hidden(hidden)
        self.__fin = GS.new_view(name+': discovered')
        self.__fin.set_hidden(False)
        self.__res = GS.new_view(name+': result')
        self.__res.set_hidden(False)
        
        self.__blur = GS.new_int(name+': blur', initial=45, min=-1, max=100, step=2)
        self.__blur.set_hidden(hidden)
        self.__blur.set_editable(editable)
        self.__canny_l = GS.new_int(name+': canny low', initial=0, min=0, max=255)
        self.__canny_l.set_hidden(hidden)
        self.__canny_l.set_editable(editable)
        self.__canny_h = GS.new_int(name+': canny high', initial=35, min=0, max=255)
        self.__canny_h.set_hidden(hidden)
        self.__canny_h.set_editable(editable)
        self.__morph_size = GS.new_int(name+': morph amount', initial=15, min=1, step=2)
        self.__morph_size.set_hidden(hidden)
        self.__morph_size.set_editable(editable)
        self.__pass_1_width = GS.new_int(name+': pass one width', initial=40, min=1)
        self.__pass_1_width.set_hidden(hidden)
        self.__pass_1_width.set_editable(editable)
        self.__cutoff_distance = GS.new_float(name+': center cutoff distance', initial=15, min=0)
        self.__cutoff_distance.set_hidden(hidden)
        self.__cutoff_distance.set_editable(editable)
        self.__cutoff_area = GS.new_float(name+': cutoff area', initial=450, min=0)
        self.__cutoff_area.set_hidden(hidden)
        self.__cutoff_area.set_editable(editable)
        self.__bean_w = GS.new_int(name+': slice width', initial=150, min=0)
        self.__bean_w.set_hidden(hidden)
        self.__bean_w.set_editable(False)
        self.__bean_h = GS.new_int(name+': slice height' ,initial=110, min=0)
        self.__bean_h.set_hidden(hidden)
        self.__bean_h.set_editable(False)
        
        #Dependent on input image size!
        self.__CENTERS = [(145,1101),(488,1098),(317,1099),(659,1097),(1001,1097),(829,1096),(1343,1094),(1173,1094),(230,979),(914,977),(573,978),(1086,975),(744,977),(401,978),(1255,974),(143,860),(486,858),(658,858),(313,858),(1171,856),(1000,856),(1341,855),(828,857),(571,739),(400,739),(228,739),(1084,736),(912,737),(742,738),(1254,735),(314,620),(143,621),(827,617),(998,615),(657,618),(1169,615),(485,618),(1339,614),(227,500),(740,498),(910,496),(570,498),(398,498),(1082,496),(1254,495),(315,381),(485,379),(142,380),(995,377),(825,378),(655,378),(1337,374),(1167,376),(226,261),(738,259),(399,260),(568,258),(1251,255),(1080,255),(909,256),(141,140),(311,140),(823,138),(653,138),(482,138),(1336,134),(1166,136),(994,136)]
    
    def slice(self, img):
        orig = img.copy()
        
        if self.__blur.get() != -1:
            img = cv2.GaussianBlur(img, (self.__blur.get(),self.__blur.get()), 0)
        
        img = cv2.Canny(img, self.__canny_l.get(), self.__canny_h.get())
        self.__canny.update(img)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.__morph_size.get(),self.__morph_size.get()))
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        self.__morph.update(img)
        
        #Pass 1
        img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        img.fill(0)
        cv2.drawContours(img, contours, -1, (255, 255, 255), self.__pass_1_width.get())
        self.__pass_1.update(img)
        #Pass 2
        img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        img.fill(0)
        cv2.drawContours(img, contours, -1, (255, 255, 255), 6)
        self.__pass_2.update(img)
        
        #Discard bad contours (no center)
        remove = []
        for i in range(len(contours)):
            m = cv2.moments(contours[i])
            if m['m00'] == 0.0:
                remove.append(i)
        contours = np.delete(contours, remove, 0)
        
        img = orig.copy()
        empty_spots = []
        
        #Show all contours
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
        #Build
        for c in contours:
            m = cv2.moments(c)
            cX = int(m["m10"] / m["m00"])
            cY = int(m["m01"] / m["m00"])
            color = (0, 0, 255)
            #Test distances
            d_cutoff = self.__cutoff_distance.get()
            a_cutoff = self.__cutoff_area.get() * 10
            for ref in self.__CENTERS:
                #Is on a center?
                if p_dist(cX, cY, ref[0], ref[1]) < d_cutoff:
                    #Is it a dot?
                    if cv2.contourArea(c) < a_cutoff:
                        #cv2.drawContours(img, [c], -1, (255, 0, 0), 3)
                        cv2.fillPoly(img, [c], (255,0,0))
                        empty_spots.append(ref)
                    else:
                        cv2.drawContours(img, [c], -1, (255, 255, 255), 3)
                        
            #Draw
            cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)
        
        #Draw calibration
        for ref in self.__CENTERS:
            cv2.circle(img, ref, 5, (75, 75, 75), -1)
        
        self.__fin.update(img)
        
        img = orig.copy()
        cropped = [] #[((x,y), IMG), ...]
        
        #Get bean locations
        beans = self.__CENTERS[:]
        beans = [p for p in beans if p not in empty_spots]
        
        w = self.__bean_w.get()
        h = self.__bean_h.get()
        for b in beans:
            x = b[0] - w//2
            y = b[1] - h//2
            cropped.append( ((x,y),crop(orig, x, y, w, h)) )
            cv2.rectangle(img, (x, y), (x+w, y+h), (50, 50, 50), 2)
        
        self.__res.update(img)
        
        return cropped
