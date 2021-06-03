def degree():

    for j in range(block,height_width,block):
        pygame.draw.line(screen, (100, 100, 100), (block,j), (height_width-20, j)) 
        pygame.draw.line(screen, (100, 100, 100), (j,block), (j, height_width-20))


from subprocess import call
import time
from functools import wraps
# import sleep to show output for some time period
from time import sleep
import os


# define clear function
def clear():
    # check and make call for specific operating system
    _ = call('clear' if os.name == 'posix' else 'cls')


def cronometra(function):
    @wraps(function)
    def wrapper(*args, **kwrds):
        start = time.time()
        print("This is the time that took for", function.__name__, "to Stated executing:", start)
        ret = function(*args, **kwrds)
        end = time.time() - start
        print("This is the time that took for", function.__name__, "to finish executing:", end)
        return ret

    return wrapper