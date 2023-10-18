from core.physics.Vector import Vector
from core.entities.cognition.Brain import Brain
from core.entities.Entity import Entity
from core.entities.Food import Food

from core.entities.cognition.trainers.PolicyGradientTrainer import PolicyGradientTrainer
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from core.engine.Reality import Reality


class Creature(Entity):

    def __init__(
            self,
            position: Vector,
            reality: "Reality",
            brain_complexity: int = 1
    ) -> None:
        super().__init__(position)
        self.reality = reality
        self.vision_reach = 10
        brain_input_size = 3 + self.vision_reach
        brain_output_size = 6
        self.brain: Brain = Brain(
            brain_input_size,
            brain_output_size,
            [int(brain_input_size * 1.5) for _ in range(brain_complexity)]
        )
        self.energy: float = 1.0
        self.trainer = PolicyGradientTrainer(self.brain, True)
        self.alive = True
        self.last_direction: int = 1

    def __str__(self):
        return str(self.__hash__())

    def _vision(self, ray: list[Vector]) -> list[Vector]:
        pixel_ray: list = []
        for point in ray:
            try:
                pixel = self.reality.space_2d[point.x][point.y]
                pixel_ray.append(pixel)
            except IndexError:
                pixel_ray.append(0.0)
        return pixel_ray

    @staticmethod
    def _normalize_vision_ray(vision_ray):
        normalized = [x / 10000000 for x in vision_ray]
        return normalized

    def direct_ray_cast(self, direction: int):
        """ This allows for a simple vision mechanism. Ideally the vision ray cast direction
        should derive from a continuous brain output allowing the creature to see beyond this 4
        directions, but the current implementation is not precisely working yet.
        We need to look into that. """

        reach = range(1, self.vision_reach + 1)
        if direction == 1:  # Look North
            return [Vector(self.position.x, self.position.y + i) for i in reach]
        elif direction == 2:  # Look South
            return [Vector(self.position.x, self.position.y - i) for i in reach]
        elif direction == 3:  # Look East
            return [Vector(self.position.x + i, self.position.y) for i in reach]
        elif direction == 4:  # Look West
            return [Vector(self.position.x - i, self.position.y) for i in reach]

    def _perceive_environment(self, direction: int) -> list[float]:
        perception = [
            self.energy,
            self.position.x / 10000,  # This is a hotfix to keep values between 0 and 1.
            self.position.y / 10000   # We should use a function to normalize these values
        ]
        vision_ray = self._vision(self.direct_ray_cast(direction))
        vision_ray = self._normalize_vision_ray(vision_ray)
        perception += vision_ray
        return perception

    def _execute_action(self, action_probabilities):
        reward = -0.1
        done = False

        direction_probs = action_probabilities[:4]
        direction_probs /= np.sum(direction_probs)
        direction = np.random.choice([1, 2, 3, 4], p=direction_probs)

        eat_prob = action_probabilities[4]
        eat = np.random.choice([0, 1], p=[1 - eat_prob, eat_prob])

        rotation_prob = action_probabilities[5]
        rotate = np.random.choice([0, 1], p=[1 - rotation_prob, rotation_prob])

        self._move(direction)

        if eat > 0.5:
            self.energy -= 0.005
            food = self.reality.get_object_by_position(self.position)
            if food and isinstance(food, Food):
                print("consumed food")
                self.energy += food.energy
                reward = 1
                self.reality.objects.remove(food)

        if rotate:
            self.rotation += 0.1
        else:
            self.rotation -= 0.1

        if self.energy <= 0.5 or not self._position_is_valid():
            reward = -1
            done = True

        if not self._position_is_valid():
            self.energy -= 0.05

        next_state = self._perceive_environment(self.last_direction)

        return reward, next_state, done

    def _move(self, direction: int) -> None:
        if direction == 1:  # Move North
            self.position.y += 1
        elif direction == 2:  # Move South
            self.position.y -= 1
        elif direction == 3:  # Move East
            self.position.x += 1
        elif direction == 4:  # Move West
            self.position.x -= 1
        self.last_direction = direction

    def update(self) -> None:
        if self.energy <= 0:
            self.alive = False
            raise DeadCreature(self)

        self._update_position()
        state = self._perceive_environment(self.last_direction)
        action_probabilities = self.brain.forward_pass(state)

        reward, next_state, done = self._execute_action(action_probabilities)

        self.trainer.train(state, action_probabilities, reward, next_state, done)

        self.energy -= 0.001

    def _position_is_valid(self):
        """ Check if the creature is within the bounds of the environment.
        """
        max_x, max_y = self.reality.space_2d.shape
        return 0 <= self.position.x < max_x and 0 <= self.position.y < max_y


class DeadCreature(Exception):
    def __init__(self, creature: Creature, message: str = None):
        self.message = message if message is not None else \
            f"Creature {creature} is DEAD"
        super().__init__(self.message)
