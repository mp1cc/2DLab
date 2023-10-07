import math


class Neuron:
    def __init__(self, weights: list[float], bias: float, learning_rate: float = 0.007):
        self.weights: list[float] = weights
        self.bias: float = bias
        self.learning_rate: float = learning_rate
        self.last_input = None
        self.last_output = None

    def activate(self, inputs: list[float]) -> float:
        weighted_sum = sum(x * w for x, w in zip(inputs, self.weights)) + self.bias
        output = self._tanh(weighted_sum)
        self.last_input = inputs
        self.last_output = output
        return output

    @staticmethod
    def _tanh(x: float) -> float:
        return math.tanh(x)

    @staticmethod
    def _tanh_derivative(x: float) -> float:
        return 1 - x ** 2

    def backpropagate(self, error: float) -> None:
        d_error_d_output = error
        d_output_d_weighted_sum = self._tanh_derivative(self.last_output)
        d_weighted_sum_d_weights = self.last_input

        for i, input_val in enumerate(d_weighted_sum_d_weights):
            self.weights[i] -= self.learning_rate * d_error_d_output * d_output_d_weighted_sum * input_val

        self.bias -= self.learning_rate * d_error_d_output * d_output_d_weighted_sum
