install:
	conda env create -f environment.yml

setup:
	#source activate assortative_mating
	export PYTHONPATH="${PWD}:${PYTHONPATH}"

test:
	py.test --cov-report term-missing --cov-report html --cov=assortative_mating tests/
