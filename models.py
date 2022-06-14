from math import cos, sin, sqrt, pow
from utils import Color


class Vector:

    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color if color else Color.random_color()

    def rotate(self, center, angle, rotate_self=False):
        """ Apply rotation around center vector
        :param rotate_self: (bool)
            - True: Rotate the vector itself
            - False: Return new rotated vector object
        :param center: (Vector) Center of rotation
        :param angle: (float) Rotation angle
        """
        rx = (self.x - center.x) * cos(angle) \
            - (self.y - center.y) * sin(angle) \
            + center.x
        ry = (self.x - center.x) * sin(angle) \
            + (self.y - center.y) * cos(angle) \
            + center.y
        if rotate_self:
            self.x = rx
            self.y = ry
        else:
            return Vector(rx, ry)

    def copy(self):
        return Vector(self.x, self.y)

    def get_magnitude(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def normalize(self):
        self.x = self.x / self.get_magnitude()
        self.y = self.y / self.get_magnitude()

    def scale(self, scalar):
        self.x = self.x * scalar
        self.y = self.y * scalar

    def fade_to_black(self, rate):
        for i in range(len(self.color)):
            self.color[i] -= self.color[i] / rate

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def get_cords(self):
        return self.x, self.y

    def get_color(self):
        return tuple(self.color)


class Segment:

    def __init__(self, length, prev=None, start_point: Vector = None):
        self.point_a = start_point if prev is None else prev.point_b.copy()
        self.point_b = self.point_a + Vector(length, 0)
        self.prev = prev
        self.children = None
        self.color = (255, 0, 0)

    def is_head(self):
        return self.prev is None

    def is_tail(self):
        return self.children is None

    def add_segment(self, length):
        segment = Segment(length, self)
        if self.is_tail():
            self.children = [segment]
        else:
            self.children.append(segment)
        return self.children

    def rotate(self, angle):
        self.point_b.rotate(self.point_a, angle, True)
        self.update_children_pos()

    def update_children_pos(self):
        if not self.is_tail():
            for child in self.children:
                child.update_pos()

    def update_pos(self):
        magnitude = self.point_b - self.point_a
        self.point_a = self.prev.point_b.copy()
        self.point_b = self.point_a + magnitude
        self.update_children_pos()

    def get_drawing_data(self):
        return self.color, self.point_a.get_cords(), self.point_b.get_cords()
