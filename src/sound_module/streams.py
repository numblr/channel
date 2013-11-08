from abc import ABCMeta, abstractmethod

class Stream(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def output(self, time):
        raise NotImplementedError
    
class ArrayStream(Stream):
    def __init__(self, values):
        self.__values = values
        
    def output(self, time):
        return self.__values[time] if time < len(self.__values) else ""
    
class NetworkStream(Stream):
    def __init__(self, network):
        self.__network = network
    
    def output(self, time):
        return self._network.get_output().output(time)
    
class InputStream(Stream):
    def __init__(self, inputs):
        self.__inputs = inputs
        
    def with_input(self, new_input):
        #return Stream(self.__inputs + (new_input, ))
        self.__inputs = self.__inputs + (new_input, )
    
    def _get_inputs(self):
        return self.__inputs
    
class Adder(InputStream):
    def __init__(self, inputs = tuple()):
        super(InputStream, self).__init__(inputs)

    def output(self, time):
        out = ""
        for x in self._get_inputs():
            out = out + x.output(time)
        
        return out
        #return sum([i.output(time) for i in self._get_inputs()])

class Delay(Adder):
    def __init__(self, inputs = tuple()):
        super(Adder, self).__init__(inputs)
        self.__time = -1
        self.__previous = "Hello"

    def output(self, time):
        if time == self.__time:
            return self.__previous
        
        if time == self.__time + 1:
            self.__time = time
            previous = self.__previous
            self.__previous = Adder.output(self, time)
            
            return previous
                
        return None
    
class Echo(Adder):
    def __init__(self, inputs = tuple()):
        super(Adder, self).__init__(inputs)

    def output(self, time):
        inputs = Adder.output(self, time)
        
        return inputs + inputs
            
class Reverse(Adder):
    def __init__(self, inputs = tuple()):
        super(Adder, self).__init__(inputs)

    def output(self, time):
        return Adder.output(self, time)[::-1]
        
class Noop(Adder):
    def __init__(self, inputs = tuple()):
        super(Adder, self).__init__(inputs)

    def output(self, time):
        return Adder.output(self, time)