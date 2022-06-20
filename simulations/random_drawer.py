from pygame.locals import *

import pygame
from core.physics.vector import Vector
from core.shapes import Segment
from core.utils import Color
from simulations.simulation import Simulation


class RandomDrawer(Simulation):

    FPS = 250
    center = Vector(Simulation.WIDTH / 2, Simulation.HEIGHT / 2)
    segment = Segment(45, start_point=center)
    segment_2 = segment.add_segment(60)[0]
    segment_3 = segment_2.add_segment(90)[0]
    segment_4 = segment_3.add_segment(90)[0]
    segment_5 = segment_4.add_segment(20)[0]
    segments = [segment, segment_2, segment_3, segment_4, segment_5]

    rotation_rate = 0.01
    points_to_fade = []
    fade_amount = 2000

    def update(self):
        self.segments[1].rotate(self.rotation_rate)
        self.segments[0].rotate(self.rotation_rate + 0.01)
        self.segments[2].rotate(self.rotation_rate + 0.0122)
        self.segments[3].rotate(self.rotation_rate - 0.01456521896333)
        self.segments[4].rotate(self.rotation_rate + 0.095555)

        for segment in self.segments:
            clr, a, b = segment.get_drawing_data()
            pygame.draw.line(self.display, clr, a, b)

        last = self.segments[-1].point_b
        self.points_to_fade.append(Vector(last.x, last.y))

        if len(self.points_to_fade) > self.fade_amount:
            self.points_to_fade.pop(0)

        for point in self.points_to_fade:
            pygame.draw.circle(self.display, Color.random_color(), point.get_cords(), 1)

    @staticmethod
    def fade_points(points: list):
        display_image = []
        col = 255
        fade_rate = col / len(points)

        for vector in reversed(points):
            display_image.append(
                ((col, col, col), (vector.x, vector.y))
            )
            col -= fade_rate

        return reversed(display_image)


if __name__ == '__main__':
    RandomDrawer().run()
