from itertools import chain

"""output = channel.send(val)"""

def identity(x):
    return x

def multi_input_channel(sum_channel):
    def wrapper(channel):
        return concatenate(sum_channel, channel)

    return wrapper
    
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

def concatenate(channel_1, channel_2):
    def generator():
        send_1 = init_channel(channel_1).send
        send_2 = init_channel(channel_2).send
    
        return memoryless_channel(_compose(send_2, send_1))
    
    return generator

def _compose(f, g):
    def h(x):
        return f(g(x))
    
    return h