import socket
from functools import wraps
from django.http import HttpRequest, HttpResponseForbidden

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except:
        return "127.0.0.1"
    finally:
        s.close()
        
def superuser_requierd(func):
    @wraps(func)
    def __inner(request: HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        
        return HttpResponseForbidden()
    
    return __inner