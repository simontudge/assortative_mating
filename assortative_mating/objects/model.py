"""
File containing the class for the model. The model class is a thin-ish
wrapper for a Population, but knows how to repeatedly call its methods in
order to simulate many generations. It knows what to record, and provides
some methods for creating graphs etc.

This is also where the parameters of the model live.
"""

import numpy as np
import matplotlib.pyplot as plt

from assortative_mating import Population
import assortative_mating.helpers.game_theory_helpers as GT

class Model():
	"""
	The full model. Contains a population and methods for running simulation, as
	well as parameters as methods for plotting and analysis.
	"""

	def __init__(self, pop, h, s, delta, generations = 128, graphs = True, check_inputs = True,
		mu_strat = 0.05, mu_assort = 0.1):
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
			dominance. Often constrained to be between 0 and 1, although not a strict requiresment.
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
		graphs : bool {True}
			Whether or not to create the standard array of graphs
		check_inputs : bool {True}
			Checks inputs such as delta h and s to see if they are within sensible ranges.
			This can be overridden by setting this to False, do this if you are sure the inputs are
			right, or you are checking non-sensible inputs for means of control.
		mu_strat : float [0,1] {0.05}:
			Probability that a strategy is mutated when it is passed on.
		mu_assort : float [0,1] {0,1}:
			Probability that the assortment is mutated as it is passed on.
		Raises
		======
		ValueError :
			If delta < 0 or delta > 1. If s < 0 or > 1 or if h*s > 1.
		
		"""

		##Raise value error if any of the conditions are violated
		if check_inputs:
			if delta < 0 or delta > 1:
				raise ValueError ("Delta must be in [0,1], got {}".format(delta))
			if s < 0 or s > 1:
				raise ValueError ("s must be in [0,1], got {}".format(s))
			if h*s > 1:
				raise ValueError("h*s must be less than 1, got {}".format(h*s))
		##Set all input parameters
		self.Population = pop
		self.h = h
		self.s = s
		self.delta = delta
		self.generations = generations
		self.graphs = graphs
		self.mu_assort = mu_assort
		self.mu_strat = mu_strat
		##Check input values
		omega_00 = 1 - s
		omega_01 = 1 - h*s
		omega_10 = omega_01
		omega_11 = 1
		self.fitness_matrix = np.array( [ [ omega_00, omega_01 ],[ omega_10, omega_11 ] ] )
		##Other usuful parametes
		self.size = pop.total_individuals
		##Save the intial state of the Population
		self.pop0 = self.Population

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
		pop = Population.from_random(size)
		return Model( pop, *args, **kwargs )

	@classmethod
	def from_function(cls, fn, size, *args, **kwargs):
		"""
		Accepts any function that returns an individual and calls it repeatedly to make
		a population.
		Inputs
		======
		fn : callable
			A function that accepts no arguments and returns an individual.
		size : int
			An even integer that determines the size of the population.
		*args, ** kwargs :
			Passed to the model constructor. Must contain h, s and delta at a minimum.

		"""
		##Make a list of individuals
		inds = [ fn() for _ in range(size) ]
		##Make a population of the necessary size
		pop = Population( inds )
		##Make the model from the population
		return cls( pop, *args, **kwargs )

	def make_graphs(self, ax = None, ESS = False):
		"""
		Returns a matplotlib figure. Plots to ax if provided, otherwise creates a figure from
		scratch.
 
		Plots both fairness and average assortment on the same figure.

		If ESS is set to True then there will also be a dashed line for the predicted ESS of
		the well mixed game.

		"""

		if ax is None:
			_,ax = plt.subplots( figsize = (16,9) )
		ax.plot( self.fairness, label = 'Fairness' )
		ax.plot( self.desired_assortment, label = 'Desired Assortment' )
		ax.plot( self.inbreeding, label = 'inbreeding' )
		ax.plot( self.fitness, label = 'Fitness' )
		ax.set_xlabel( "Generations" )
		ax.legend()
		if ESS:
			ess_value = GT.ESS_h_s_delta( self.h, self.s, self.delta )
			x_bound = ax.get_xbound() 
			ax.plot( x_bound, [ ess_value ]*2, '--')

		return ax.figure

	def go(self):
		"""
		Sets the simulation running.
		
		"""

		self.fairness = []
		self.desired_assortment = []
		self.inbreeding = []
		self.fitness = []
		for i in range(self.generations):
			##Record some metrics
			self.fairness.append( self.Population.fairness)
			self.desired_assortment.append( self.Population.average_assortment )
			self.inbreeding.append( self.Population.inbreeding )
			self.fitness.append( self.Population.average_fitness( self.fitness_matrix ) )
			##Get the next generation
			self.Population = self.Population.new_generation( fitness_matrix = self.fitness_matrix,\
			 delta = self.delta, mu_strat = self.mu_strat, mu_assort = self.mu_assort )
			

		##Set some final metrics, which are useful for classes and functions that sweep this model
		self.final_fairness = self.Population.fairness
		self.final_desired_assortment = self.desired_assortment[0]

		if self.graphs:
			self.make_graphs()


		