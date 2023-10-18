from core.entities.cognition.ActivationFunctions import ActivationFunction
from core.entities.cognition.ActivationFunctions import Sigmoid


class Neuron:
    def __init__(
            self, 
            weights: list[float], 
            bias: float, 
            learning_rate: float = 0.007, 
            activation_function: ActivationFunction = Sigmoid
    ):
        self.weights: list[float] = weights
        self.bias: float = bias
        self.learning_rate: float = learning_rate
        self.last_input = None
        self.last_output = None
        self.activation_function = activation_function

    def activate(self, inputs: list[float]) -> float:
        weighted_sum = sum(x * w for x, w in zip(inputs, self.weights)) + self.bias
        output = self.activation_function.activate(weighted_sum)
        self.last_input = inputs
        self.last_output = output
        return output

    def adjust_weights(self, error: float) -> None:
        d_error_d_output = error
        d_output_d_weighted_sum = self.activation_function.derivative(self.last_output)
        d_weighted_sum_d_weights = self.last_input

        for i, input_val in enumerate(d_weighted_sum_d_weights):
            self.weights[i] -= self.learning_rate * d_error_d_output * d_output_d_weighted_sum * input_val

        self.bias -= self.learning_rate * d_error_d_output * d_output_d_weighted_sum
