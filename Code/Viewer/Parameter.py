from abc import ABC, abstractmethod
from BridgeElement import BridgeElement
import threading

class Parameter(BridgeElement, ABC):

    @abstractmethod
    def __init__(self, name, listener, editable = True):
        super(Parameter, self).__init__(name, listener)
        self.__editable = editable
        self.__await_lock = threading.Lock()
        self.__await_lock_lock = threading.Lock()
    
    @abstractmethod
    def announce(self):
        super(View, self).announce()
        self._notify_listener({'editable':self.is_editable()})
    
    def _get_type(self):
        return 'parameter';
    
    @abstractmethod
    def notify(self, data):
        self.__await_lock_lock.acquire()
        if self.__await_lock.locked():
            self.__await_lock.release()
        self.__await_lock_lock.release()
    
    @abstractmethod
    def _get_type(self):
        pass
    
    def set_editable(self, status):
        self.__editable = status
        self.__notify_listener({'editable':self.is_editable()})
    
    def is_editable(self):
        return self.__editable
    
    def await_remote(self):
        self.__await_lock.acquire()