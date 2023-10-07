from typing import TYPE_CHECKING
from core.entities.RealObject import RealObject
from core.physics.Vector import Vector

if TYPE_CHECKING:
    from core.engine.Reality import Reality


class Food(RealObject):
    def __init__(self, energy: int, position: Vector, reality: "Reality"):
        super().__init__(position, reality)
        self.energy = energy
