from modular.modules.base import process

"""output = channel.send(val)"""

DELAY_INITIAL = "Hello"

def identity(x):
    return x

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

#def multi_input_channel(channel):
#    return chain(sum_channel, channel)
#
#def delay_channel():
#    return shift_channel(1, [DELAY_INITIAL])
#        
#def echo_channel():
#    return memoryless_channel(_echo)
#    
#def _echo(value):
#    return value * 2
#
#def reverse_channel():
#    return memoryless_channel(_echo)
#    
#def _reverse(value):
#    return value[::-1]
#
#def sum_channel():
#    return memoryless_channel(_sum)
#
#def _sum(value):
#    return "".join(value)
#
#def noop_channel():
#    return memoryless_channel(identity)
    
def shift_channel(n, initial_values = [], operation = identity):
    if len(initial_values) > n + 1:
        raise ValueError("There can be at most {0} initial values: {1} where given ".format(n, len(initial_values)))
    
    length = n + 1
    buffer_ = list(initial_values) + [None] * (length - len(initial_values))
    
    count = -1
    while True:
        buffer_[count % length] = operation((yield buffer_[count % length]))
        count += 1

def memoryless_channel(operation):
    value = None
    while True:
        value = (yield value)
        value = operation(value)
        
def init_channel(channel, *args):
    instance = channel(*args)
    instance.next()
    
    return instance

def chain(channel_1, channel_2):
    def generator():
        send_1 = init_channel(channel_1).send
        send_2 = init_channel(channel_2).send
    
        return memoryless_channel(_compose(send_2, send_1))
    
    return generator

def _compose(f, g):
    def h(x):
        return f(g(x))
    
    return h