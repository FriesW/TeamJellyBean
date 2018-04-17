from abc import ABC, abstractmethod
from BridgeElement import BridgeElement

class Parameter(BridgeElement, ABC):

    @abstractmethod
    def __init__(self, name, listener, editable = True):
        super(Parameter, self).__init__(name, listener)
        self.__editable = editable
    
    @abstractmethod
    def announce(self):
        super(View, self).announce()
        self._notify_listener({'editable':self.is_editable()})
    
    @abstractmethod
    def __get_js(self):
        pass
    
    def set_editable(self, status):
        self.__editable = status
        self.__notify_listener({'editable':self.is_editable()})
    
    def is_editable(self):
        return self.__editable