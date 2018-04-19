from ViewServer import ViewServer

__server = ViewServer()

def new_view(name, *args, **kwargs):
    return __server.new_view(name, *args, **kwargs)

def new_int(name, *args, **kwargs):
    return __server.new_int(name, *args, **kwargs)

def new_float(name, *args, **kwargs):
    return __server.new_float(name, *args, **kwargs)

def new_string(name, *args, **kwargs):
    return __server.new_string(name, *args, **kwargs)
    
def new_event(name, *args, **kwargs):
    return __server.new_event(name, *args, **kwargs)

def new_bool(name, *args, **kwargs):
    return __server.new_bool(name, *args, **kwargs)