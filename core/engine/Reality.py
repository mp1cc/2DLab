from .Simulation import Simulation
import numpy
from core.entities.RealObject import RealObject
from core.physics.Vector import Vector


class Reality:

    objects: list[RealObject]

    def __init__(self, simulation: Simulation):
        self._simulation = simulation
        self.space_2d: numpy.ndarray = self._simulation.get_surface_2d()
        self.objects = []

    def update(self):
        self.space_2d = self._simulation.get_surface_2d()

    def get_object_by_position(self, position: Vector) -> RealObject | None:
        if self.objects:
            for real_object in self.objects:
                if real_object.position == position:
                    return real_object
