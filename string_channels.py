"""Channels that process string input.

All channels accept either a single string or a sequence of strings as input.
The output maybe truncated if it becomes unreasonably large.

sum_channel -- outputs the concatenate the strings in the input
delay_channel -- outputs the previous summed input strings 
echo channel -- outputs the summed input concatenated with itself
reverse_channel -- outputs the reverse summed input
process_sequence -- helper function to process a sequence of inputs on a channel

See also modular.channels.channels

"""
from itertools import chain
from modular.channels.channels import shift_channel, memoryless_channel, \
    multi_input_channel

DELAY_INITIAL = "hello"

_MAX_LENGTH = 10000

def _sum(value):
    return "".join(value)[:_MAX_LENGTH]

def sum_channel():
    """Returns an initialized generator that outputs the concatenated strings in the input."""
    return memoryless_channel(_sum)

@multi_input_channel(sum_channel)
def delay_channel():
    """Returns an initialized generator that outputs the previous summed input."""
    return shift_channel(1, [DELAY_INITIAL])
    
def _echo(value):
    return (value * 2)[:_MAX_LENGTH]
        
@multi_input_channel(sum_channel)
def echo_channel():
    """Returns an initialized generator that outputs the summed input concatenated with itself."""
    return memoryless_channel(_echo)
    
def _reverse(value):
    return value[::-1]

@multi_input_channel(sum_channel)
def reverse_channel():
    """Returns an initialized generator that outputs the summed input reversed."""
    return memoryless_channel(_reverse)

def process_sequence(channel, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The input_sequence must be a single string, a sequence of strings or a
    sequence of sequences of strings.
    
    The generator contains the output values of the channel that is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings. None values in the output are converted to empty strings.
    
    """
    inputs = chain(input_sequence, iter(str, "infinite generator of empty strings"))
    raw_outputs = (channel.send(input_) for input_ in inputs)
    
    return (output if output else "" for output in raw_outputs)