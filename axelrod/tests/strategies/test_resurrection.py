"""Test for the Resurrection strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D
class Resurrection(TestPlayer):

    name = "Resurrection"
    player = axelrod.Resurrection
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by Cooperating
        self.first_play_test(C)
        
        # Check if the turns played are greater than 5 
        self.responses_test([D], [D, C, C, D, D, D, D, D] , [C] * 8)
        
        #Check if turns played are less than 5.
        self.responses_test([C], [D, C, D, C], [C] * 4)
        
        # Check for TFT behavior after 5 rounds
        self.responses_test([C], [C] * 5, [C, C, C, C, C, D])
        
        # Check for four defections and a cooperation by opponent
        self.responses_test([D], [C] * 5, [D, D, D, D, D, C])
