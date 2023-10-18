from core.physics import Vector
from core.entities.RealObject import RealObject
import math


class Entity(RealObject):

    def __init__(
            self,
            position: Vector
    ):
        super().__init__(position)
        self.velocity: Vector = Vector(0, 0)
        self.acceleration: Vector = Vector(0, 0)
        self.rotation: float = 0.0
        self.friction: float = 0.9

    def _update_position(self) -> None:
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = self.acceleration.multiply(self.friction, self.friction)

    def _move(self, direction: Vector) -> None:
        self.acceleration += direction.normalize()

    def _rotate(self, radians: float) -> None:
        if radians > math.pi:
            radians = radians % math.pi
        self.rotation = radians

    def ray_cast(self, distance: int) -> list[Vector]:
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
