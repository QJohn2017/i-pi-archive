#!/usr/bin/python
""" getproperty.py

Parses a property output file and - if present - outputs the column(s)
corresponding to the desired property. Relies on the infrastructure of i-pi, 
so the ipi package should be installed in the Python module directory, or 
the i-pi main directory must be added to the PYTHONPATH environment variable.

Syntax:
   geproperty.py propertyfile propertyname [skip] 
"""

import sys, re
import numpy as np
from ipi.utils.messages import verbosity, banner, warning
from ipi.engine.simulation import Simulation
from ipi.engine.outputs import *
from ipi.engine.properties import getkey
from ipi.inputs.simulation import InputSimulation
from ipi.utils.io import io_xml
from ipi.utils.units import unit_to_internal
from ipi.utils.mathtools import logsumlog


def main(inputfile, propertyname="potential", skip="0"):
   skip = int(skip)
   
   # opens & parses the input file   
   ifile = open(inputfile,"r")
   
   reprop = re.compile(' ([0-9]*) *--> '+propertyname)
   reunit = re.compile('{(.*)}')
   
 
   # now reads the file one frame at a time, and outputs only the required column(s)
   icol=-1
   step=0
   while True:
      try:
         line= ifile.readline()         
         if len(line)==0: raise EOFError
         while line[0] == "#":  # fast forward if line is a comment 
            rm=reprop.search(line)
            if not (rm is None):
               if icol>=0: 
                  warning("Multiple instances of the specified property "+propertyname+" have been found")
                  raise EOFError
               icol=int(rm.group(1))-1
            line= ifile.readline()         
            if len(line)==0: raise EOFError         
         if (icol<0): 
            warning("Could not find "+propertyname+" in file "+inputfile)
            raise EOFError            
         line=line.split()
         if (step>=skip): print line[icol]         
         step+=1
      except EOFError:
         break

if __name__ == '__main__':
   main(*sys.argv[1:])
