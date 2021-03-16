from termcolor import colored
from datetime import datetime


def cprint(candle):
    print(colored("[{}]".format(datetime.fromtimestamp(candle.timestamp), attrs=['blink'])), candle)
    pass

"""Values are colored on base of 0-100"""
def ranked_color(value):
    if value < 20:
        result = colored(str(value), "red")
    elif value >= 20 and value < 40:
        result = colored(str(value), "magenta")
    elif value >= 40 and value < 60:
        result = colored(str(value), "green")
    else:
        result = colored(str(value), "white")
    return result
