from core.physics import Vector
from core.engine import Reality


class RealObject:

    def __init__(self, position: Vector, reality: Reality):
        self.position = position
        self.reality = reality
