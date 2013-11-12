"""A Module represents a named processing channel."""
class Module():
    def __init__(self, id_, channel):
        self.id = id_
        self.channel = channel
    
    def get_state(self):
        return self.id, self.channel

    def _start(self):
        return Module(self.id, self.channel())
    
    def __eq__(self, other):
        if self is other:
            return True
        
        if not other:
            return False
        
        return self.id == other.id and isinstance(other.channel, type(self.channel))
    
    def __hash__(self):
        return hash(self.id)