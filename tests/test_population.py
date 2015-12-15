"""
File for testing the population class.
"""

import unittest
from code import population, individual

class test_population(unittest.TestCase):
	
	def setUp(self):
		"""
		Make some dummy lists of individuals and popualtions, that can be tested repeastedly.
		"""
		self.random_individuals = [ individual.from_random() for _ in range(128) ]
		self.random_pop = population.from_random(128)

	def tearDown(self):
		pass

	def test_can_be_intitialised_from_list(self):
		"""
		Test that the population can be initialised from a list of individuals.
		"""
		myPop = population( self.random_individuals )
		self.assertIsInstance( myPop, population )

	def test_can_be_initialised_from_random(self):
		"""
		Test that the population can be initialised from random individuals.
		
		"""

		myPop = population.from_random( size = 128 )
		self.assertIsInstance(myPop, population)

	def test_initialiser_raises_value_error_with_odd_individuals(self):
		"""
		Population must be created with an even number of individuals. Test that valueerror 
		is raised if this is not the case.
		"""

		list_of_individuals = [ individual.from_random() for _ in range(127) ]
		with self.assertRaises(ValueError):
			myPop = population( list_of_individuals )

		with self.assertRaises(ValueError):
			myPop = population.from_random(127)

	def test_divide_population(self):
		"""
		Tests that the population can be divided into two.
		"""

		self.random_pop.divide_population()
		self.assertEqual( len( self.random_pop.females ) , 64 )
		self.assertEqual( len( self.random_pop.males ) , 64 )

		self.assertIsInstance( self.random_pop.females[4], individual )
		self.assertIsInstance( self.random_pop.males[12], individual )
