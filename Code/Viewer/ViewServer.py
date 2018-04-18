from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from View import View
import threading
import _thread
import json
import traceback

class ViewServer:
    
    def __init__(self, port = 8000):
        self.__lock = threading.Lock()
        self._bridges = {}
        self._client = None
        self.__server = SimpleWebSocketServer('', port, self.__make_handler__())
        _thread.start_new_thread(self.__run__, ())
    
    def __run__(self):
        self.__server.serveforever()
    
    def new_view(self, name):
        name = str(name)
        nv = View(name, self.__send_message__)
        self._bridges[nv.get_id()] = nv
        return nv

    def __send_message__(self, message):
        if self._client != None:
            self._client.sendMessage(json.dumps(message))
    
    def __make_handler__(parent):
        class Handler(WebSocket):
            
            def handleConnected(self):
                print("Connected")
                if parent._client != None:
                        parent._client.close()
                parent._client = self
                for b in parent._bridges:
                    parent._bridges[b].announce()
                
            def handleClose(self):
                if parent._client == self:
                    parent._client = None
                print("Disconnect")
            
            def handleMessage(self):
                data = json.loads(self.data)
                for obj_id, values in data.items():
                    if obj_id in parent._bridges:
                        parent._bridges[obj_id].notify(values)
            
        return Handler
