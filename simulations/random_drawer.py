from pygame.locals import *

import pygame
from core.physics.Vector import Vector
from core.Shapes import Segment
from core.Utils import Color
from core.engine.Simulation import Simulation


class RandomDrawer(Simulation):

    FPS = 144
    center = Vector(int(Simulation.WIDTH / 2), int(Simulation.HEIGHT / 2))
    segment = Segment(90, start_point=center)
    segment_2 = segment.add_segment(90)[0]
    segment_3 = segment_2.add_segment(90)[0]
    segment_4 = segment_3.add_segment(90)[0]
    segment_5 = segment_4.add_segment(90)[0]
    segments = [segment, segment_2, segment_3, segment_4, segment_5]

    rotation_rate = 0.161803398875
    points_to_fade = []
    fade_amount = 2000
    counter = 0

    def update(self):
        self.surface.fill(Color.BLACK)
        self.display.fill(Color.BLACK)
        self.segments[1].rotate(self.rotation_rate*2)
        self.segments[0].rotate(self.rotation_rate+0.01)
        self.segments[2].rotate(self.rotation_rate+0.03)
        self.segments[3].rotate(self.rotation_rate+0.04)
        self.segments[4].rotate(self.rotation_rate+0.01)

        for segment in self.segments:
            clr, a, b = segment.get_drawing_data()
            # pygame.draw.line(self.display, clr, a, b)

        last = self.segments[-1].point_b
        self.points_to_fade.append(Vector(last.x, last.y))

        if len(self.points_to_fade) > self.fade_amount:
            self.points_to_fade.pop(0)

        color = [255, 0, 255]
        if self.counter % 7 == 0:
            color = [0, 255, 255]
            self.counter = 0

        for point in self.points_to_fade:
            pygame.draw.circle(self.display, color, point.get_cords(), 2)
            Color.fade_to_black(color, 2000)
            #point.x += 0.012
            #point.y += 0.0212
            # point.rotate(self.center, 0.006, True)

        self.counter += 1

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
