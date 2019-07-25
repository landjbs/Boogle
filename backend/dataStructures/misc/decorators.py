import functools
from termcolor import colored


def log_completion(func=None,*, taskString=""):
    """ Logs beginning and end of function to command line as taskString """
    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        print(colored(taskString, 'red'), end='\r')
        value = func(*args, **kwargs)
        print(colored(f"COMPLETE: {taskString}", 'cyan'))
        return value
    return wrap_func
