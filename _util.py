"""Utility functions for channels."""
def identity(x):
    return x

def compose(f, g):
    def h(x):
        return f(g(x))
    
    return h

def start(generator_function):
    def wrapper(*args):
        generator = generator_function(*args)
        next(generator)
        
        return generator
    
    return wrapper