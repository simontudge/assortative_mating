"""
Fule for testing the game theoretic function in helper.game_theory_helpers.
These are mostly fairly trivial mathematical functions, so these tests simple
check that they obey certain minimum requirments.
"""

import unittest

from assortative_mating.helpers.game_theory_helpers import *

class test_game_theory(unittest.TestCase):

	def setUp(self):
		pass

	def test_hsdelta_ST_transform_returns_plausible_results(self):
		"""
		The function that transfroms h, s and delta into S and T must obey
		a few basic properties, test them here.

		"""

		##If delta = 0 then S=T
		S,T = get_ST(h = 0.92323,s = .723723,delta = 0)
		self.assertEqual(S,T)

		#h = 0 corresponds to S + T = 2
		S,T = get_ST(h = 0.,s = .323, delta = 0.55)
		self.assertAlmostEqual( S + T, 2 )

		##h = 1/2 corresponds to S+T = 1
		S,T = get_ST(h = 0.5,s = .25,delta = 0.11)
		self.assertAlmostEqual( S + T , 1 )

	def test_ESS(self):
		"""
		Test that the ESS function returns sensible results for various fixed games.
		
		"""

		##Harmony, S > 0, T < 1
		self.assertEqual( ESS( 0.5, 0.9 ), 1 )

		##PD, S < 0, T > 1
		self.assertEqual( ESS( -0.5, 1.9 ), 0 )

		##Staghunt, favours defect S < 0, T < 1 and T - S > 1
		self.assertEqual( ESS( S = -.6, T = .65 ), 0  )

		##Staghunt, favours cooperate S < 0, T < 1 and T - S < 1 
		self.assertEqual( ESS( S = -.3, T = .35 ), 1 )

		##Snowdrift, with equal proportions ( T - S = 1 ), S > 0, T > 1
		self.assertAlmostEqual( ESS( 0.3, 1.3 ), 0.5 )