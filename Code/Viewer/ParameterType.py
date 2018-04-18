from Parameter import Parameter

class Integer(Parameter):
    def __init__(self, name, listener, initial = 0, min = None, max = None, step = 1):
        self.__val = initial
        self.__min = min
        self.__max = max
        self.__step = step
        super(Integer, self).__init__(name, listener)
    
    def set(self, nn):
        self.__val = nn
    
    def get(self):
        return self.__val
    
    def announce(self):
        super(Integer, self).announce()
        self._notify_listener({'input_type':'number'})
        self._notify_listener({'input_value':self.__val})
        if self.__min: self._notify_listener({'min':self.__min})
        if self.__max: self._notify_listener({'max':self.__max})
        if self.__step: self._notify_listener({'step':self.__step})
    
    def notify(self, data):
        if 'value' in data:
            self.__val = int(data['value'])
            super(Integer, self).notify(None)
    
    def set_frozen(self, status):
        pass