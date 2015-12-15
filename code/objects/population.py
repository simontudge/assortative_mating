"""
File containing the class for a population of individuals.
A population of individuals is simply a list of individuals with some methods
for splitting and pairing the population, and seleticing the next generation.

"""

from code import individual

class population(object):
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

	@classmethod
	def from_random(cls, size):
		"""
		Initialise a population with a given size with random individuals.

		"""
		individuals = [ individual.from_random() for _ in range(size) ]
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
		"""
		pass

	def new_generation(self):
		"""
		"""
		pass