from Parameter import Parameter
import re

class Integer(Parameter):
    def __init__(self, name, listener, initial = 0, min = None, max = None, step = 1):
        if step == None or step == 0:
            step = 1
        start = 0
        if min != None:
            start = min
        if max != None:
            max = max - ( (max - start) % step )
        self.__min = min
        self.__max = max
        self.__step = step
        super(Integer, self).__init__(name, listener, initial)
    
    def _get_input_type(self):
        return 'number';
    
    def _validator(self, input):
        input = int(float(input))
        
        step_offset = 0
        if self.__min != None:
            step_offset = self.__min
        if self.__step and (input - step_offset) % self.__step != 0:
            leftover = abs(input - step_offset) % self.__step
            if input > self.get():
                input = input + self.__step - leftover
            else:
                input = input - leftover
        
        if self.__max != None:
            input = min(input, self.__max)
        if self.__min != None:
            input = max(input, self.__min)
        
        return (True, input)


class Float(Parameter):
    def __init__(self, name, listener, initial = 0, min = None, max = None):
        self.__min = min
        self.__max = max
        super(Float, self).__init__(name, listener, initial)
        
    def _get_input_type(self):
        return 'number';
    
    def _validator(self, input):
        input = float(input)
        if self.__max != None:
            input = min(input, self.__max)
        if self.__min != None:
            input = max(input, self.__min)
        return (True, input)


class String(Parameter):
    def __init__(self, name, listener, initial = '', pattern_remove = None, pattern_accept = None):
        self.__remove = pattern_remove
        self.__accept = pattern_accept
        super(String, self).__init__(name, listener, initial)
    
    def _get_input_type(self):
        return 'text';
    
    def _validator(self, input):
        input = str(input)
        if self.__remove:
            input = re.sub(self.__remove, '', input)
        status = True
        if self.__accept:
            status = bool( re.fullmatch(self.__accept, input) ) #or maybe re.search
        return (status, input)
