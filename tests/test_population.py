"""
File for testing the population class.
"""

import unittest
from assortative_mating import Population, Individual, Pair

import numpy as np
import matplotlib as mpl

class test_population(unittest.TestCase):
	
	def setUp(self):
		"""
		Make some dummy lists of individuals and popualtions, that can be tested repeastedly.
		"""
		self.random_individuals = [ Individual.from_random() for _ in range(128) ]
		self.random_pop = Population.from_random(128)

		I1 = Individual( 1,1 , 0,0 )
		I2 = Individual( 1,1 , 0,0 )
		I3 = Individual( 1,0 , 0,1 )
		I4 = Individual( 0,0 , 1,0 ) 

		self.small_pop = Population( [I1,I2,I3,I4] ) 

	def tearDown(self):
		pass

	def test_can_be_intitialised_from_list(self):
		"""
		Test that the population can be initialised from a list of individuals.
		"""
		myPop = Population( self.random_individuals )
		self.assertIsInstance( myPop, Population )

	def test_can_be_initialised_from_random(self):
		"""
		Test that the population can be initialised from random individuals.
		
		"""

		myPop = Population.from_random( size = 128 )
		self.assertIsInstance(myPop, Population)

	def test_initialiser_raises_value_error_with_odd_individuals(self):
		"""
		Population must be created with an even number of individuals. Test that valueerror 
		is raised if this is not the case.
		"""

		list_of_individuals = [ Individual.from_random() for _ in range(127) ]
		with self.assertRaises(ValueError):
			myPop = Population( list_of_individuals )

		with self.assertRaises(ValueError):
			myPop = Population.from_random(127)

	def test_population_length_works(self):
		"""
		Test that the len function works on a population.

		"""
		self.assertEquals( len(self.random_pop), 128 )

	def test_divide_population(self):
		"""
		Tests that the population can be divided into two.
		"""

		self.random_pop.divide_population()
		self.assertEqual( len( self.random_pop.females ) , 64 )
		self.assertEqual( len( self.random_pop.males ) , 64 )

		self.assertIsInstance( self.random_pop.females[4], Individual )
		self.assertIsInstance( self.random_pop.males[12], Individual )

	def test_pair_population(self):
		"""
		Test that pair population creates a list of pairs of length one half of
		the population.

		"""

		self.random_pop.pair_population()
		self.assertEqual( len( self.random_pop.pairs ) , 64 )
		self.assertIsInstance( self.random_pop.pairs[16], Pair  )

	def test_pairing_is_sensible(self):
		"""
		Test that the pairing of individuals is sensible. The corelation of phentypes
		should be roughly equal to the average value of desired assortment.
		"""
		##Start fro scratch, incase this messes with something else
		pop = Population.from_random(10000)
		pop.pair_population()
		x = [ p[0].phenotypic_value for p in pop.pairs ]
		y = [ p[1].phenotypic_value for p in pop.pairs ]
		corr = np.corrcoef( x, y )[0,1]
		average_assortment = np.mean( [ I.desired_assortment for I in pop.individuals ] )
		##This seems to be a very approximate law, so let's be quite generous in what we allow
		self.assertAlmostEqual( corr, average_assortment, places = 1 )

	def test_get_mean_desired_assortment(self):
		"""
		Function that returns the average desired assortment, quite trivial so just test with one
		dummy population.
		"""

		self.assertAlmostEquals( self.small_pop.average_assortment, 0.625 )

	def test_fairness(self):
		"""
		Should return the average extent of fair meiosis. Check against the small population.

		"""

		self.assertEquals( self.small_pop.fairness, 0.25 )

	def test_plot_scatter_pairs_returns_figure(self):
		"""
		Test that the method plotter_scatter_pairs returns a matplotlib figure.
		We can't really do any better than that.
		"""

		fig = self.random_pop.plot_scatter_pairs()
		self.assertIsInstance( fig, mpl.figure.Figure )

	def test_new_generation_returns_population(self):
		"""
		Test that selecting the next generation returns a population.
		
		"""

		fitness_matrix = np.array( [[0.,0.1],[0.1,1.1]] )

		new_pop = self.random_pop.new_generation(fitness_matrix, delta = 0.1)
		self.assertIsInstance(new_pop, Population)
		self.assertEqual( len(new_pop), len( self.random_pop ) )

	def test_next_gen_returns_sensible_children(self):
		"""
		Call the next gen method for a population with three pairs.
		Assert that the returned frequencies are as expected.
		"""

		##All the individuals want maximum assortment
		I1 = Individual( 1,1, 0, 0 )
		I2 = Individual( 1,1, 0, 1 )
		I3 = Individual( 1,1, 1, 1 )

		##A popwith two of each kind should pair up exactly...
		pop = Population( [I1,I1,I2,I2,I3,I3] )
		##...so long as we set this bit by hand
		pop.males = [I1,I2,I3]
		pop.females = [I1,I2,I3]
		##Make the fitnesses exactly addative, for ease
		M = np.array( [ [ 0, 0.5 ],[ 0.5, 1. ] ] )
		delta = 0
		new_pops = [ pop.new_generation(M,delta = delta, mu_strat = 0, mu_assort = 0) for _ in range(5000) ]
		##We shhould have ratios of roughly 2:1:0 for phenotypic values of 1:0.5:0
		##Making the mean 2.5/3 = 
		mean_fairness = np.mean( [ p.fairness for p in new_pops ]  )
		self.assertAlmostEqual( mean_fairness, 2.5/3, places = 2 )