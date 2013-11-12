from itertools import chain 
from modular.channels.channels import shift_channel, memoryless_channel, \
    multi_input_channel

DELAY_INITIAL = "Hello"

def _sum(value):
    return "".join(value)

def sum_channel():
    return memoryless_channel(_sum)

@multi_input_channel(sum_channel)
def delay_channel():
    return shift_channel(1, [DELAY_INITIAL])
    
def _echo(value):
    return value * 2
        
@multi_input_channel(sum_channel)
def echo_channel():
    return memoryless_channel(_echo)
    
def _reverse(value):
    return value[::-1]

@multi_input_channel(sum_channel)
def reverse_channel():
    return memoryless_channel(_reverse)

def process_sequence(channel, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The input_sequence must be a single string, a sequence of strings or a
    sequence of sequences of strings.
    
    The generator contains the output values of the module that is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings. None values in the output are converted to empty strings.
    
    """
    inputs = chain(input_sequence, iter(str, "infinite generator of empty strings"))
    raw_outputs = (channel.send(input_) for input_ in inputs)
    
    return (output if output else "" for output in raw_outputs)