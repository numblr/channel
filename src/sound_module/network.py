from sound_module.streams import Reverse, Delay, ArrayStream, Stream
    
class Module(object):
    def __init__(self, module_id, stream):
        self.__id = module_id
        self.__stream = stream
        
    def get_id(self):
        return self.__id

    def add_input(self, new_input):
        self.__stream.with_input(new_input.__stream)
        
    def output(self, time):
        return self.__stream.output(time)
    
    def _get_stream(self):
        return self.__stream
    
class Network(Stream):
    def __init__(self, array_input):
        self.__input = Module("input", array_input)
        self.__modules = {}
        self.__output = array_input
        self.__first = True
        
    def add_module(self, module):
        if self.__first:
            module.add_input(self.__input)
            self.__first = False
        self.__modules[module.get_id()] = module
        self.__output = module
        
    def add_connection(self, module_out_id, module_in_id):
        input_module = self.__modules[module_in_id]
        output_module = self.__modules[module_out_id]
        input_module.add_input(output_module)
        
    def output(self, time):
        return self.__output.output(time)

if __name__ == "__main__":
    inputs = ArrayStream(("Hello", "World", ""))
    net = Network(inputs)
    net.add_module(Module("A", Reverse()))
    net.add_module(Module("B", Delay()))
    net.add_connection("A", "B")
    net.add_connection("B", "A")
    
    print(net.output(0))
    print(net.output(1))
    print(net.output(2))
    print(net.output(3))
    print(net.output(8))
