from time import time
from random import seed, random


class Color:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0

    @staticmethod
    def random_color():
        """ Generate a tuple containing random RGB values
        :return: (tuple(int)) (RED, GREEN, BLUE)
        """
        seed(time()*10000000)
        return [(random() * 1000) % 255 for v in range(3)]
