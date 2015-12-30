"""
File containg the object to represent an individual. Individuals are defined by the genes
that they have, and contain methods for choosing a mate, determining their own fitness and
creating an offspring.

"""

from numpy import random
from assortative_mating.helpers.utils import random_choice

class Individual(object):
	"""
	Class representing a single individual. An individual has four allele at two loci.
	It is thus a diploid individual. It is responsible for choosing a mate, and for 
	producing gametes. It also knows its own fitness.
	"""

	def __init__(self, a1, a2, m1, m2, *, q = 0.5, crossover = 0):
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
		q : float [0,1] {0.5}
			The extent to which the larger value of a is dominant.
			Actual desired assortment is determined by q*a_b + (1-q)*a_s
			where a_b is the bigger of the two values. So q = 1/2 means
			the effect is the mean of the two, where as q = 0 means the
			smaller one is completely dominant.
		crossover : float [0,1] {0}
			Proability that an individual crosses over its halplotype on
			mating. Crossover = 0 means that a1 and m1 will definitely be
			inherited together, whereas crossover = 1 means that an genes
			will be split and paired at random.

		"""
		if not ( a1 >= 0 and a1 <= 1 ):
			raise ValueError ("a1 must be between 0 and 1, got {}".format(a1))
		if not ( a2 >= 0 and a2 <= 1 ):
			raise ValueError ("a2 must be between 0 and 1, got {}".format(a2))
		if not ( m1 in {0,1} ):
			raise ValueError ("m1 must be either 0 or 1, got {}".format(m1))
		if not ( m2 in {0,1} ):
			raise ValueError ("m2 must be either 0 or 1, got {}".format(m2))

		##The four alleles
		self.a1 = float( a1 )
		self.a2 = float( a2 )
		self.m1 = m1
		self.m2 = m2

		##For convenience lets represent the two haplotypes as well
		self.haplo1 = (a1,m1)
		self.haplo2 = (a2,m2)

		##"Constant" parameters. These should be constant for the entire model,
		##But i'll put them as values of the object so that they can be made
		##To vary at a later stage.
		self.q = q
		self.crossover = crossover
	
	def __repr__(self):
		"""
		Standard method for representing the individual when printed to screen.

		"""
		return """\t{:.2}---{:.2}\n\t{}---{}
		""".format(self.a1, self.a2, float( self.m1 ), float( self.m2 ) )

	@classmethod
	def from_random(cls):
		"""
		Alternative constructor, to generate an individual from random.
		Selects a1 and a2 from the uniform random distribution, and
		m1 and m2 randomly as either 0 or 1.
		
		"""
		return cls( random.random(), random.random(), random.randint(2), random.randint(2) )

	@property
	def desired_assortment(self):
		"""
		Returns the desired assortment of the individual, based on its values for the two
		genes a1 and a2.

		"""

		bigger = max( self.a1, self.a2 )
		smaller = min( self.a1, self.a2 )
		return self.q*bigger + ( 1 - self.q )*smaller

	@property
	def phenotypic_value(self):
		"""
		The value of the phenotype, this is defined as the average value of the
		gene at locus a. Individuals can be only one of three types. 0, 1/2 or 1.
		
		"""

		return 0.5*( self.m1 + self.m2 )


	def choose_mate(self, mates ):
		"""
		Choose a mate at "Random" based on a list of potential mates.
		The choice depends in the individuals desired_assortment (A).
		With probability A they choose a mate of the same phenotype as
		themselves, and with probability 1 - A they choose a random mate.

		Returns
		=======
		A tuple, the first value being the integer index of the mate choosen
		and the second value being the mate itself.

		"""

		##A list of phenotypic values, together with the index of the individual
		all_mates = list( enumerate(mates) )

		if random.random() < self.desired_assortment:
			##Then we choose a mate who is clonally related
			potential_mates = [ p for p in all_mates if p[1].phenotypic_value == self.phenotypic_value ]
			##In the special case where there are no identical mates to choose from we'll just choose
			##at random.
			if len(potential_mates) == 0:
				potential_mates = all_mates
		else:
			##Choose a mate at random
			potential_mates = all_mates

		return random_choice( potential_mates )
		

	def make_gamete(self, delta, mu_strat = 0.05, mu_assort = 0.1):
		"""
		Returns a gamete, i.e. a gene a and a gene m.
		Which genes are chossen depends firstly on whether
		crossover takes place, and also on whether the individual
		contains any meiotic distorter alleles.
		Needs also mu_strat and mu_assort. See Individual.mutate_gamete.
		"""
		##Choose whether to crossover or not
		if random.random() < self.crossover:
			do_crossover = True
			##We can already select the value of gamete a if we know
			##Crossover will take place...
			gamete_a = random_choice( [self.a1, self.a2] )
		else:
			do_crossover = False

		##The probability of selecting m1 given gentic values of m1 and m2
		p_select_m1 = 0.5*( 1 + ( 1 - self.m1 )*delta - (1 - self.m2 )*delta )
		if random.random() < p_select_m1:
			gamete_m = self.m1
			if not do_crossover:
				gamete_a = self.a1
		else:
			gamete_m = self.m2
			if not do_crossover:
				gamete_a = self.a2

		gamete = gamete_a, gamete_m
		return self.mutate_gamete( gamete, mu_strat, mu_assort )

	def fitness(self, fitnes_matrix):
		"""
		Return the fitness of the individual based on a payoff matrix.
		This is determined soley by the m genes that the individual has.
		"""
		return fitnes_matrix[ self.m1, self.m2 ]

	@staticmethod
	def mutate_gamete(gamete, mu_strat = 0.05, mu_assort = 0.1):
		"""
		Takes a gamete and with specifed probabilities returns a mutated copy of the gamete.
		Inputs:
		=======
		gamete: (float, int):
			A gamete to be mutated. A gamete is represented by a tuple which contains the value
			of the two genes in the form (g_a, g_m).
		mu_strat : float {0.05}
			Probabilty with which the gamete will be mutated
		mu_assort: float {0.1}
			Probability with which the assortment will be mutated.
		Notes
		=====
		The gene for the strategy is a binary number. With probability mu_strat the allele which switch
		to the other version of the strategy.
		The gene for assortment is real number between zero and one. It is mutated with probability mu_assort.
		In which case a random ammount is added or subtracted to the value. This is drawn from the gaussian
		distribution with mean zero and standard deviation 0.05. Furthermore the returned value is scaled to
		lie within 0 and 1.
		"""
		old_a, old_m = gamete
		##Do the strategy
		if random.random() < mu_strat:
			new_m = ( old_m + 1 )%2
		else:
			new_m = old_m
		##Now do the assortment bit
		if random.random() < mu_assort:
			new_a = old_a + random.normal( 0, 0.05 )
			if new_a > 1:
				new_a = 1
			elif new_a < 0:
				new_a = 0
		else:
			new_a = old_a
		return ( new_a, new_m )
		

########Some helper methods for the individual, if there are many of these might consider having
#them in a seperate file, e.g. helpers.individual_helpers. For now just have them here.

def constant_assortment_individual( assortment, **kwargs):
	"""Returns an individual with specifed constant assortment.
	Assortment must be between 0 and 1, inclusive. Can specify both
	q and crossover via the **kwargs.
	"""
	return Individual( assortment, assortment, random.randint(2), random.randint(2), **kwargs )