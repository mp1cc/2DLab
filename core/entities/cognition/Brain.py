import random
from core.entities.cognition.Neuron import Neuron

import logging


class Brain:
    def __init__(self, input_size, output_size, hidden_sizes):
        # Validate parameters
        if input_size <= 0 or output_size <= 0 or any(size <= 0 for size in hidden_sizes):
            raise ValueError("Layer sizes must be positive integers.")
        
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_sizes = hidden_sizes
        self.input_layer = self._build_neuron_layer(input_size, input_size)
        self.hidden_layers = self._build_hidden_layers(input_size, hidden_sizes)
        self.output_layer = self._build_neuron_layer(hidden_sizes[-1], output_size)

    def _build_hidden_layers(self, input_size: int, hidden_sizes: list[int]):
        hidden_layers = []
        previous_size = input_size
        for layer_size in hidden_sizes:
            hidden_layers.append(
                self._build_neuron_layer(previous_size, layer_size)
            )
            previous_size = layer_size
        return hidden_layers

    @staticmethod
    def _build_neuron_layer(input_size, size):
        return [
            Neuron(
                weights=[random.uniform(-1, 1) for _ in range(input_size)],
                bias=random.uniform(-1, 1)
            ) for _ in range(size)
        ]

    def forward_pass(self, inputs: list[float]) -> list[float]:
        # Validate inputs
        if len(inputs) != self.input_size:
            raise ValueError(f"Input size must be {self.input_size}.")
        logging.debug(f"Forward pass inputs: {inputs}")
        layer_input = inputs
        for layer in [self.input_layer] + self.hidden_layers:
            layer_output = [neuron.activate(layer_input) for neuron in layer]
            layer_input = layer_output
        return [neuron.activate(layer_input) for neuron in self.output_layer]


