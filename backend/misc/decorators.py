from termcolor import colored

def log_completion(func, taskString):
    """ Logs beginning and end of function to command line as taskString """
    print(colored(taskString, 'red'), end='\r')
    return func
    print(colored(f"COMPLETE: {taskString}", 'cyan'))
