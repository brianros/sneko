

_list = []

class Peripheral:
    def __init__(self):
        if type(self) is Peripheral:
            raise TypeError("Peripheral cannot be instantiated directly")
        
        _list.append(self)
    
    def debug(self):
        raise NotImplementedError(f"Please override peripheral debug for: {type(self).__name__}")
    
    def reset(self):
        pass

def debug_peripherals():
    for p in _list:
        p.debug()

def reset_peripherals():
    for p in _list:
        p.reset()

