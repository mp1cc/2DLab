import numpy
import pygame
import sys
from pygame.locals import *
from abc import ABC


class Simulation(ABC):
    """ Base Simulation Class
    This class is meant to serve as a parent class for you to create your own
    simulations. It handles the main loop for pygame and all its settings so
    that you don't have to copy/paste them all over the place.
    Simply inherit from this class, override the update() function (main game loop),
    and you're good to go.
    Finally, you call it in a main function like so.

    class ExampleSim(Simulation):

        def update():
            # simulation code that will be executed each frame.

    if __name__ == '__main__':
        ExampleSim().run()
    """

    HEIGHT: int = 1000
    WIDTH: int = 1000
    SCREEN_CENTER: tuple[float, float] = (
        HEIGHT / 2,
        WIDTH / 2
    )
    FPS: int = 60

    def __init__(self):
        self.fps_clock = pygame.time.Clock()
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.set_caption()
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT))

    def update(self):
        """ Override this function and add your simulation code here.
        """
        pass

    @staticmethod
    def check_exit():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def get_surface_2d(self) -> numpy.ndarray:
        return pygame.surfarray.array2d(self.surface)

    def run(self):
        while True:
            self.display.blit(self.surface, self.SCREEN_CENTER)
            self.update()
            self.check_exit()
            pygame.display.update()
            self.fps_clock.tick(self.FPS)

    def set_caption(self):
        pygame.display.set_caption(str(self.name()))

    def name(self):
        return str(self.__class__).strip("<>'").split(".")[-1]
