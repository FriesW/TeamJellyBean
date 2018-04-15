from View import View
import threading
import _thread
from http.server import HTTPServer, BaseHTTPRequestHandler

class ViewServer:
    def __init__(self, port = 8000):
        self.lock = threading.Lock()
        self.views = {}
        server_address = ('', port)
        self.httpd = HTTPServer(server_address, self.__make_handler__())
        _thread.start_new_thread(self.__run__, ())
    
    def __run__(self):
        self.httpd.serve_forever()
    
    def new_view(self, name):
        name = str(name)
        if name == '':
            raise Exception("Name cannot be empty.")
        if '\n' in name:
            raise Exception("No newlines in name.")
        new_v = View()
        self.lock.acquire()
        if name in self.views:
            self.lock.release()
            raise Exception("View name cannot be reused.")
        self.views[name] = new_v
        self.lock.release()
        return new_v

    
    def __make_handler__(parent):
        class Handler(BaseHTTPRequestHandler):
            
            def _h(self, good = True):
                if good:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                else:
                    self.send_response(403)
                    self.end_headers()

            def _out(self, string):
                if not isinstance(string, bytes):
                    if not isinstance(string, str):
                        string = str(string)
                    string = string.encode('utf-8')
                self.wfile.write(string)
            
            def do_GET(self):
                #Get keys
                parent.lock.acquire()
                keys = list(parent.views.keys())
                parent.lock.release()
                path = self.path[1:]
                #Listing
                if path == '':
                    self._h()
                    self._out('\n'.join(keys))
                #A particular key
                elif path in keys:
                    self._h()
                    parent.lock.acquire()
                    out = parent.views[path].get_render()
                    parent.lock.release()
                    self._out(out)
                #Bad path
                else:
                    self._h(False)
            
            def log_message(self, format, *args): return
            
        return Handler
