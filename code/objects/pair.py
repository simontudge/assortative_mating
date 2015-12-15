"""
This is the file for the pairs class. A pair is an object that represents two individuals.
It knows the fitness of the pair, as well as how to create an offspring from that pair.
"""

from code import individual

class pair(object):
	"""
	Object representing a pair. This is simply a 2-tuple of individuals,
	together with methods for determining the fitness of the individuals,
	and for creating an offspring.

	"""

	def __init__(self, I1, I2):
		"""
		Create a pair object from two individuals, I1 and I2.
		"""
		if ( not isinstance( I1, individual) ) or ( not isinstance(I2, individual) ):
			raise TypeError("Both inputs must be of type individual")
		self.I1 = I1
		self.I2 = I2
		self.pair = (I1,I2)

	@classmethod
	def from_random(cls):
		"""
		Creates a pair from two random individuals.
		Not usually called directly, exists mostly for 
		testing perposes.

		"""
		return cls( individual.from_random(), individual.from_random() )

	def __repr__(self):
		return "Pair of individuals:\n"+ self.I1.__repr__() + "\n" + self.I2.__repr__()

	def fitness(self, fitness_matrix):
		"""
		Returns the fitness of the pair, which is simply the mean fitness of the 
		two individuals.
		"""
		return 0.5*( self.I1.fitness(fitness_matrix) + self.I2.fitness(fitness_matrix) )

	def make_child(self, delta):
		"""
		Returns an individual which is the child of the two individuals in this pair.
		Calls make gamete on each individual and combines to make another individual.

		"""
		a1, m1 = self.I1.make_gamete(delta = delta)
		a2, m2 = self.I2.make_gamete(delta = delta)
		return individual(a1,a2, m1, m2)