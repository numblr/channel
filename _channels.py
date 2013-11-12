"""output = channel.send(val)"""
from modular.channels._util import compose, identity, start

@start
def shift_channel(n, initial_values = [], operation = identity):
    if len(initial_values) > n + 1:
        raise ValueError("There can be at most {0} initial values: {1} where given ".format(n, len(initial_values)))
    
    length = n + 1
    buffer_ = list(initial_values) + [None] * (length - len(initial_values))
    
    count = -1
    while True:
        buffer_[count % length] = operation((yield buffer_[count % length]))
        count += 1
        
@start
def memoryless_channel(operation = identity):
    value = None
    while True:
        value = (yield value)
        value = operation(value)

def multi_input_channel(sum_channel):
    def wrapper(channel):
        return concatenate(sum_channel, channel)

    return wrapper
    
def concatenate(channel_1, channel_2):
    def generator():
        send_1 = channel_1().send
        send_2 = channel_2().send
    
        return memoryless_channel(compose(send_2, send_1))
    
    return generator