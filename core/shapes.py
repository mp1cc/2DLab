from core.physics.vector import Vector


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
