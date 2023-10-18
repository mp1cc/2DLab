from core.entities.cognition.trainers.BrainTrainer import BrainTrainer

import numpy as np


class ReinforcedTrainer(BrainTrainer):

    def train(self, state, action, reward, next_state, done, gamma=0.99):
        """
        Train the Brain using Q-learning approach.

        Parameters:
        - state: The current state.
        - action: The action taken.
        - reward: The reward received.
        - next_state: The state reached after taking the action.
        - done: Boolean indicating if the episode is finished.
        - gamma: Discount factor for future rewards.
        """

        # Forward pass for the current state and next state
        q_values = self.brain.forward_pass(state)
        next_q_values = self.brain.forward_pass(next_state)

        # Compute the target Q-value
        target = reward
        if not done:
            target += gamma * np.max(next_q_values)

        # Update the Q-value for the taken action towards the target
        target_q_values = q_values[:]
        target_q_values[action] = target

        # Backward pass: Update the weights based on the difference
        # between the target Q-values and the predicted Q-values
        self.backward_pass(state, target_q_values)

    def backward_pass(self, inputs: list[float], target_q_values: list[float]):
        """
        Backward pass for the neural network. Updates weights using the gradient
        of the loss with respect to the weights.
        
        Parameters:
        - inputs: The input features for the forward pass.
        - target_q_values: The target Q-values to train towards.
        """
        
        # Forward pass, storing the inputs to each layer
        layer_inputs = [inputs]
        for layer in [self.brain.input_layer] + self.brain.hidden_layers:
            layer_input = layer_inputs[-1]
            layer_output = [neuron.activate(layer_input) for neuron in layer]
            layer_inputs.append(layer_output)
        outputs = [neuron.activate(layer_inputs[-1]) for neuron in self.brain.output_layer]
        
        # Compute the error of the output layer
        error = [2 * (o - t) for o, t in zip(outputs, target_q_values)]
        
        # Backward pass through each layer, updating weights and computing error for the next layer
        for i in reversed(range(len(self.brain.hidden_layers) + 1)):
            layer = self.brain.output_layer if i == len(self.brain.hidden_layers) else self.brain.hidden_layers[i]
            
            # Update weights for each neuron in the current layer
            for j, neuron in enumerate(layer):
                # Adjusting the weights based on the error
                neuron.adjust_weights(error[j])
            
            # If this is not the input layer, compute error for the previous layer
            if i != 0:
                next_layer = layer
                layer = self.brain.hidden_layers[i - 1] if i != 0 else self.brain.input_layer
                
                # Compute error for each neuron in the current layer
                error = [
                    sum(next_neuron.weights[j] * error[k] for k, next_neuron in enumerate(next_layer))
                    for j, neuron in enumerate(layer)
                ]

