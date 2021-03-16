from termcolor import colored
from datetime import datetime


def cprint(candle):
    print(colored("[{}]".format(datetime.fromtimestamp(candle.timestamp))), candle)
    pass
