from nicegui import app
class EventBus:
    def __init__(self):
        self.listeners = {}
    
    def on(self, event, callback):
        self.listeners.setdefault(event, []).append(callback)
    
    def emit(self, event, *args, **kwargs):
        for cb in self.listeners.get(event, []):
            cb(*args, **kwargs)
    
    def kill_listener(self, event, cb):
        for cb in self.listeners.get(event, []):
            self.listeners[event].remove(cb)
    
    def reset(self):
        for event in self.listeners:
            for cb in self.listeners[event]:
                self.listeners[event].remove(cb)

event_bus = EventBus()

@app.on_shutdown
async def end_bus():
    global event_bus
    event_bus.reset()
    event_bus = None