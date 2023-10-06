from core.engine import Simulation
from core.engine import Reality


class PetriDish(Simulation):

    def __init__(self):
        super().__init__()
        self.reality = Reality(self)
        self.entities = [
        ]

    def update(self):
        pass


if __name__ == '__main__':
    PetriDish().run()
