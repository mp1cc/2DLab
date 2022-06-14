import pygame
import sys
from pygame.locals import *
from models import Vector, Segment, Color

HEIGHT = 1000
WIDTH = 1000
FPS = 250
fps_clock = pygame.time.Clock()
center = Vector(WIDTH/2, HEIGHT/2)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2D Lab')

segment = Segment(45, start_point=Vector(WIDTH / 2, HEIGHT / 2))
segment_2 = segment.add_segment(60)[0]
segment_3 = segment_2.add_segment(90)[0]
segment_4 = segment_3.add_segment(90)[0]
segment_5 = segment_4.add_segment(20)[0]

segments = [segment, segment_2, segment_3, segment_4, segment_5]
#segments = [segment, segment_2]
rotation_rate = 0.01
points_to_fade = []
fade_amount = 2000


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


while True:  # main game loop
    DISPLAYSURF.fill(Color.BLACK)
    segments[1].rotate(rotation_rate)
    segments[0].rotate(rotation_rate + 0.01)
    segments[2].rotate(rotation_rate + 0.0122)
    segments[3].rotate(rotation_rate - 0.01456521896333)
    segments[4].rotate(rotation_rate + 0.095555)

    for segment in segments:
        clr, a, b = segment.get_drawing_data()
        pygame.draw.line(DISPLAYSURF, clr, a, b)
    last = segments[-1].point_b
    points_to_fade.append(Vector(last.x, last.y))

    if len(points_to_fade) > fade_amount:
        points_to_fade.pop(0)

    for point in points_to_fade:
        pygame.draw.circle(DISPLAYSURF, point.get_color(), point.get_cords(), 1)
        point.fade_to_black(1000)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fps_clock.tick(FPS)
