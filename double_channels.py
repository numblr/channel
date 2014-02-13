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
from .channels import memoryless_channel, multi_input_channel
from .channels import process_sequence as process
from ._util import identity, start
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
@start
def moving_average_channel(n, initial_values = [], operation = identity, zero_val=0):
    """Returns a generator that returns the moving average over n elements preceeding its input.
    
    Keyword arguments:
    
    initial_values -- At most n default values for the first iterations (default empty)
    operation -- a function that operates on the inputs to the generator (default identity)
    
    """ 
    init = list(initial_values)
    init_value_count = len(init)
    if init_value_count > n:
        raise ValueError("There can be at most {0} initial values: {1} where given ".format(n, len(initial_values)))
    
    buffer_ = init + [zero_val] * (n - init_value_count)
    count = 0
    while True:
        input_ = operation((yield mean(buffer_)))
        
        buffer_[count] = input_
        count = (count + 1) % n


def _inverse(value):
    return - value


@multi_input_channel(sum_channel)
def inverse_channel(n):
    """Returns an initialized generator that outputs the negative of the summed input."""
    return memoryless_channel(_inverse)


def process_sequence(channel, input_sequence):
    """Returns an infinite generator of outputs for the given sequence of inputs.
    
    The input_sequence must be a single number, a sequence of numbers or a
    sequence of sequences of numbers.
    
    The generator contains the output values of the module that is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of zeros.
    None values in the output are converted to zeros.
    
    """
    return process(channel, input_sequence, iter(int, 1), 0)#"infinite generator of zeros")))