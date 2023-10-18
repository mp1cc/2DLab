from core.entities.RealObject import RealObject
from core.physics.Vector import Vector


class Food(RealObject):
    def __init__(self, energy: float, position: Vector):
        super().__init__(position)
        self.energy = energy
