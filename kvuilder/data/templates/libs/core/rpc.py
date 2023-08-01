from oscpy.client import send_message
from oscpy.server import OSCThreadServer


class API(object):
    
    def __init__(self, objects: dict = {}, callback: object = object, port: int = 3000, bind_to: str = '127.0.0.1'):
        self._objects = objects
        self.callback = callback
        server = OSCThreadServer()
        server.listen(bind_to, port=port, default=True)
        self.registered_agents = {}
        for root_path, obj in objects.items():
            for path, method in {x: getattr(obj, x) for x in obj.__dir__() if callable(getattr(obj, x))}.items():
                server.bind(bytes(f'/objects/{root_path}/{path}'.encode()), method)
        server.bind(b'/register', self.register_agent)
        server.bind(b'/emit', self.emit)
        server.bind(b'/callback', self.callback)
        server.bind(b'/reset', self.registered_agents.clear)
        self.server = server
    
    def register_agent(self, addr: tuple, description: str = ''):
        self.registered_agents[addr] = description
    
    def emit(self, *args, callback=b'/callback'):
        for addr, port in self.registered_agents.keys():
            send_message(osc_address=callback, values=args, ip_address=addr, port=port)
    
    def stop(self):
        self.server.stop_all()
    
    def __del__(self):
        self.stop()
