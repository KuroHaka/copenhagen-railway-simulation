from unittest.mock import MagicMock
import os, sys, unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Simulation import Simulation

class Test_simulation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.sim = Simulation()

        self.sim.plt.show = MagicMock()
        self.sim.animator.FuncAnimation = MagicMock()
        self.sim.run_simulation_with_animation(10, 10, output_fig=False)

    def test_animation_rendering(self):
        self.sim.animator.FuncAnimation()

    def test_visualization_showing(self):
        self.sim.plt.show.assert_called()


unittest.main()