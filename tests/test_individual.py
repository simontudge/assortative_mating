"""
Script for testing the functionality of the individual class.

"""
import unittest
from code import *
import numpy as np
from numpy import random

class test_individual(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_individual_can_be_constructed(self):
		"""
		Simply gives the individual calls some constants and asserts that
		the individual has been constructed correctly.

		"""
		a1, a2 = ( 0.2, 0.5 )
		m1, m2 = ( 0, 1 )
		newIndividual = individual( a1, a2, m1, m2 )

		self.assertIsInstance( newIndividual, individual )
		self.assertEquals( a1, newIndividual.a1 )
		self.assertEquals( a2, newIndividual.a2 )
		self.assertEquals( m1, newIndividual.m1 )
		self.assertEquals( m2, newIndividual.m2 )

	def test_individual_raises_ValueError_with_invalid_genes(self):
		"""
		Test that the individual constructor raises ValueError when passed
		a value of a gene outside of the permitted range. 
		
		"""
		invalid_a1 = -0.9
		invalid_a2 = 1.1
		invalid_m1 = 0.5
		invalid_m2 = 2

		valid_a = 0.5
		valid_m = 1

		with self.assertRaises(ValueError):
			newIndividual = individual( invalid_a1, valid_a, valid_m, valid_m )

		with self.assertRaises(ValueError):
			newIndividual = individual( valid_a, invalid_a2, valid_m, valid_m )

		with self.assertRaises(ValueError):
			newIndividual = individual( valid_a, valid_a, invalid_m1, valid_m )

		with self.assertRaises(ValueError):
			newIndividual = individual( valid_a, valid_a, valid_m, invalid_m2 )


	def test_random_constructor(self):
		"""
		Test that the random constructor behaves as expected. I.e. it outputs
		genes within the given permitted range.

		"""
		
		##Make an individual from random
		newIndividual = individual.from_random()
		self.assertIsInstance( newIndividual, individual )

		##Make an array of random individuals and check they lie within reasonable
		##bounds
		all_individuals = [ individual.from_random() for i in range( 1000 ) ]
		a1s = [ al.a1 for al in all_individuals ]
		a2s = [ al.a2 for al in all_individuals ]
		m1s = [ al.m1 for al in all_individuals ]
		m2s = [ al.m2 for al in all_individuals ]

		##These are generated from random, so the mean should be close to 0.5
		self.assertAlmostEqual( np.mean(a1s), 0.5, places = 1 )
		##And the variance should be close to 1/3 - 1/4
		self.assertAlmostEqual( np.var(a2s), 1/3. - 1/4., places = 1 )
		##Check out the value of m
		self.assertAlmostEqual( np.mean(m1s), 0.5, places = 1 )
		self.assertAlmostEqual( np.var( m2s ), 0.25, places = 1 )

	def test_desired_assortment(self):
		"""
		An individual should have the desired assortment given by q*a1 + (1-q)*a2
		Where a1 is the larger of the two alleles.

		"""

		##Do this by testing a few standard cases
		I1 = individual( 0.4, 0.7, 1, 1 )
		I2 = individual( 0.4, 0.7, 1, 1, q = 0.7 )
		I3 = individual( 0.7, 0.0, 1, 0 )
		I4 = individual( 0.7, 0.0, 1, 0, q = 1. )
		I5 = individual( 0.7, 0.0, 1, 0, q = 0. )

		##Using the default value of one half
		self.assertEquals( I1.desired_assortment, 0.5*( 0.4 + 0.7 ) )
		self.assertEquals( I2.desired_assortment, 0.7*0.7 + ( 1 - 0.7 )*0.4 )

		self.assertEquals( I3.desired_assortment, 0.7*0.5)
		self.assertEquals( I4.desired_assortment, 0.7 )
		self.assertEquals( I5.desired_assortment, 0. )

	def test_phenotypic_value(self):
		"""
		Tests the individuals phenotypic. This is straightforward, I just need to 
		comapre with the 4 possible scenarios.
		
		"""

		I1 = individual( 0.4, 0.7, 1, 1 )
		I2 = individual( 0.4, 0.7, 1, 0 )
		I3 = individual( 0.7, 0.0, 0, 1 )
		I4 = individual( 0.7, 0.0, 0, 0 )

		self.assertEquals( I1.phenotypic_value, 1 )
		self.assertEquals( I2.phenotypic_value, 0.5 )
		self.assertEquals( I3.phenotypic_value, 0.5 )
		self.assertEquals( I4.phenotypic_value, 0 )

	def test_choose_mate(self):
		"""
		Test the choose mate function. We create some dummy individuals, and one dummy
		list of individuals to choose from. We check that in each case the expected mate
		chossen is (statistically) of the right type.
		"""

		#There should be plenty to choose from here so no issues
		mates = [ individual.from_random() for i in range( 128 ) ]
		##Calculate the average phenotypic value
		p_values = [m.phenotypic_value for m in mates]
		mean_p = np.mean(p_values)

		##An individuals with desired assortment of 1
		#and phenotpye of one
		I_max_one = individual( 1, 1, 1, 1 )
		##Likewise but with phentype equal 1/2
		I_max_half = individual( 1, 1, 0, 1 )
		##And with phenotpye zero
		I_max_zero = individual( 1, 1, 0, 0)

		#The function should return a tuple, the index of the mate, and
		##the mate itself, hence the index 1
		self.assertEquals( I_max_one.choose_mate(mates)[1].phenotypic_value, 1 )  
		self.assertEquals( I_max_half.choose_mate(mates)[1].phenotypic_value, 0.5 )
		self.assertEquals( I_max_zero.choose_mate(mates)[1].phenotypic_value, 0. )

		##Now look at a random chooser, he should pick a value close to the mean
		I_min = individual( 0, 0, 1, 0 )
		choices = [ I_min.choose_mate( mates )[1].phenotypic_value for _ in range( 50000 ) ]
		self.assertAlmostEqual( np.mean(choices), mean_p, places = 2)

		##In general the expected value for an individual with desired assortment A
		##and phenotypic value p, given a mean phenotypic value p_bar, should be equal
		##to: A*p + (1-A)*p_bar.
		A = random.random()
		I = individual( A, A, random.randint(2), random.randint(2) )
		P = I.phenotypic_value
		expected = A*P + ( 1 - A )*mean_p
		measured = np.mean( [ I.choose_mate(mates)[1].phenotypic_value for _ in range(50000) ] )
		self.assertAlmostEqual( expected, measured, places = 2 )

		##Check behaviour when there is no one appropriate to pick
		I = individual( 1, 1, 1, 1 )
		mates = [ individual(0,1,0,1), individual(0,1,1,0) ]
		self.assertEquals( I.choose_mate( mates )[1].phenotypic_value, 0.5 )

	def test_make_gamete_without_crossover(self):
		"""
		Call the individuals make gamete method. This should return a haplotype.
		The probability of each halpotype should depend on the value of delta.

		"""

		##Some example individuals
		I0 = individual( 1, 0, 0, 0 )
		I1 = individual( 1, 1, 0, 1 ) 
		I2 = individual( 0, 1, 1, 0 ) 
		I3 = individual( 0, 0, 1, 1 )

		#With delta = 0 these should be chossen at random
		delta = 0
		total_samples = 100000
		I0_gametes = [ I0.make_gamete( delta = delta ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I0_gametes.count( (1,0) )/total_samples, 0.5, places = 2  )
		self.assertAlmostEqual( I0_gametes.count( (0,0) )/total_samples, 0.5, places = 2  )

		I2_gametes = [ I2.make_gamete( delta = delta ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I2_gametes.count( (0,1) )/total_samples, 0.5, places = 2 )
		self.assertAlmostEqual( I2_gametes.count( (1,0) )/total_samples, 0.5, places = 2 )  

		##Try with an intermediate value of delta
		delta = 0.4
		I2_gametes = [ I2.make_gamete( delta = delta ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I2_gametes.count( (0,1) )/total_samples, 0.5*(1-delta), places = 2 )
		I1_gametes = [ I1.make_gamete( delta = delta ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I1_gametes.count( (1,0) )/total_samples, 0.5*(1+delta), places = 2 )


		##With extreme value of delta
		delta = 1
		self.assertEqual( I1.make_gamete( delta = delta ), ( 1, 0 ) )
		I0_gametes = [ I0.make_gamete( delta = delta ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I0_gametes.count( (1,0) )/total_samples, 0.5, places = 2 )

	def test_make_gametes_with_crossover(self):
		"""
		Tests the make gametes function with the differring values of crossover.
		"""
		
		crossover = 0
		#Test individual
		I = individual(1,0,1,0, crossover = crossover)
		gametes = [ I.make_gamete(delta = 0) for _ in range(1000) ]
		self.assertNotIn( (1,0), gametes )
		self.assertNotIn( (0,1), gametes )

		crossover = 0.6
		#Test individual
		I = individual(1,0,1,0, crossover = crossover)
		##Wtih zero delta we should see the haplotype (1,1) more often than the
		##haplotype (1,0). 60% of the time we'll choose at random, so we should see
		##the haplotype 1,0 15% of the time
		total_samples = 50000
		gametes = [ I.make_gamete(delta = 0) for _ in range(total_samples) ]
		self.assertAlmostEqual( gametes.count( (1,0) )/total_samples, 0.15, places = 2 )

		crossover = 1.0
		##Regardless of delta we should see the two variants of a appearing equally often
		I = individual(1,0,1,0, crossover = crossover)
		gametes = [ I.make_gamete(delta = random.random() ) for _ in range(total_samples) ]
		ms = [ g[0] for g in gametes ]
		self.assertAlmostEqual( ms.count(1)/total_samples, 0.5, places = 2 )

	def test_fintess_is_correct(self):
		"""
		Test that the individual computes its fintess correctly from a matrix.

		"""

		##The matix is assumed to be symmetric
		fitness_matrix = np.array( [ [1.1 , 0.1 ],[0.1, 0.0] ] )

		I0 = individual( 1,1, 0, 0 )
		I1 = individual( 1,1, 0, 1 )
		I2 = individual( 1,1, 1, 0 )
		I3 = individual( 1,1, 1, 1 )

		self.assertEqual( I0.fitness(fitness_matrix), 1.1 )
		self.assertEqual( I1.fitness(fitness_matrix), 0.1 )
		self.assertEqual( I2.fitness(fitness_matrix), 0.1 ) 
		self.assertEqual( I3.fitness(fitness_matrix), 0 ) 

class test_mutation(unittest.TestCase):

	def test_mutate_gamete(self):
		"""
		Test that the mutation of gametes behaves as expected.
		"""
		pass