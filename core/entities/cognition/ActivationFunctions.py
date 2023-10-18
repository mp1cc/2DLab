import math
from abc import ABC, abstractmethod


class ActivationFunction(ABC):

    @staticmethod
    @abstractmethod
    def activate(x: float):
        """Abstract activation method"""
        pass

    @staticmethod
    @abstractmethod
    def derivative(x: float):
        """Abstract derivative method"""
        pass


class Tanh(ActivationFunction):

    @staticmethod
    def activate(x: float) -> float:
        """
        Computes the hyperbolic tangent of the input.
        """
        return math.tanh(x)

    @staticmethod
    def derivative(x: float) -> float:
        """
        Computes the derivative of the hyperbolic tangent of the input.
        """
        return 1 - x ** 2


class Sigmoid(ActivationFunction):
    @staticmethod
    def activate(x: float) -> float:
        """
        Computes the sigmoid of the input.
        """
        # Clip input to prevent overflow
        x = max(min(x, 15), -15)
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def derivative(x: float) -> float:
        """
        Computes the derivative of the sigmoid of the input.
        """
        sig = Sigmoid.activate(x)
        return sig * (1 - sig)
