"""
File containg the object to represent an individual. Individuals are defined by the genes
that they have, and contain methods for choosing a mate, determining their own fitness and
creating an offspring.

"""

from numpy import random

class individual():
	"""
	"""

	def __init__(self, a1, a2, m1, m2):
		"""
		Initialiser for class individual.
		An individual is defined by four alleles. One of which determines the
		desired assortative matting (a). This lies in the interval [0,1]. 1 
		being an individual who always tries to mate assortativly in in the maximum
		sence, and zero being an individual who mates at random.
		The other gene is the value of the meotic disstorter and can be either 0, always
		distorts aka a defctor, or 1, doesn't distort aka a cooperator.
		Each gene has two copies as the individuals are diploid.
		
		Inputs
		======
		a_1 : float [0,1]
			Paternally derived value of the gene a
		a_2 : float [0,1]
			Maternally derived value of the gene a
		m_1 : int {0,1}
			Paternally derived value of the gene m
		m_2 : int {0,1}
			Maternally derived value of the gene m
		
		"""
		if not ( a1 >= 0 and a1 <= 1 ):
			raise ValueError ("a1 must be between 0 and 1, got {}".format(a1))
		if not ( a2 >= 0 and a2 <= 1 ):
			raise ValueError ("a2 must be between 0 and 1, got {}".format(a2))
		if not ( m1 in {0,1} ):
			raise ValueError ("m1 must be either 0 or 1, got {}".format(m1))
		if not ( m2 in {0,1} ):
			raise ValueError ("m2 must be either 0 or 1, got {}".format(m2))

		self.a1 = a1
		self.a2 = a2
		self.m1 = m1
		self.m2 = m2

	def __repr__(self):
		"""
		Standard method for representing the individual when printed to screen.

		"""
		return """\t{:.2}---{:.2}\n\t{:.2}---{:.2}
		""".format(self.a1, self.a2, float( self.m1 ), float( self.m2 ) )

	@classmethod
	def from_random(cls):
		"""
		Alternative constructor, to generate an individual from random.
		Selects a1 and a2 from the uniform random distribution, and
		m1 and m2 randomly as either 0 or 1.
		
		"""
		return cls( random.random(), random.random(), random.randint(2), random.randint(2) )

	def desired_assortment(self, q = 1/2):
		"""
		Returns the desired assortment of the individual, based on its values for the two
		genes a1 and a2. Also needs the value of q which determines the extent to which the
		larger of the two values of a is greater.

		"""


	def choose_mate(self, list_of_mates ):
		"""
		"""
		pass

	def make_offspring(self, mate):
		"""
		"""
		pass

	def fitness(self, fitnes_matrix):
		"""
		"""
		pass