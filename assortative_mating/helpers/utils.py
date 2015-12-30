"""
A collection of miscelenous utilities.
"""

from numpy import random
import numpy as np

##Note the numpy.random.choice basically does this,
##But that it is inconvinient in two way. Firstly the
##list chossen from must be 'flat'. i.e. no lists of
##list, and secondly the weight must sum to one.
def random_choice(input_iterable, p = None, size = None, replacement = True, with_index = False):
	"""
	Choose at random from the list, potentially weighted with the
	list of wiegths p. Set replacement = False to sample without
	replacement, default = True.

	If with_index is True the returned value is a tuple of the from
	(index, value)

	size, an integer specifing the number of times to sample the array, default None
	Note that None returns a single element of the list, whereas 1 returns a list with_index
	one element.
	
	"""

	input_list = np.array(input_iterable)

	##Normalise the vector p
	if p is not None:
		p_array = np.array(p)
		#Make the smallest number equal to zero by adding a constant if necessary
		if min(p_array) < 0:
			p_array -= min(p_array)
		##If the array is all zero, add one
		if sum(p_array) == 0:
			p_array += 1
		##Now normalise the array
		p_array = p_array/sum(p_array)
	else:
		p_array = None

	##Choose the index of the array which to pick, this is necessary as the numpy
	##function will complain if the list is not a flat list.
	index = random.choice( range( len(input_list) ), size = size, replace = replacement, p = p_array )
	if with_index:
		return index, input_list[index]
	else:
		return input_list[index]
