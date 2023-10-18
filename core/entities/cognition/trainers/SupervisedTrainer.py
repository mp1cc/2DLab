from core.entities.cognition.trainers.BrainTrainer import BrainTrainer


class SupervisedTrainer(BrainTrainer):

    def train(self, inputs: list[float], expected_output: list[float]):
        # Forward pass
        outputs = self.brain.forward_pass(inputs)
        assert len(outputs) == len(expected_output), "Output and expected output size mismatch."

        # Compute the initial error
        error = [o - e for o, e in zip(outputs, expected_output)]

        self.backward_pass(error)

    def backward_pass(self, error: list[float]):
        for i in reversed(range(len(self.brain.hidden_layers) + 1)):
            layer = self.brain.output_layer if i == len(self.brain.hidden_layers) else self.brain.hidden_layers[i]

            # Backpropagate the error for each neuron in the current layer
            for j, neuron in enumerate(layer):
                neuron.adjust_weights(error[j])

            # If this is the output layer, no need to compute error for further layers
            if i == 0:
                break

            # Compute the error for the next layer in the backward pass
            next_layer = layer
            layer = self.brain.hidden_layers[i - 1] if i != 0 else self.brain.input_layer

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