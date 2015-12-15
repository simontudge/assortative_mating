"""
Collection of tests for the model class.
"""

from assortative_mating import model, population

import unittest
import numpy as np

class test_model(unittest.TestCase):

	def setUp(self):
		self.random_pop = population.from_random(128)

	def tearDown(self):
		pass

	def test_model_can_be_constructed(self):
		"""
		Simply pass some variables to the model, and check that the
		model constructs.
		"""
		h,s,delta = 0.5, 0.4, 0.3
		myModel = model( self.random_pop, h, s, delta )
		self.assertIsInstance( myModel, model )
		##This is the expected outcome of the fitness matrix
		expected_matrix = np.array([ [ 1 - s, 1 - h*s ], [ 1 - h*s, 1 ] ])
		print (myModel.fitness_matrix)
		print (expected_matrix)
		self.assertTrue( np.all( myModel.fitness_matrix == expected_matrix ) )

	def test_raises_expected_valueerrors(self):

		##Delta too big
		with self.assertRaises( ValueError ):
			model( self.random_pop, h = 0.5, s = 0.5, delta = 1.1 )

		##Delta too small
		with self.assertRaises( ValueError ):
			model( self.random_pop, h = 0.5, s = 0.5, delta = -.1 )		

		##s too big
		with self.assertRaises( ValueError ):
			model( self.random_pop, h = 0.5, s = 1.1, delta = 0.9 )		

		##s too small
		with self.assertRaises( ValueError ):
			model( self.random_pop, h = 0.5, s = -0.05, delta = 0.9 )

		##h*s too big
		with self.assertRaises( ValueError ):
			model( self.random_pop, h = 1.5, s = 0.9, delta = 0.9 )

	def test_can_construct_with_random_pop(self):
		"""
		Assert that we can constuct the class from a random population.
		"""
		myModel = model.from_random_pop( 16, h = 0.4, s = 0.4, delta =0.2)
		self.assertIsInstance( myModel, model )
		self.assertEqual( myModel.size, 16 )


	##This just tests that it runs, proper function testing must take place
	##in a notebook.
	def test_go(self):
		"""
		Can't really test the whole model automatically in any detail, but
		check that the whole thing can run, and the population stays the same
		size

		"""

		myModel = model.from_random_pop( 16, h = 0.4, s = 0.4, delta =0.2)
		myModel.go()
		self.assertEqual( len( myModel.population ), len( myModel.pop0 ) )
		##Check that something has happened at least
		self.assertNotEqual( myModel.population, myModel.pop0 )

	def test_records_fairness(self):
		"""
		Test that the model record fairness, simply by asserting that the model
		has a list of the length of the number of generations.

		"""

		gens = 26
		pop = population.from_random(32)
		fairness0 = pop.fairness
		myModel = model( pop, h = 0.4, s = 0.6, delta = 0.3, generations = gens)
		myModel.go()
		self.assertEqual( len( myModel.fairness ), gens )
		self.assertEqual( fairness0, myModel.fairness[0] )

	def test_model_sets_final_results(self):
		"""
		The othe classes will be looing for certain key words after the simulation has stopped.
		Check that they exist, and are sensible vaules.
		"""

		myModel = model.from_random_pop( 16, 0.4, 0.5, 0.1 )
		myModel.go()
		self.assertGreaterEqual( myModel.final_fairness, 0 )
		self.assertLessEqual( myModel.final_fairness, 1 )