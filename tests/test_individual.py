"""
Script for testing the functionality of the Individual class.

"""
import unittest
from assortative_mating import *
import numpy as np
from numpy import random
from assortative_mating.objects.individual import constant_assortment_individual

class test_individual(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_individual_can_be_constructed(self):
		"""
		Simply gives the Individual calls some constants and asserts that
		the Individual has been constructed correctly.

		"""
		a1, a2 = ( 0.2, 0.5 )
		m1, m2 = ( 0, 1 )
		newIndividual = Individual( a1, a2, m1, m2 )

		self.assertIsInstance( newIndividual, Individual )
		self.assertEquals( a1, newIndividual.a1 )
		self.assertEquals( a2, newIndividual.a2 )
		self.assertEquals( m1, newIndividual.m1 )
		self.assertEquals( m2, newIndividual.m2 )

	def test_individual_raises_ValueError_with_invalid_genes(self):
		"""
		Test that the Individual constructor raises ValueError when passed
		a value of a gene outside of the permitted range. 
		
		"""
		invalid_a1 = -0.9
		invalid_a2 = 1.1
		invalid_m1 = 0.5
		invalid_m2 = 2

		valid_a = 0.5
		valid_m = 1

		with self.assertRaises(ValueError):
			newIndividual = Individual( invalid_a1, valid_a, valid_m, valid_m )

		with self.assertRaises(ValueError):
			newIndividual = Individual( valid_a, invalid_a2, valid_m, valid_m )

		with self.assertRaises(ValueError):
			newIndividual = Individual( valid_a, valid_a, invalid_m1, valid_m )

		with self.assertRaises(ValueError):
			newIndividual = Individual( valid_a, valid_a, valid_m, invalid_m2 )


	def test_random_constructor(self):
		"""
		Test that the random constructor behaves as expected. I.e. it outputs
		genes within the given permitted range.

		"""
		
		##Make an Individual from random
		newIndividual = Individual.from_random()
		self.assertIsInstance( newIndividual, Individual )

		##Make an array of random Individuals and check they lie within reasonable
		##bounds
		all_Individuals = [ Individual.from_random() for i in range( 1000 ) ]
		a1s = [ al.a1 for al in all_Individuals ]
		a2s = [ al.a2 for al in all_Individuals ]
		m1s = [ al.m1 for al in all_Individuals ]
		m2s = [ al.m2 for al in all_Individuals ]

		##These are generated from random, so the mean should be close to 0.5
		self.assertAlmostEqual( np.mean(a1s), 0.5, places = 1 )
		##And the variance should be close to 1/3 - 1/4
		self.assertAlmostEqual( np.var(a2s), 1/3. - 1/4., places = 1 )
		##Check out the value of m
		self.assertAlmostEqual( np.mean(m1s), 0.5, places = 1 )
		self.assertAlmostEqual( np.var( m2s ), 0.25, places = 1 )

	def test_desired_assortment(self):
		"""
		An Individual should have the desired assortment given by q*a1 + (1-q)*a2
		Where a1 is the larger of the two alleles.

		"""

		##Do this by testing a few standard cases
		I1 = Individual( 0.4, 0.7, 1, 1 )
		I2 = Individual( 0.4, 0.7, 1, 1, q = 0.7 )
		I3 = Individual( 0.7, 0.0, 1, 0 )
		I4 = Individual( 0.7, 0.0, 1, 0, q = 1. )
		I5 = Individual( 0.7, 0.0, 1, 0, q = 0. )

		##Using the default value of one half
		self.assertEquals( I1.desired_assortment, 0.5*( 0.4 + 0.7 ) )
		self.assertEquals( I2.desired_assortment, 0.7*0.7 + ( 1 - 0.7 )*0.4 )

		self.assertEquals( I3.desired_assortment, 0.7*0.5)
		self.assertEquals( I4.desired_assortment, 0.7 )
		self.assertEquals( I5.desired_assortment, 0. )

	def test_phenotypic_value(self):
		"""
		Tests the Individuals phenotypic. This is straightforward, I just need to 
		comapre with the 4 possible scenarios.
		
		"""

		I1 = Individual( 0.4, 0.7, 1, 1 )
		I2 = Individual( 0.4, 0.7, 1, 0 )
		I3 = Individual( 0.7, 0.0, 0, 1 )
		I4 = Individual( 0.7, 0.0, 0, 0 )

		self.assertEquals( I1.phenotypic_value, 1 )
		self.assertEquals( I2.phenotypic_value, 0.5 )
		self.assertEquals( I3.phenotypic_value, 0.5 )
		self.assertEquals( I4.phenotypic_value, 0 )

	def test_choose_mate(self):
		"""
		Test the choose mate function. We create some dummy Individuals, and one dummy
		list of Individuals to choose from. We check that in each case the expected mate
		chossen is (statistically) of the right type.
		"""

		#There should be plenty to choose from here so no issues
		mates = [ Individual.from_random() for i in range( 128 ) ]
		##Calculate the average phenotypic value
		p_values = [m.phenotypic_value for m in mates]
		mean_p = np.mean(p_values)

		##An Individuals with desired assortment of 1
		#and phenotpye of one
		I_max_one = Individual( 1, 1, 1, 1 )
		##Likewise but with phentype equal 1/2
		I_max_half = Individual( 1, 1, 0, 1 )
		##And with phenotpye zero
		I_max_zero = Individual( 1, 1, 0, 0)

		#The function should return a tuple, the index of the mate, and
		##the mate itself, hence the index 1
		self.assertEquals( I_max_one.choose_mate(mates)[1].phenotypic_value, 1 )  
		self.assertEquals( I_max_half.choose_mate(mates)[1].phenotypic_value, 0.5 )
		self.assertEquals( I_max_zero.choose_mate(mates)[1].phenotypic_value, 0. )

		##Now look at a random chooser, he should pick a value close to the mean
		I_min = Individual( 0, 0, 1, 0 )
		choices = [ I_min.choose_mate( mates )[1].phenotypic_value for _ in range( 50000 ) ]
		self.assertAlmostEqual( np.mean(choices), mean_p, places = 2)

		##In general the expected value for an Individual with desired assortment A
		##and phenotypic value p, given a mean phenotypic value p_bar, should be equal
		##to: A*p + (1-A)*p_bar.
		A = random.random()
		I = Individual( A, A, random.randint(2), random.randint(2) )
		P = I.phenotypic_value
		expected = A*P + ( 1 - A )*mean_p
		measured = np.mean( [ I.choose_mate(mates)[1].phenotypic_value for _ in range(50000) ] )
		self.assertAlmostEqual( expected, measured, places = 2 )

		##Check behaviour when there is no one appropriate to pick
		I = Individual( 1, 1, 1, 1 )
		mates = [ Individual(0,1,0,1), Individual(0,1,1,0) ]
		self.assertEquals( I.choose_mate( mates )[1].phenotypic_value, 0.5 )

	def test_make_gamete_without_crossover(self):
		"""
		Call the Individuals make gamete method. This should return a haplotype.
		The probability of each halpotype should depend on the value of delta.

		"""

		##Some example Individuals
		I0 = Individual( 1, 0, 0, 0 )
		I1 = Individual( 1, 1, 0, 1 ) 
		I2 = Individual( 0, 1, 1, 0 ) 
		I3 = Individual( 0, 0, 1, 1 )

		#With delta = 0 these should be chossen at random
		delta = 0
		total_samples = 100000
		I0_gametes = [ I0.make_gamete( delta = delta, mu_strat = 0, mu_assort = 0 ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I0_gametes.count( (1,0) )/total_samples, 0.5, places = 2  )
		self.assertAlmostEqual( I0_gametes.count( (0,0) )/total_samples, 0.5, places = 2  )

		I2_gametes = [ I2.make_gamete( delta = delta, mu_strat = 0, mu_assort = 0 ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I2_gametes.count( (0,1) )/total_samples, 0.5, places = 2 )
		self.assertAlmostEqual( I2_gametes.count( (1,0) )/total_samples, 0.5, places = 2 )  

		##Try with an intermediate value of delta
		delta = 0.4
		I2_gametes = [ I2.make_gamete( delta = delta, mu_strat = 0, mu_assort = 0 ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I2_gametes.count( (0,1) )/total_samples, 0.5*(1-delta), places = 2 )
		I1_gametes = [ I1.make_gamete( delta = delta, mu_strat = 0, mu_assort = 0 ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I1_gametes.count( (1,0) )/total_samples, 0.5*(1+delta), places = 2 )


		##With extreme value of delta
		delta = 1
		self.assertEqual( I1.make_gamete( delta = delta, mu_strat = 0, mu_assort = 0 ), ( 1, 0 ) )
		I0_gametes = [ I0.make_gamete( delta = delta, mu_strat = 0, mu_assort = 0 ) for _ in range(total_samples) ]
		self.assertAlmostEqual( I0_gametes.count( (1,0) )/total_samples, 0.5, places = 2 )

	def test_make_gametes_with_crossover(self):
		"""
		Tests the make gametes function with the differring values of crossover.
		"""
		
		crossover = 0
		#Test Individual
		I = Individual(1,0,1,0, crossover = crossover)
		gametes = [ I.make_gamete(delta = 0, mu_strat = 0, mu_assort = 0) for _ in range(1000) ]
		self.assertNotIn( (1,0), gametes )
		self.assertNotIn( (0,1), gametes )

		crossover = 0.6
		#Test Individual
		I = Individual(1,0,1,0, crossover = crossover)
		##Wtih zero delta we should see the haplotype (1,1) more often than the
		##haplotype (1,0). 60% of the time we'll choose at random, so we should see
		##the haplotype 1,0 15% of the time
		total_samples = 50000
		gametes = [ I.make_gamete(delta = 0, mu_strat = 0, mu_assort = 0) for _ in range(total_samples) ]
		self.assertAlmostEqual( gametes.count( (1,0) )/total_samples, 0.15, places = 2 )

		crossover = 1.0
		##Regardless of delta we should see the two variants of a appearing equally often
		I = Individual(1,0,1,0, crossover = crossover)
		gametes = [ I.make_gamete(delta = random.random(), mu_strat = 0, mu_assort = 0 ) for _ in range(total_samples) ]
		ms = [ g[0] for g in gametes ]
		self.assertAlmostEqual( ms.count(1)/total_samples, 0.5, places = 2 )

	def test_fitness_is_correct(self):
		"""
		Test that the Individual computes its fintess correctly from a matrix.

		"""

		##The matix is assumed to be symmetric
		fitness_matrix = np.array( [ [1.1 , 0.1 ],[0.1, 0.0] ] )

		I0 = Individual( 1,1, 0, 0 )
		I1 = Individual( 1,1, 0, 1 )
		I2 = Individual( 1,1, 1, 0 )
		I3 = Individual( 1,1, 1, 1 )

		self.assertEqual( I0.fitness(fitness_matrix), 1.1 )
		self.assertEqual( I1.fitness(fitness_matrix), 0.1 )
		self.assertEqual( I2.fitness(fitness_matrix), 0.1 ) 
		self.assertEqual( I3.fitness(fitness_matrix), 0 ) 

class test_individual_helpers(unittest.TestCase):
	"""
	Class for testing all the helper functions in the Individual.py file.
	"""

	def setUp(self):
		pass

	def test_can_create_constant_assortment_individual(self):
		"""
		Test that we can return an Individual with constant assortment.
		"""

		inds = [ constant_assortment_individual(0.3, crossover = 0.3) for _ in range(100) ]
		self.assertAlmostEqual( np.mean( [ i.desired_assortment for i in inds] ), 0.3 )
		self.assertAlmostEqual( np.var( [ i.desired_assortment for i in inds] ), 0. )
		self.assertEqual( inds[0].crossover, 0.3 )

class test_mutation(unittest.TestCase):

	def setUp(self):
		self.test_gamete = ( 0.4, 1 )
		##Make an array of mutated gamete to test with
		self.total_trials = 50000
		self.mutated = [ Individual.mutate_gamete( self.test_gamete, mu_strat = 0.3, mu_assort = 0.2 ) for _ in range(self.total_trials) ]
		self.mutated_strategies = [ m[1] for m in self.mutated ]
		self.mutated_assort = [ m[0] for m in self.mutated ]

	def _is_gamete(self,g):
		"""
		Check to see if the input is a valid gamete.
		"""
		
		if not isinstance(g,tuple):
			return False
		elif len(g) != 2:
			return False
		elif g[0] < 0 or g[0] > 1:
			return False
		elif g[1] not in [0,1]:
			return False
		else:
			return True


	def test_mutation_returns_gamete(self):
		"""
		Test that the mutation function returns some kind of valid gamete.
		"""
		self.assertTrue( self._is_gamete( Individual.mutate_gamete( self.test_gamete ) ) )

	def test_mutation_does_nothing_with_zero_parameters(self):
		"""
		If both of the mutation parameters are set to zero, the returned gamete should be the same as the
		input.

		"""

		self.assertEqual( Individual.mutate_gamete( self.test_gamete, 0, 0 ), self.test_gamete )

	def test_mutate_strat(self):
		"""
		Test strategy mutation. If we repeatedly mutate our test gamete we can test that this is within
		sensible bounds.

		"""

		total_mutated = self.mutated_strategies.count(0)/self.total_trials
		self.assertAlmostEqual( total_mutated, 0.3, places = 2 )

	def test_mutate_assort(self):
		"""
		Check the statisitcal properties of the mutated assortment genes.
		"""

		#The mean should be roughly the same
		self.assertAlmostEqual( np.mean( self.mutated_assort ), 0.4, places = 2 )

		##The number mutated should be roughly equal to this
		self.assertAlmostEqual( self.mutated_assort.count(0.4)/self.total_trials, 0.8, places = 2 )

		##The standard deviation of those that are mutated should be close to this
		self.assertAlmostEqual( np.std( [ g_m for g_m in self.mutated_assort if g_m != 0.4 ] ), 0.05, places = 2 )

	def test_mutate_assort_doesnt_leave_intervale(self):
		"""
		Make sure that gametes close to the boundary don't leave the interval.

		"""

		Min =  min( [ Individual.mutate_gamete( (0,1) )[0] for _ in range(1000) ] )
		self.assertEquals(Min , 0)

		Max =  max( [ Individual.mutate_gamete( (1,1) )[0] for _ in range(1000) ] )
		self.assertEquals(Max, 1)