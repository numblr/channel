from modular.channels.channels import DELAY_INITIAL, shift_channel,\
    memoryless_channel, chain

def multi_input_channel(channel):
    return chain(sum_channel, channel)

def delay_channel():
    return shift_channel(1, [DELAY_INITIAL])
        
def echo_channel():
    return memoryless_channel(_echo)
    
def _echo(value):
    return value * 2

def reverse_channel():
    return memoryless_channel(_reverse)
    
def _reverse(value):
    return value[::-1]

def sum_channel():
    return memoryless_channel(_sum)

def _sum(value):
    return "".join(value)
