from abc import ABC, abstractmethod
from BridgeElement import BridgeElement
import threading

class Parameter(BridgeElement, ABC):

    @abstractmethod
    def __init__(self, name, listener, initial, editable = True):
        self.__val = initial
        self.__editable = editable
        self.__await = threading.Event()
        super(Parameter, self).__init__(name, listener)
        self.set(initial)
    
    def announce(self):
        super(Parameter, self).announce()
        self._notify_listener({
          'input_type' : self._get_input_type(),
          'input_value' : self.get(),
          'editable' : self.is_editable()
        })
    
    @abstractmethod
    def _get_input_type(self):
        pass
    
    def _get_type(self):
        return 'parameter'
    
    def notify(self, data):
        if 'input_value' in data:
            if self.is_editable():
                self.set(data['input_value'])
            else:
                self.announce()
        self.__await.set()
        self.__await.clear()
    
    def await_remote(self, timeout = None):
        rv = self.__await.wait(timeout)
        self.__await.clear()
        return rv
    
    def set_editable(self, status):
        self.__editable = status
        self._notify_listener({ 'editable' : self.is_editable() })
    
    def is_editable(self):
        return self.__editable
        #return True
        
    @abstractmethod
    def _validator(self, input):
        return (False, None)
        
    def get(self):
        return self.__val
    
    def set(self, new_val):
        accept = False
        try: accept, new_val = self._validator(new_val)
        except: pass
        if(accept):
            self.__val = new_val
        self._notify_listener({ 'input_value' : self.__val })
        return accept
    
    
    #Don't have time for this functionality
    def set_frozen(self, status):
        pass