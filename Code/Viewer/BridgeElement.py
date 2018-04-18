from abc import ABC, abstractmethod
import uuid

class BridgeElement(ABC):
    
    @abstractmethod
    def __init__(self, name, listener, hidden = False):
        self.__name = name
        self.__id = 'obj_' + uuid.uuid4().hex
        self.__listener = listener
        self.__is_frozen = False
        self.__is_hidden = hidden
        self.announce()
    
    @abstractmethod
    def announce(self):
        self._notify_listener({
          'name':self.get_name(),
          'hidden':self.is_hidden()
        })
    
    def get_id(self):
        return self.__id
        
    def get_name(self):
        return self.__name
    
    @abstractmethod
    def notify(self, data):
        pass
        #self._on_notify( data )
    
    #@abstractmethod
    #def _on_notify(self, data):
    #    pass
    
    def _notify_listener(self, data):
        self.__listener({self.get_id() : data})
    
    @abstractmethod
    def set_frozen(self, status):
        self.__is_frozen = status
    
    def is_frozen(self):
        return self.__is_frozen
    
    def set_hidden(self, status):
        self.__is_hidden = status
        self._notify_listener({'hidden':self.is_hidden()})
    
    def is_hidden(self):
        return self.__is_hidden