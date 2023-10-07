import random

from core.entities.Neuron import Neuron


class Brain:
    def __init__(self, input_size, output_size, hidden_sizes):
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
        layer_input = inputs
        for layer in [self.input_layer] + self.hidden_layers:
            layer_output = [neuron.activate(layer_input) for neuron in layer]
            layer_input = layer_output
        return [neuron.activate(layer_input) for neuron in self.output_layer]

    def train(self, inputs: list[float], expected_output: list[float]):
        # Forward pass
        outputs = self.forward_pass(inputs)
        assert len(outputs) == len(expected_output), "Output and expected output size mismatch."

        # Compute the initial error
        error = [o - e for o, e in zip(outputs, expected_output)]

        # Backward pass
        for i in reversed(range(len(self.hidden_layers) + 1)):
            layer = self.output_layer if i == len(self.hidden_layers) else self.hidden_layers[i]

            # Backpropagate the error for each neuron in the current layer
            for j, neuron in enumerate(layer):
                neuron.backpropagate(error[j])

            # If this is the output layer, no need to compute error for further layers
            if i == 0:
                break

            # Compute the error for the next layer in the backward pass
            next_layer = layer
            layer = self.hidden_layers[i - 1] if i != 0 else self.input_layer

            # Update error for each neuron in the current layer
            error = [
                sum(next_neuron.weights[j] * error[k] for k, next_neuron in enumerate(next_layer))
                for j, neuron in enumerate(layer)
            ]

            # Validate: Ensure error is not empty and has correct size
            assert error, "Error is empty."
            assert len(error) == len(layer), (
                f"Error size does not match layer size. "
                f"Error size: {len(error)}, Layer size: {len(layer)}"
            )


# simple xor test for a basic brain
if __name__ == '__main__':
    xor_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    xor_outputs = [[0], [1], [1], [0]]

    brain = Brain(2, 1, [4, 3])

    epochs = 50000

    # Train the network
    for epoch in range(epochs):
        total_error = 0
        for i in range(len(xor_inputs)):
            brain.train(xor_inputs[i], xor_outputs[i])
            output = brain.forward_pass(xor_inputs[i])
            error = sum((o - xo) ** 2 for o, xo in zip(output, xor_outputs[i]))
            total_error += error

        if epoch % 1000 == 0:
            print(f'Epoch: {epoch}, Error: {total_error:.6f}')

    # Evaluate the network
    for i in range(len(xor_inputs)):
        print(
            f'Input: {xor_inputs[i]}, Output: {brain.forward_pass(xor_inputs[i])[0]:.6f}, Expected: {xor_outputs[i][0]}'
        )
