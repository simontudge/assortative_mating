"""
Script for testing the functionality of the individual class.

"""
import unittest
from code import *

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