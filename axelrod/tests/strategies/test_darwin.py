"""Tests for the Darwin PD strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDarwin(TestPlayer):

    name = "Darwin"
    player = axelrod.Darwin
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,
        'manipulates_source': False,
        'manipulates_state': True
    }

    @classmethod
    def tearDownClass(cls):
        """After all tests have run, makes sure the Darwin genome is reset."""
        cls.player.reset_genome()
        super(TestDarwin, cls).tearDownClass()

    def setUp(self):
        """Each test starts with a fresh genome."""
        self.player.reset_genome()
        super(TestDarwin, self).setUp()

    def test_setup(self):
        player = self.player()
        self.assertEqual(player.genome, [C])
        self.assertEqual(player.history, [])

    def test_foil_strategy_inspection(self):
        self.assertEqual(self.player().foil_strategy_inspection(), C)

    def test_strategy(self):
        p1 = self.player()
        p1.reset()

        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)] * 5, attrs={'genome': [C] * 5})

        expected_genome = [D] * 4 + [C]
        self.versus_test(axelrod.Defector(), expected_actions=[(C, D)] * 5, attrs={'genome': expected_genome})

        # uses genome
        expected_actions = [(C, C)] + [(D, C)] * 3 + [(C, C)] * 2
        self.versus_test(axelrod.Cooperator(), expected_actions)

    def test_against_geller_and_mindreader(self):
        self.versus_test(axelrod.GellerCooperator(), expected_actions=[(C, C)] * 2, attrs={'genome': [C, C]})

        self.versus_test(axelrod.MindReader(), expected_actions=[(C, D)] * 2, attrs={'genome': [D, C]})

    def test_reset_only_resets_first_move_of_genome(self):
        self.versus_test(axelrod.Defector(), expected_actions=[(C, D)] + [(D, D)] * 4)

        p1 = self.player()
        self.assertEqual(p1.genome, [D, C, C, C, D])
        p1.reset()
        self.assertEqual(p1.history, [])
        self.assertEqual(p1.genome, [C, C, C, C, D])

    def test_all_darwin_instances_share_one_genome(self):
        p1 = self.player()
        p2 = self.player()
        self.assertIs(p1.genome, p2.genome)

        self.versus_test(axelrod.Defector(), expected_actions=[(C, D)] + [(D, D)] * 4)

        self.assertEqual(p2.genome, [D, C, C, C, D])
        self.assertIs(p1.genome, p2.genome)
        p3 = self.player()
        self.assertIs(p3.genome, p2.genome)

    def test_reset_genome(self):
        self.versus_test(axelrod.Defector(), expected_actions=[(C, D)] + [(D, D)] * 4)
        self.player.reset_genome()
        self.assertEqual(self.player().genome, [C])
