"""
File containing the class for a population of individuals.
A population of individuals is simply a list of individuals with some methods
for splitting and pairing the population, and seleticing the next generation.

"""

from assortative_mating import Individual
from assortative_mating.objects.pair import Pair
from assortative_mating.helpers.utils import random_choice

import numpy as np
import matplotlib.pyplot as plt
try:
	import seaborn
except ImportError:
	pass

class Population(object):
	"""
	Class representing a population. This is essentially a wrapper for a list of
	individuals, but contains methods for pairing the individuals, mating them
	and creating new populations.
	"""

	def __init__(self, individuals):
		"""
		Initialise the population class with a list of individuals.
		individuals must be a list of individuals with an even length.
		"""
		if len(individuals)%2 != 0:
			raise ValueError("List of individuals must be even in length")
		self.individuals = individuals
		self.total_individuals = len(individuals)
		##Set these to none, as they will be set later
		self.females = None
		self.males = None
		self.pairs = None 

	def __repr__(self):
		return "Population of {} individuals".format( self.total_individuals )

	def __len__(self):
		"""
		Returns the length of the population, defined as the total number of individuals.
		"""
		return self.total_individuals

	def __getitem__(self, i):
		return self.individuals[i]

	@classmethod
	def from_random(cls, size):
		"""
		Initialise a population with a given size with random individuals.

		"""
		individuals = [ Individual.from_random() for _ in range(size) ]
		return cls( individuals )

	def divide_population(self):
		"""
		Divides the population in two. Sets the results to two lists
		called females and males. This assumes that the population is
		already in a random order. 
		"""

		self.females = self.individuals[:int( self.total_individuals/2 )]
		self.males = self.individuals[int( self.total_individuals/2 ):] 

	def pair_population(self):
		"""
		Takes a female and let's her choose a mate, removes that female and
		male from the list. Repeats until everyone is paired.
		
		"""
		if self.females is None or self.males is None:
			self.divide_population()
		pairs = []
		for female in self.females:
			index, male = female.choose_mate( self.males )
			##Make a pair
			new_pair = Pair( female, male )
			pairs.append( new_pair )
			##Remove the male from the list of males
			self.males.pop(index)
		self.pairs = pairs

	def new_generation(self, fitness_matrix, delta, mu_strat = 0.05, mu_assort = 0.1 ):
		"""
		Creates and returns a new population which is the outcome of one generation of selection.
		"""
		if self.pairs is None:
			self.pair_population()
		fitnesses = [ p.fitness( fitness_matrix ) for p in self.pairs ]
		parents = random_choice( self.pairs, p = fitnesses, size = self.total_individuals )
		children = [ p.make_child(delta, mu_strat = mu_strat, mu_assort = mu_assort) for p in parents ]
		return Population( children )

	##########Metrics############

	@property
	def fairness(self):
		"""
		Returns the average value of the fair allele in the population.

		"""
		return np.mean( [ I.phenotypic_value for I in self.individuals ] )

	@property
	def average_assortment(self):
		"""
		Returns the mean desired assortment of the population.

		"""
		return np.mean( [ I.desired_assortment for I in self.individuals ] )

	@property
	def inbreeding(self):
		"""
		Returns the messured inbreeding, rather than the average desired assortment. This should
		be roughly similiar to the avarage dedired assortment, but is measured as the outcome of the
		actual pairing. It is the normalised covariance of the phenotypes of the individuals in each
		pair.

		"""

		if self.pairs is None:
			self.pair_population()

		x = [ p[0].phenotypic_value for p in self.pairs ]
		y = [ p[1].phenotypic_value for p in self.pairs ]
		return np.corrcoef( x, y )[0,1]

	def average_fitness( self, fitness_matrix ):
		"""
		Return the average fitness of the population, given a fitness matrix.

		"""
		return np.mean( [ I.fitness(fitness_matrix) for I in self.individuals ] )

	#######Plots##############

	def plot_scatter_pairs(self, ax = None, figsize = (16,9) ):
		"""
		Returns a matplotlib figure with a scatter plot of female phenotpye on the x-axis
		and male phenotype on the y-axis, together with a line of best fit and some additional
		annotations.
		Inputs
		======
		ax : matplotlib axes {None}
			Axes on which to make the plot, if none they will be created.
		figsize : 2-tuple { (16,9 ) }
			2-tuple denoting the figure size in inches
		Returns
		=======
		matplotib figure
		
		"""

		if ax is None:
			_, ax = plt.subplots(figsize=figsize)

		if ( self.females is None ) or (self.males is None):
			self.pair_population()

		x = [ p[0].phenotypic_value for p in self.pairs ]
		y = [ p[1].phenotypic_value for p in self.pairs ]
		
		ax.scatter(x,y)
		ax.set_xlabel("Female phenotype")
		ax.set_ylabel("Male phenotype")
		return ax.figure
