install:
	conda env create -f environment.yml

setup:
	#source activate assortative_mating
	##Why isn't this working!?
	export PYTHONPATH="$HOME/evolution_of_assortative_mating/code:$PYTHONPATH"

test:
	py.test
