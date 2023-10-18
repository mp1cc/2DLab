from time import time
from random import seed, random


class Color:
    WHITE: tuple[int] = 255, 255, 255
    BLACK: tuple[int] = 0, 0, 0
    GREEN: tuple[int] = 0, 255, 0
    RED: tuple[int] = 255, 0, 0

    @staticmethod
    def random_color() -> list[int]:
        """ Generate a tuple containing random RGB values
        :return: (RED, GREEN, BLUE)
        """
        seed(time()*10000000)
        return [
            int((random() * 1000) % 255) for v in range(3)
        ]

    @staticmethod
    def fade_to_black(color: list[int], rate: float) -> None:
        for i in range(len(color)):
            color[i] -= color[i] / rate
