"""
Tests for the file utils.py
"""

import unittest
from assortative_mating.helpers.utils import *

class test_random_choice(unittest.TestCase):
	"""
	Simple tests for random_choice.
	"""

	def setUp(self):

		##A dummy list of objects
		self.objects = ['t',7, {'a':5,'b':12}, 'A horse' ]

	def tearDown(self):
		pass

	def test_random_choice_returns_something_sensible(self):
		"""
		Choose from a collection of objects, and assert that the choice is
		one of those objects.
		
		"""

		self.assertIn( random_choice(self.objects), self.objects  )

	def test_choose_handles_constant_probabilities(self):
		"""
		Test that the choose function can handle constant probabilities.
		"""

		self.assertIn( random_choice( self.objects, p = [0,0,0,0]), self.objects )
		self.assertIn( random_choice( self.objects, p = [1,1,1,1]), self.objects )

	def test_choose_handles_negative_numbers(self):
		"""
		Test that the function will correctly handle negative numbers.
		"""

		self.assertIn( random_choice( self.objects, p = [ -1,-2,-3,-4 ] ), self.objects )
		self.assertIn( random_choice( self.objects, p = [ -1,-1,-1,-1 ] ), self.objects )

	def test_choose_picks_right_ratio(self):
		"""
		Use a dummy case, check the resulting proportions.

		"""

		choices = [ random_choice( self.objects, p = [0,1,2,3] ) for _ in range(100000) ]
		counts = [ choices.count( o ) for o in self.objects ]
		##The first one should be not be in the list, as the weight is zero
		self.assertEquals( counts[0], 0 )
		##The ratios should be as follows
		self.assertAlmostEqual( counts[1]*2/counts[2], 1, places = 1 )
		self.assertAlmostEqual( counts[1]*3/counts[3] , 1, places = 1)
		self.assertAlmostEqual( counts[2]*3/2./counts[3], 1, places = 1 )

	def test_choose_can_return_index(self):
		"""
		Test that random_choice can return the index of the value it chooses.
		"""

		index, value = random_choice( [2,3,4], with_index = True )
		self.assertEquals( index + 2, value )

	def test_random_choice_can_be_given_length(self):
		"""
		"""

		self.assertEqual( len( random_choice( range(10), length = 20 ) ) , 20 )




