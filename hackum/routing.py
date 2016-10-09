from channels.routing import route
from channels.routing import include

from .apps.core import consumers as core
 
http_routing = [
    route('http.request', core.http_consumer)
]
 
stream_routing = [
 
]
 
channel_routing = {
    'websocket.connect': core.ws_connect,
    'websocket.receive': core.ws_receive,
    'websocket.disconnect': core.ws_disconnect
}