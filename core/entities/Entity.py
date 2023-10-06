from core.physics import Vector
from core.engine import Reality
from core.entities.RealObject import RealObject
import math


class Entity(RealObject):

    def __init__(
            self,
            position: Vector,
            reality: Reality,
            max_energy: float = 100.0
    ):
        super().__init__(position, reality)
        self.max_energy: float = max_energy
        self.energy: float = max_energy
        self.velocity: Vector = Vector(0, 0)
        self.acceleration: Vector = Vector(0, 0)
        self.rotation: float = 0.0
        self.friction: float = 0.9

    def _update_position(self) -> None:
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = self.acceleration.multiply(self.friction, self.friction)

    def _move(self, direction: Vector) -> None:
        if self.energy:
            self.acceleration += direction.normalize()
            self.energy -= 1.0

    def _rotate(self, radians: float) -> None:
        if radians > math.pi:
            radians = radians % math.pi
        self.rotation = radians

    def _ray_cast(self, distance: int) -> list[Vector]:
        ray: list = []
        for i in range(distance):
            cursor: Vector = self.position + Vector(i + 1, 0)
            rotation_center = ray[-1] if ray else self.position
            ray.append(
                cursor.rotate(
                    center=rotation_center, angle=self.rotation
                )
            )
        return ray

    def update(self) -> None:
        self._update_position()
        self.energy -= 1.0
