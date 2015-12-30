"""
Collection of tests for the Model class.
"""

from assortative_mating import Model, Population, Individual

import unittest
import numpy as np
import matplotlib as mpl

class test_model(unittest.TestCase):

	def setUp(self):
		self.random_pop = Population.from_random(128)

	def tearDown(self):
		pass

	def test_model_can_be_constructed(self):
		"""
		Simply pass some variables to the model, and check that the
		model constructs.
		"""
		h,s,delta = 0.5, 0.4, 0.3
		myModel = Model( self.random_pop, h, s, delta )
		self.assertIsInstance( myModel, Model )
		##This is the expected outcome of the fitness matrix
		expected_matrix = np.array([ [ 1 - s, 1 - h*s ], [ 1 - h*s, 1 ] ])
		print (myModel.fitness_matrix)
		print (expected_matrix)
		self.assertTrue( np.all( myModel.fitness_matrix == expected_matrix ) )

	def test_raises_expected_valueErrors(self):

		##Delta too big
		with self.assertRaises( ValueError ):
			Model( self.random_pop, h = 0.5, s = 0.5, delta = 1.1 )

		##Delta too small
		with self.assertRaises( ValueError ):
			Model( self.random_pop, h = 0.5, s = 0.5, delta = -.1 )		

		##s too big
		with self.assertRaises( ValueError ):
			Model( self.random_pop, h = 0.5, s = 1.1, delta = 0.9 )		

		##s too small
		with self.assertRaises( ValueError ):
			Model( self.random_pop, h = 0.5, s = -0.05, delta = 0.9 )

		##h*s too big
		with self.assertRaises( ValueError ):
			Model( self.random_pop, h = 1.5, s = 0.9, delta = 0.9 )

	def test_can_construct_with_random_pop(self):
		"""
		Assert that we can constuct the class from a random population.
		"""
		myModel = Model.from_random_pop( 16, h = 0.4, s = 0.4, delta =0.2)
		self.assertIsInstance( myModel, Model )
		self.assertEqual( myModel.size, 16 )

	def test_can_be_contructed_from_function(self):
		"""
		Test that we can construct a model from a function that returns an
		individual.
		"""
		##Make a function that returns a constan individual
		def _const_ind():
			return Individual(1,1,1,1)
		myModel = Model.from_function( _const_ind, 12, 0.3,0.3,0.9 )
		self.assertIsInstance(myModel, Model)
		self.assertEqual( myModel.size, 12  )
		self.assertEqual( myModel.delta, 0.9 )
		self.assertEqual( myModel.Population.fairness, 1 )
		self.assertEqual( myModel.Population.average_assortment, 1 )

	##This just tests that it runs, proper function testing must take place
	##in a notebook.
	def test_go(self):
		"""
		Can't really test the whole Model automatically in any detail, but
		check that the whole thing can run, and the population stays the same
		size

		"""

		myModel = Model.from_random_pop( 16, h = 0.4, s = 0.4, delta =0.2)
		myModel.go()
		self.assertEqual( len( myModel.Population ), len( myModel.pop0 ) )
		##Check that something has happened at least
		self.assertNotEqual( myModel.Population, myModel.pop0 )

	def test_records_fairness(self):
		"""
		Test that the model record fairness, simply by asserting that the model
		has a list of the length of the number of generations.

		"""

		gens = 26
		pop = Population.from_random(32)
		fairness0 = pop.fairness
		myModel = Model( pop, h = 0.4, s = 0.6, delta = 0.3, generations = gens)
		myModel.go()
		self.assertEqual( len( myModel.fairness ), gens )
		self.assertEqual( fairness0, myModel.fairness[0] )

	def test_records_assortment(self):
		"""
		Check that the model records assortment.
		"""

		gens = 26
		pop = Population.from_random(32)
		assort0 = pop.average_assortment
		myModel = Model( pop, h = 0.4, s = 0.6, delta = 0.3, generations = gens)
		myModel.go()
		self.assertEqual( len( myModel.desired_assortment ), gens )
		self.assertEqual( assort0, myModel.desired_assortment[0] )

	def test_model_sets_final_results(self):
		"""
		The other classes will be looking for certain key words after the simulation has stopped.
		Check that they exist, and are sensible vaules.
		"""

		myModel = Model.from_random_pop( 16, 0.4, 0.5, 0.1 )
		myModel.go()
		self.assertGreaterEqual( myModel.final_fairness, 0 )
		self.assertLessEqual( myModel.final_fairness, 1 )

		self.assertGreaterEqual( myModel.final_desired_assortment, 0 )
		self.assertLessEqual( myModel.final_desired_assortment, 1 )

	def test_make_graph_returns_matplotlib_figure(self):
		"""
		Simply assert that the function returns a figure.

		"""

		myModel = Model.from_random_pop( 16, 0.4, 0.5, 0.1, graphs = False)
		myModel.go()
		fig = myModel.make_graphs()
		self.assertIsInstance( fig, mpl.figure.Figure )

	def test_model_handles_mutation(self):
		"""
		Run the model for one generation, and see that mutation is taking effect.
		"""

		mod = Model.from_random_pop( 16, 0.4, 0.5, 0.1, graphs = False,\
		 generations = 1, mu_strat = 0.5, mu_assort = 0 )
		mod.go()
		##We're bascially just checking that this runs, so this is just a minimal test
		self.assertIsInstance(mod,Model)