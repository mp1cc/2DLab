from core.entities.cognition.trainers.QTrainer import ReinforcedTrainer
from core.entities.cognition.Brain import Brain
import pytest
import numpy as np

# Your class definitions should be here or imported

def test_reinforced_trainer():
    # Example state and action
    state = [0.5, 0.1, 0.2]  
    next_state = [0.6, 0.1, 0.2]  
    action = 1  
    reward = 1.0  
    done = False  
    
    # Neural network architecture
    input_size = 3
    output_size = 3
    hidden_sizes = [3]

    # Create a brain instance
    brain = Brain(input_size, output_size, hidden_sizes)

    # Create a ReinforcedTrainer instance
    trainer = ReinforcedTrainer(brain) 

    # Train the network with the sample data
    trainer.train(state, action, reward, next_state, done)

    # Test forward pass with the trained brain
    output = brain.forward_pass(state)

    # Validate the output
    assert isinstance(output, list), "Output is not a list"
    assert len(output) == output_size, "Output size is incorrect"
    assert all(isinstance(x, float) for x in output), "Output does not consist of floats"
