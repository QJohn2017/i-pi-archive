"""Deals with creating the ensembles class.

Copyright (C) 2013, Robert Meissner and Riccardo Petraglia

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http.//www.gnu.org/licenses/>.


Classes:
   InputEnsemble: Deals with creating the Ensemble object from a file, and
      writing the checkpoints.
"""

import numpy as np
import ipi.engine.initializer
from ipi.engine.smotion import Smotion, ReplicaExchange, MetaDyn
from ipi.utils.inputvalue import *
from .remd import InputReplicaExchange
from .metad import InputMetaDyn
from ipi.utils.units import *

__all__ = ['InputSmotion']


class InputSmotion(Input):
    """Smotion calculation input class.

    A class to encompass the different "smootion" :) calculations.

    Attributes:
       mode: An obligatory string giving the kind of smootion calculation to be performed.

    Fields:

    """

    attribs = {"mode": (InputAttribute, {"dtype": str,
                                         "help": "Kind of smotion which should be performed.",
                                         "options": ['dummy', 'remd', 'metad']})}
    fields = {"remd": (InputReplicaExchange, {"default": {},
                                              "help": "Option for REMD simulation"}),
              "metad": (InputMetaDyn, {"default": {},
                                       "help": "Option for REMD simulation"})}

    dynamic = {}

    default_help = "Allow chosing the type of smotion to be performed. Holds all the information that is calculation specific, such as replica exchange parameters, etc."
    default_label = "SMOTION"

    def store(self, sc):
        """Takes a smootion calculation instance and stores a minimal representation of it.

        Args:
           sc: A smootion calculation class.
        """

        super(InputSmotion, self).store(sc)

        if type(sc) is Smotion:
            self.mode.store("dummy")
        elif type(sc) is ReplicaExchange:
            self.mode.store("remd")
            self.remd.store(sc)
        elif type(sc) is MetaDyn:
            self.mode.store("metad")
            self.metad.store(sc)
        else:
            raise ValueError("Cannot store Smotion calculator of type " + str(type(sc)))

    def fetch(self):
        """Creates a smootion calculator object.

        Returns:
           An ensemble object of the appropriate mode and with the appropriate
           objects given the attributes of the InputEnsemble object.
        """

        super(InputSmotion, self).fetch()

        if self.mode.fetch() == "remd":
            sc = ReplicaExchange(**self.remd.fetch())
        elif self.mode.fetch() == "metad":
            sc = MetaDyn(**self.metad.fetch())
        else:
            sc = Smotion()
            #raise ValueError("'" + self.mode.fetch() + "' is not a supported motion calculation mode.")

        return sc
