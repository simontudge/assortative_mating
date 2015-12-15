"""
File for testing the pair class. Mostly it's functionality is quite trivial, so these
tests are quite simple.

"""

import unittest
import numpy as np

from code import pair, individual


class test_pair(unittest.TestCase):

	def setUp(self):
		"""
		Setup by creating some dummy individuals that can be called later.
		"""
		self.I1 = individual( 1,0, 0, 1 )
		self.I2 = individual( 1,1, 0, 0 )

	def tearDown(self):
		pass

	def test_can_be_constructed_from_two_individuals(self):
		"""
		Test that the basic constructor works by passing two individuals.
		
		"""
		myPair = pair(self.I1, self.I2)
		self.assertIsInstance(myPair, pair)

	def test_raise_TypeError_if_inputs_not_individuals(self):
		"""
		Assert that the constructor raises a type error if the user
		attempts to construct with objects that are not of type individual.
		"""

		with self.assertRaises( TypeError ):
			pair( self.I1, 3 )
		with self.assertRaises( TypeError ):
			pair( (1,1,0,1), self.I2 )

	def test_can_be_constructed_from_random(self):
		"""
		Call the random constructor and check that it returns the right type.

		"""
		myPair = pair.from_random()
		self.assertIsInstance( myPair, pair )

	def test_fitness_is_mean_of_individual(self):
		"""
		Define a payoff matrix, and check that the fitness returned is the
		correct value simply by computing by hand.
		
		"""
		myPair = pair( self.I1, self.I2 )
		fitness_matrix = np.array( [ [ 1.1, 0.1 ],[0.1, 0 ] ] )
		pair_fitness = myPair.fitness( fitness_matrix )
		expected = 0.6
		self.assertAlmostEqual( pair_fitness, expected )

	def test_make_child_returns_individual(self):
		"""
		call the make child method, and assert that the returned type is 
		of type individual.

		"""

		myPair = pair( self.I1, self.I2 )
		child = myPair.make_child(delta = 0.5)
		self.assertIsInstance(child, individual)

	def test_make_child_return_sensible_genes(self):
		"""
		Use an extreme case to test that make child is not doing something silly.
		
		"""
		I1 = individual(1,1,1,1)
		I2 = individual(0,0,0,0)
		myPair = pair(I1,I2)
		##Repeat a few time to be safe
		for _ in range(64):
			child = myPair.make_child(delta = 0.5)
			##The child must have an a value of 1 and one of 0 and likewise for m
			self.assertEqual( child.a1 + child.a2, 1 )
			self.assertEqual( child.m1 + child.m2, 1 )