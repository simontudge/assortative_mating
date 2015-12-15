"""
File containing the class for the model. The model class is a thin-ish
wrapper for a population, but knows how to repeatedly call its methods in
order to simulate many generations. It knows what to record, and provides
some methods for creating graphs etc.

This is also where the parameters of the model live.
"""

import numpy as np
import matplotlib.pyplot as plt

from assortative_mating import population

class model():
	"""
	The full model. Contains a population and methods for running simulation, as
	well as parameters as methods for plotting and analysis.
	"""

	def __init__(self, pop, h, s, delta, generations = 128, make_graphs = True):
		"""
		Construct a model, the model class contains a population, and all the parameters
		needed to define a model. It handles iterating the model through multiple generations
		as well as making graphs and recording various statistics.
		Inputs
		======
		pop : population
			Any instance of the population class.
		h : float
			Standard parameter from population genetics. Determines the extend of over/under
			dominance. Often constrained to be between 0 and 1, although not a strict requirment.
		s : float
			Standard parameter from population genetics, determines the extent to which
			the less fit homozygote is less fit than the fitter one.
		delta : float [0,1]
			Determines the extent to which the meitic distorter is able to cheat meiosis.
			delta = 0 corresponds to the case of a completely ineffective distorter, and
			delta = 1 corresponds to a perfect distorter.
		pop_size : int {128}
			Number of individuals that the population contains.
		generations : int {128}
			Number of decrete generations over which to select.
		make_graphs : bool {True}
			Whether or not to create the standard array of graphs
		Raises
		======
		ValueError :
			If delta < 0 or delta > 1. If s < 0 or > 1 or if h*s > 1.
		"""

		##Raise value error if any of the conditions are violated
		if delta < 0 or delta > 1:
			raise ValueError ("Delta must be in [0,1], got {}".format(delta))
		if s < 0 or s > 1:
			raise ValueError ("s must be in [0,1], got {}".format(s))
		if h*s > 1:
			raise ValueError("h*s must be greater than 0, got {}".format(h*s))
		##Set all input parameters
		self.population = pop
		self.h = h
		self.s = s
		self.delta = delta
		self.generations = generations
		self.make_graphs = make_graphs
		##Check input values
		omega_00 = 1 - s
		omega_01 = 1 - h*s
		omega_10 = omega_01
		omega_11 = 1
		self.fitness_matrix = np.array( [[ omega_00, omega_01 ],[ omega_10, omega_11 ] ] )
		##Other usuful parametes
		self.size = pop.total_individuals
		##Save the intial state of the population
		self.pop0 = self.population

	def __repr__(self):
		"""
		Simple summary of key points of model.
		"""
		return "Model of size {}, with h = {}, s = {} and delta = {}".\
		format(self.size,self.h, self.s, self.delta)

	@classmethod
	def from_random_pop(cls, size, *args, **kwargs):
		"""
		Create the model from a random initial condition.
		Inputs
		======
		size : int
			size of the population
		*args, **kwargs :
			passed to default constructor of model
		"""
		pop = population.from_random(size)
		return model( pop, *args, **kwargs )

	def make_graphs(self):
		"""
		"""
		pass

	def go(self):
		"""
		Sets the simulation running.
		
		"""

		self.fairness = []
		for i in range(self.generations):
			##Record some metrics
			self.fairness.append( self.population.fairness)
			##Get the next generation
			self.population = self.population.new_generation( fitness_matrix = self.fitness_matrix, delta = self.delta )
			
		##Set some final metrics, which are useful for classes and functions that sweep this model
		self.final_fairness = self.population.fairness


		