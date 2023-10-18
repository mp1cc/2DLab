from core.entities.cognition.trainers.BrainTrainer import BrainTrainer

import numpy as np


class PolicyGradientTrainer(BrainTrainer):
    def __init__(self, brain, continuous_actions=False):
        super().__init__(brain)
        self.trajectory = []
        self.continuous_actions = continuous_actions

    def train(self, state, action, reward, next_state, done, gamma=0.99):
        self.trajectory.append((state, action, reward))
        if done:
            self.backward_pass(gamma)
            self.trajectory = []

    def backward_pass(self, gamma):
        g = 0
        for state, action, reward in reversed(self.trajectory):
            g = reward + gamma * g
            self.update_weights(state, action, g)

    def update_weights(self, state, action, g):
        # Forward pass to get the action probabilities or parameters of the action distribution
        action_params = self.brain.forward_pass(state)

        if self.continuous_actions:
            standard_deviation = 1.0

            grad_log_policy = (np.array(action) - np.array(action_params)) / (standard_deviation ** 2)
        else:
            # Discrete action case: softmax output is assumed
            action_probs = action_params
            grad_log_policy = np.zeros_like(action_probs)
            grad_log_policy[action] = 1 / action_probs[action]

        for i, neuron in enumerate(self.brain.output_layer):
            # Update the weights
            neuron.adjust_weights(-g * grad_log_policy[i])
