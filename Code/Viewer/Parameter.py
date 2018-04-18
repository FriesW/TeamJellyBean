from abc import ABC, abstractmethod
from BridgeElement import BridgeElement
import threading

class Parameter(BridgeElement, ABC):

    @abstractmethod
    def __init__(self, name, listener, editable = True):
        self.__editable = editable
        self.__await = threading.Event()
        super(Parameter, self).__init__(name, listener)
    
    @abstractmethod
    def announce(self):
        super(Parameter, self).announce()
        self._notify_listener({'editable':self.is_editable()})
    
    def _get_type(self):
        return 'parameter'
    
    @abstractmethod
    def notify(self, data):
        self.__await.set()
        self.__await.clear()
    
    def await_remote(self, timeout = None):
        rv = self.__await.wait(timeout)
        self.__await.clear()
        return rv
    
    def set_editable(self, status):
        self.__editable = status
        self._notify_listener({'editable':self.is_editable()})
    
    def is_editable(self):
        return self.__editable
        #return True
    
