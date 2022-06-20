from core.physics.vector import Vector


class RigidBody:

    def __init__(self, position: Vector = None, ):
        self.position = position if position is not None else Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

    def update(self):
        self.velocity += self.acceleration

    def calculate_collision(self, other):
        pass


class SquareBody(RigidBody):

    def __init__(self, position: Vector, size: float, rotation=0):
        super().__init__(position)
        self.size = size
        self.vertices = self.get_vertices(size)
        self.prev_position = position.copy()
        if rotation:
            self.rotate(rotation)
        self.rotation = rotation

    def get_vertices(self, size):
        return [
            self.position + Vector(size, size),
            self.position + Vector(-size, size),
            self.position + Vector(-size, -size),
            self.position + Vector(size, -size)
        ]

    def rotate(self, rotation_rate):
        for vertex in self.vertices:
            vertex.rotate(center=self.position, angle=rotation_rate, rotate_self=True)

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        if self.prev_position != self.position:
            self.vertices = self.get_vertices(self.size)
            self.rotate(self.rotation)

    def get_projection(self, y_axis=False):
        scalar_values = [vector.y if y_axis else vector.x for vector in self.vertices]
        return min(scalar_values), max(scalar_values)

    def projection_overlap(self, other, y_axis=False):
        s_proj = self.get_projection(y_axis)
        o_proj = other.get_projection(y_axis)

        return o_proj[0] < s_proj[0] < o_proj[1] or o_proj[0] < s_proj[1] < o_proj[1]

    def calculate_collision(self, other):
        return self.projection_overlap(other) and self.projection_overlap(other, y_axis=True)
