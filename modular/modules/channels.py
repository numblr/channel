from modular.modules.base import process

"""output = channel.send(val)"""

def process_sequence(module, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The input_sequence must be a single string, a sequence of strings or a
    sequence of sequences of strings.
    
    The generator contains the output values of the module that is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings. None values in the output are converted to empty strings.
    
    """
    inputs = chain(input_sequence, iter(str, "infinite generator of empty strings"))
    while True:
        input_value = next(inputs)
        module, new_output = process(module, input_value)

        yield new_output if new_output else ""

def multi_input_channel(channel):
    return chain(sum_channel, channel)

def delay_channel():
    return shift_channel(1, ["Hello"])
        
def echo_channel():
    return memoryless_channel(_echo)
    
def _echo(value):
    return value * 2

def sum_channel():
    return memoryless_channel(_sum)

def _sum(value):
    return " ".join(value)

def noop_channel():
    return memoryless_channel(id)

def channel(generator, *args):
    instance = generator(*args)
    instance.next()
    
    return instance
    
def shift_channel(n, initial_values = [], operation = id):
    if len(initial_values) > n + 1:
        raise ValueError("There can be at most {0} initial values: {1} where given ".format(n, len(initial_values)))
    
    def generator(n, init, op):
        length = n + 1
        buffer_ = list(init) + [None] * (length - len(init))
        
        count = -1
        while True:
            buffer_[count % length] = op((yield buffer_[count % length]))
            count += 1
            
    return channel(generator, n, initial_values, operation)

def memoryless_channel(operation):
    def generator(op):
        value = (yield)
        while True:
            value = op((yield value))

    return channel(generator, operation)

def chain(channel_1, channel_2):
    return memoryless_channel(_compose(channel_1.send, channel_2.send))

def _compose(f, g):
    def h(x):
        return f(g(x))
    
    return h