
from core.entities.cognition.Brain import Brain
from abc import ABC, abstractmethod


class BrainTrainer(ABC):

    def __init__(self, brain: Brain) -> None:
        self.brain = brain
