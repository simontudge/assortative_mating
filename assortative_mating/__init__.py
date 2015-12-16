##Set the matplotlib backend to be suitable for a server without a graphical interface
import matplotlib as mpl
mpl.use('Agg')


##Expose the most important classes to the global namespace
from .objects.individual import Individual
from .objects.population import Population
from .objects.model import Model
from .objects.pair import Pair