import unittest
import os
from .racetrack import RaceTrack

class TestRaceTrack(unittest.TestCase):

    def setUp(self):
        racetrack_csv = os.path.join(os.path.abspath(__file__), "..", "data", "figure05-05-left.csv")
        self.race = RaceTrack(racetrack_csv)

    def test_is_over_boundary(self):
        self.assertEqual(self.race.is_over_boundary((3, 30)), False)
        self.assertEqual(self.race.is_over_boundary((16, 26)), False)
        
        self.assertEqual(self.race.is_over_boundary((10, 25)), True)
        self.assertEqual(self.race.is_over_boundary((16, 0)), True)
        
        self.assertEqual(self.race.is_over_boundary((16, -1)), True)
        self.assertEqual(self.race.is_over_boundary((-1, 4)), True)

        self.assertEqual(self.race.is_over_boundary((1, 32)), True)
        self.assertEqual(self.race.is_over_boundary((17, 30)), True)
        
    def test_run(self):
        self.assertEqual(self.race.run((14, 28), (5, -5), 0)[0], (16, 26))

        # self.assertEqual(self.race.run((3, 14), (5, -4), 0)[0], (5, 16))
        # self.assertEqual(self.race.run((3, 14), (4, -5), 0)[0], (5, 16))
        # self.assertEqual(self.race.run((3, 14), (3, -5), 0)[1], (0, 0))
        
        # self.assertEqual(self.race.run((3, 13), (-5, 5), 0)[0], (0, 16))
        # self.assertEqual(self.race.run((3, 13), (-4, 5), 0)[0], (1, 16))
        # self.assertEqual(self.race.run((3, 13), (-5, 4), 0)[1], (0, 0))

        # self.assertEqual(self.race.run((31, 3), (-4, 4), 0)[0], (27, 7))
        # self.assertEqual(self.race.run((29, 3), (-1, -1), 0)[0], (28, 2))
        # self.assertEqual(self.race.run((7, 8), (-2, 2), 0)[0], (5, 10))
        
        # self.assertEqual(self.race.run((8, 8), (-4, 2), 0)[0], (4, 10))
        # self.assertEqual(self.race.run((8, 8), (-4, 3), 0)[1], (0, 0))
        
        # self.assertEqual(self.race.run((10, 7), (-4, 2), 0)[0], (6, 9))
     
        
    def test_play(self):
        #state, player_trajectory = self.race.play();
        #print(state)
        #print(len(player_trajectory))
        #pprint(player_trajectory[-10:])
        pass

    def test_get_actions(self):
        actions = self.race.get_actions(((4, 0), (0, 0)), 1);
        self.assertTrue((0, 0) not in actions)    
        actions = self.race.get_actions(((3, 0), (1, 1)), 1);
        self.assertTrue((-1, -1) not in actions)     
        actions = self.race.get_actions(((3, 0), (5, 1)), 1);
        self.assertTrue((1, -1) not in actions)     
        actions = self.race.get_actions(((3, 0), (-5, 1)), 1);
        self.assertTrue((-1, -1) not in actions)
        actions = self.race.get_actions(((3, 0), (-1, 5)), 1);
        self.assertTrue((-1, 1) not in actions) 
        actions = self.race.get_actions(((3, 0), (-1, -5)), 1);
        self.assertTrue((-1, -1) not in actions) 
        actions = self.race.get_actions(((3, 0), (5, -5)), 1);
        self.assertTrue((1, -1) not in actions) 
