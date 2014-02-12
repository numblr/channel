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
from .channels import shift_channel, memoryless_channel, multi_input_channel
from ._util import identity
from itertools import chain
from numpy import mean

def _sum(value):
    if value is None:
        raise TypeError("NoneType")
    try:
        return sum(value)
    except TypeError:
        return value

def sum_channel():
    """Returns an initialized generator that outputs the concatenated strings in the input."""
    return memoryless_channel(_sum)


@multi_input_channel(sum_channel)
def moving_average_channel(n, initial_values = [], operation = identity):
    """Returns a generator that returns the moving average over n elements in its input.
    
    The moving average induces a delay of n/2 steps against it's input
    
    Keyword arguments:
    
    initial_values -- At most n default outputs for the first iterations (default empty)
    operation -- a function that operates on the inputs to the generator (default identity)
    
    """ 
    count = n // 2
    if len(initial_values) > count:
        raise ValueError("There can be at most {0} initial values: {1} where given ".format(n, len(initial_values)))
    
    buffer_ = list(initial_values) + [0] * (n - count)
    
    while True:
        input_ = operation((yield mean(buffer_)))
        
        buffer_[count] = input_
        count = (count + 1) % n


@multi_input_channel(sum_channel)
def delay_channel():
    """Returns an initialized generator that outputs the previous summed input."""
    return shift_channel(44100)


def _inverse(value):
    return - value


@multi_input_channel(sum_channel)
def inverse_channel():
    """Returns an initialized generator that outputs the negative of the summed input."""
    return memoryless_channel(_inverse)


def process_sequence(channel, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The input_sequence must be a single string, a sequence of strings or a
    sequence of sequences of strings.
    
    The generator contains the output values of the module that is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings. None values in the output are converted to empty strings.
    
    """
    inputs = chain(input_sequence, iter(int, 1))#"infinite generator of zeros"))
    raw_outputs = (channel.send(input_) for input_ in inputs)
    
    return (output for output in raw_outputs if output)