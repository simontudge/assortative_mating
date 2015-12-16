"""
Script for a collection of helper functions for dealing with the game theoretic asspects of the model.
These are things such as converting between certain parameter sets and finding equilibriums etc.

"""

def get_ST(h,s,delta):
	"""
	Returns the equivalent S T parameterisation of the game from h, s and
	delta. Returns as a tuple (S,T).
	"""
	S = ( ( 1 - delta )*( 1 - h*s ) - ( 1 - s ) )/s
	T = ( ( 1 + delta )*( 1 - h*s )-( 1 - s ) )/s
	return S,T

##Convert from S and T to h,s and delta
##Not clear how to do this, will have to fix one of these parameters.

##ESS in terms of S and T
def ESS(S,T):
	r"""
	Returns the ESS in terms of x, frequency of cooperate, give S and T.
	For bistable game, (i.e. the stag-hunt) game returns the frequency reach
	if the population starts at 50% cooperate.
	"""
	 ##PD
	if S <= 0 and T >= 1:
	 	return 0
	 #stag-hunt
	elif S <= 0 and T <= 1:
	 	##Defect Favoured
	 	if T - S >= 1:
	 		return 0
	 	##Coop favoured
	 	else:
	 		return 1
	 ##Harmony
	elif S >= 0 and T <= 1:
		return 1
	 ##Snowdrift
	elif S >= 0 and T >= 1:
		return S/( S + T - 1 )
	else:
		raise ValueError ("No-ESS found, something has gone wrong!")

def hd_from_STs(S,T,s):
	"""
	Returns h and delta in a tuple, give a value of S, T and s.
	
	"""

	h = .5*( 2 - S - T )
	delta = ( s*( T - S ))/( 2 + s*( S + T - 2 ) )

	return h,delta

##ESS in terms of h, s and delta.
def ESS_h_s_delta(h,s,delta):
	"""
	Returns the ESS in terms of h s and delta.

	"""
	S,T = get_ST(h,s,delta)
	return ESS(S,T)