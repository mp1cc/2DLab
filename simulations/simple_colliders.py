import pygame
from pygame.locals import *

from core.physics.RigidBody import SquareBody
from core.physics.Vector import Vector
from core.Utils import Color
from core.engine.Simulation import Simulation


class SimpleColliders(Simulation):

    center = Vector(Simulation.WIDTH / 2, Simulation.HEIGHT / 2)
    boxes = [
        SquareBody(center + Vector(0, 200), 70, 5),
        SquareBody(center + Vector(0, -160), 70, 10)
    ]

    def update(self):

        for box in self.boxes:
            self.draw_square_body(box)

        for box1 in self.boxes:
            for box2 in self.boxes:
                if box1 is not box2 and box2.calculate_collision(box1):
                    pygame.draw.circle(self.display, Color.WHITE, box1.position.get_cords(), 1)

        for box in self.boxes:
            box.update()

        self.boxes[1].rotate(0.01)
        self.boxes[0].rotate(0.01)
        self.boxes[0].position.rotate(self.center, 0.01, True)

    def draw_square_body(self, body: SquareBody):
        for vertex in body.vertices:
            pygame.draw.circle(self.display, Color.WHITE, vertex.get_cords(), 1)


if __name__ == '__main__':
    SimpleColliders().run()
