from math import cos, sin, sqrt, pow


class Vector:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def rotate(
            self,
            center: "Vector",
            angle: float,
            rotate_self: bool = False
    ) -> ["Vector", None]:
        """ Apply rotation around center vector
        :param rotate_self: (bool)
            - True: Rotate the vector itself
            - False: Return new rotated vector object
        :param center: (Vector) Center of rotation
        :param angle: (float) Rotation angle
        """
        rx = self._calculate_x_rotation(center, angle)
        ry = self._calculate_y_rotation(center, angle)
        if rotate_self:
            self.x = rx
            self.y = ry
        else:
            return Vector(rx, ry)

    def _calculate_x_rotation(
            self,
            center: "Vector",
            angle: float
    ) -> int:
        return int(
            (self.x - center.x) * cos(angle) -
            (self.y - center.y) * sin(angle) +
            center.x
        )

    def _calculate_y_rotation(
            self,
            center: "Vector",
            angle: float
    ) -> int:
        return int(
            (self.x - center.x) * sin(angle) +
            (self.y - center.y) * cos(angle) +
            center.y
        )

    def copy(self):
        return Vector(self.x, self.y)

    def get_magnitude(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def normalize(self):
        self.x = self.x / self.get_magnitude()
        self.y = self.y / self.get_magnitude()

    def multiply(self, scalar_x, scalar_y):
        return Vector(self.x * scalar_x, self.y * scalar_y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def get_cords(self):
        return self.x, self.y

    def __eq__(self, other):
        return int(self.x) == int(other.x) and \
            int(self.y) == int(other.y)
