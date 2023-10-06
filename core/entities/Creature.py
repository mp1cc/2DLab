from core.physics import Vector
from core.entities import Brain
from core.entities.Entity import Entity
from core.engine import Reality


class Creature(Entity):

    def __init__(
            self,
            position: Vector,
            reality: Reality,
            brain: Brain,
    ) -> None:
        super().__init__(position, reality)
        self.brain: Brain = brain

    def _vision(self, ray: list[Vector]) -> list[Vector]:
        pixel_ray: list = []
        for point in ray:
            try:
                pixel = self.reality.space_2d[point.x][point.y]
                pixel_ray.append(pixel)
            except IndexError:
                break
        return pixel_ray

    def update(self) -> None:
        if self.energy:
            self._update_position()
            brain_input = [
                self.position.x,
                self.position.y,
                self.energy
            ]
            brain_output = self.brain.process(brain_input)
            self.energy -= 1.0

