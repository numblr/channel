"""Input processing units.

A channel is a generator function that creates an initalized generator for
input procssing. Processing is done by sending the input to the generator
using its send method:

>>> initialized_channel = some_channel()
>>> output = initialized_channel.send(input)

The generator is imediatelly initialized, that is, the first call to the
send method should already contain the first input value, not None.

shift_channel -- process consecutive inputs and output them shifted against the input
memoryless_channel -- process consecutive inputs independently 
multi_input_channel -- decorator to concatenate a single input channel with a channel that allows multiple inputs
concatenate -- concatenate channels

"""
from ._util import compose, identity, start

@start
def shift_channel(n, initial_values = [], operation = identity):
    """Returns a generator that returns its processed output shifted by n iterations against its input.
    
    Keyword arguments:
    
    initial_values -- At most n default outputs for the first iterations (default empty)
    operation -- a function that operates on the inputs to the generator (default identity)
    
    """ 
    if len(initial_values) > n:
        raise ValueError("There can be at most {0} initial values: {1} where given ".format(n, len(initial_values)))
    
    length = n + 1
    buffer_ = [None] * (n - len(initial_values)) + list(initial_values) + [None] 
    
    count = n
    while True:
        buffer_[count] = operation((yield buffer_[count]))
        count = (count + 1) % length
        
@start
def memoryless_channel(operation = identity):
    """Returns a generator that processes its inputs independently and returns the output immediately.
    
    Keyword arguments:
    
    operation -- a function that operates on the inputs to the generator (default identity)
    
    """ 
    processed_value = None
    while True:
        value = (yield processed_value)
        processed_value = operation(value)

def multi_input_channel(sum_channel):
    """Decorator to concatenate the given sum_channel with the decorated channel."""
    def wrapper(channel):
        return concatenate(sum_channel, channel)

    return wrapper

def concatenate(channel_1, channel_2):
    """Concatenates the given channels, that is the output of channel_1 is sent to channel_2"""
    def generator_function():
        send_1 = channel_1().send
        send_2 = channel_2().send
    
        return memoryless_channel(compose(send_2, send_1))
    
    return generator_function