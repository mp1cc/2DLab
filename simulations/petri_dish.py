from core.engine.Simulation import Simulation
from core.engine.Reality import Reality
from core.physics.Vector import Vector
from core.entities.Creature import Creature, DeadCreature
from core.entities.Food import Food
from core.Utils import Color
import pygame
import random


class PetriDish(Simulation):

    HEIGHT: int = 500
    WIDTH: int = 500
    SCREEN_CENTER: tuple[float, float] = (
        HEIGHT / 2,
        WIDTH / 2
    )

    def __init__(self):
        super().__init__()
        self.reality = Reality(self)
        self.creatures = []
        self._create_creatures(10, 10)
        self._create_food(10000)
        self.dead_creatures = []

    def _create_food(self, quantity: int):
        for _ in range(quantity):
            self.reality.objects.append(
                Food(
                    energy=0.5,
                    position=Vector(
                        random.randint(0, self.WIDTH),
                        random.randint(0, self.HEIGHT)
                    )
                )
            )

    def _create_creatures(self, quantity: int, complexity: int):
        for _ in range(quantity):
            self.creatures.append(
                Creature(
                    Vector(
                        int(self.SCREEN_CENTER[0]),
                        int(self.SCREEN_CENTER[1])
                    ),
                    self.reality,
                    complexity
                )
            )

    def update(self):
        self._remove_dead_creatures()
        self.display.fill(Color.BLACK)
        self.surface.fill(Color.BLACK)
        self.reality.update()
        self._draw_objects()
        self._update_creatures()

    def _update_creatures(self):
        for i in range(len(self.creatures)):
            creature = self.creatures[i]
            self._draw_creature(creature)
            try:
                creature.update()
            except DeadCreature as dc:
                print(dc)

    def _draw_objects(self):
        for food in self.reality.objects:
            pygame.draw.circle(self.display, Color.GREEN, food.position.get_cords(), 1)

    def _draw_creature(self, creature):
        creature_color = Color.WHITE
        vision_color = Color.RED
        vision_ray = creature.direct_ray_cast(creature.last_direction)
        for vector in vision_ray:
            pygame.draw.circle(self.display, vision_color, vector.get_cords(), 1)
        pygame.draw.circle(self.display, creature_color, creature.position.get_cords(), 1)

    def _remove_dead_creatures(self):
        self.creatures = [creature for creature in self.creatures if creature.alive]


if __name__ == '__main__':
    PetriDish().run()
