import random

import math


class Neuron:
    def __init__(self, weights: list[float], bias: float):
        self.weights = weights
        self.bias = bias
        self.learning_rate: float = 0.1

    def activate(self, inputs: list[float]) -> float:
        weighted_sum = sum([inputs[i] * self.weights[i] for i in range(len(inputs))])
        weighted_sum += self.bias
        output = self._sigmoid(weighted_sum)

        return output

    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))

    def error(self, output: float, target: float) -> float:
        error = output - target
        return error

    def backpropagate(self, inputs: list[float], error: float) -> None:
        weights_gradient: list[float] = [inputs[i] * error for i in range(len(inputs))]
        bias_gradient: float = error

        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * weights_gradient[i]
        self.bias -= self.learning_rate * bias_gradient


class Brain:
    def __init__(self, input_size: int, output_size: int, hidden_sizes: tuple[int] | list[int]):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_sizes = hidden_sizes
        self.input_layer = None
        self.hidden_layers = None
        self.output_layer = None

        self._build_brain()

    def _build_neuron_layer(self, input_size: int, size: int) -> list[Neuron]:
        layer: list = []
        for i in range(size):
            layer.append(
                Neuron(
                    weights=[random.random() for i in range(input_size)],
                    bias=random.random()
                )
            )
        return layer

    def _build_brain(self) -> None:
        self.input_layer = self._build_neuron_layer(self.input_size, self.input_size)
        hidden_layers = []
        for i in range(len(self.hidden_sizes)):
            previous_size = self.input_size if i == 0 else self.hidden_sizes[i - 1]
            hidden_layers.append(
                self._build_neuron_layer(previous_size, self.hidden_sizes[i])
            )
        self.hidden_layers = hidden_layers
        self.output_layer = self._build_neuron_layer(self.hidden_sizes[-1], self.output_size)

    def _activate_layer(self, layer: list[Neuron], inputs: list[float]) -> list[float]:
        outputs: list = []
        for i in range(len(layer)):
            neuron: Neuron = layer[i]
            outputs.append(neuron.activate(inputs))
        return outputs

    def process(self, inputs: list[float]) -> list[float]:
        if len(inputs) != self.input_size:
            raise ValueError("The number of inputs does not match the size of the first neuron layer")
        outputs: list = self._activate_layer(self.input_layer, inputs)

        for layer in self.hidden_layers:
            outputs = self._activate_layer(layer, outputs)

        outputs = self._activate_layer(self.output_layer, outputs)

        return outputs


if __name__ == '__main__':
    brain1 = Brain(input_size=3, output_size=2, hidden_sizes=[4, 5, 6])

    inputs1 = [0.3, 0.5, 0.6]

    outputs1 = brain1.process(inputs1)

    print(outputs1)
