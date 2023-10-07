import math
import pytest
from core.entities.Neuron import Neuron


@pytest.fixture
def sample_neuron():
    weights = [0.5, -0.5]
    bias = 0.5
    return Neuron(weights, bias)


def test_activation(sample_neuron):
    inputs = [1, 1]
    expected_output = math.tanh(sum(x * w for x, w in zip(inputs, sample_neuron.weights)) + sample_neuron.bias)

    output = sample_neuron.activate(inputs)

    assert output == expected_output
    assert sample_neuron.last_input == inputs
    assert sample_neuron.last_output == output


def test_tanh(sample_neuron):
    assert sample_neuron._tanh(0) == 0
    assert sample_neuron._tanh(1) == math.tanh(1)


def test_tanh_derivative(sample_neuron):
    assert sample_neuron._tanh_derivative(0) == 1
    assert sample_neuron._tanh_derivative(1) == 0


def test_backpropagate(sample_neuron):
    # Example error and previous input/output for testing
    error = 0.5
    sample_neuron.last_input = [1, 1]
    sample_neuron.last_output = sample_neuron._tanh(0.5)

    old_weights = sample_neuron.weights.copy()
    old_bias = sample_neuron.bias

    sample_neuron.backpropagate(error)

    # Ensure weights and bias are updated (actual update values depend on your learning rate and activation derivative)
    assert sample_neuron.weights != old_weights
    assert sample_neuron.bias != old_bias
