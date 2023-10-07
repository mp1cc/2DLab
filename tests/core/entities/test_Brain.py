import pytest
from core.entities.Brain import Brain


@pytest.fixture
def sample_brain():
    input_size = 2
    output_size = 1
    hidden_sizes = [3, 2]
    return Brain(input_size, output_size, hidden_sizes)


def test_initialization(sample_brain):
    # Input layer
    assert len(sample_brain.input_layer) == 2
    for neuron in sample_brain.input_layer:
        assert len(neuron.weights) == 2  # input_size

    # Hidden layers
    assert len(sample_brain.hidden_layers) == 2  # number of hidden layers
    for i, size in enumerate(sample_brain.hidden_sizes):
        assert len(sample_brain.hidden_layers[i]) == size  # neurons in each layer
        for neuron in sample_brain.hidden_layers[i]:
            prev_layer_size = 2 if i == 0 else sample_brain.hidden_sizes[i - 1]
            assert len(neuron.weights) == prev_layer_size  # weights based on previous layer size

    # Output layer
    assert len(sample_brain.output_layer) == 1  # output_size
    for neuron in sample_brain.output_layer:
        assert len(neuron.weights) == 2  # last hidden layer size


def test_forward_pass(sample_brain):
    inputs = [1, 1]
    output = sample_brain.forward_pass(inputs)

    # Check if output is between -1 and 1 (tanh activation)
    assert -1 <= output[0] <= 1


def test_train_xor(sample_brain):
    xor_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    xor_outputs = [[0], [1], [1], [0]]

    # Training
    epochs = 50000
    for epoch in range(epochs):
        for i in range(len(xor_inputs)):
            sample_brain.train(xor_inputs[i], xor_outputs[i])

    # Testing
    for i, input_data in enumerate(xor_inputs):
        output = sample_brain.forward_pass(input_data)[0]

        # Check if the output is close to the expected output
        assert abs(output - xor_outputs[i][0]) < 0.1
