import pygame
import sys
from pygame.locals import *
from core.utils import Color


class Simulation:
    """ Base Simulation Class
    This class is meant to serve as a parent class for you to create your own
    simulations. It handles the main loop for pygame and all its settings so
    that you don't have to copy/paste them all over the place.
    Simply inherit from this class, override the update() function, and you're
    good to go.
    Finally, you call it in a main function like so.
    if __name__ == '__main__':
        SimpleColliders().run()
    """

    HEIGHT = 1000
    WIDTH = 1000
    FPS = 60

    def __init__(self):
        self.fps_clock = pygame.time.Clock()
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.set_caption()

    def update(self):
        pass

    @staticmethod
    def check_exit():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.display.fill(Color.BLACK)
            self.update()
            self.check_exit()
            pygame.display.update()
            self.fps_clock.tick(self.FPS)

    def set_caption(self):
        pygame.display.set_caption(str(self.name()))

    def name(self):
        return str(self.__class__).strip("<>'").split(".")[-1]
