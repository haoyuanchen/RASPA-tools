"""
about:
generate a simulation.input file given the (modified with Z0/Z1) CIF file

usage:
python simgen.py MOF.cif ads.pdb 

Haoyuan Chen, 03.17.2020
"""

import sys
from ase.io import *
import numpy as np

cifname = sys.argv[1]
adsname = sys.argv[2]

# can change these values
cutoff = 12.0
ncycles = 1000
ninit = 0
nprint = 100
nmovie = 10
temp = 100.0
nads = 1

def unitcells(cifname,cutoff):
    c = read(cifname)
    cells = [1,1,1]
    if c.cell.orthorhombic:
        for i in range(3):
            cells[i] = np.ceil(2*cutoff/c.cell[i][i])
    else:
    # below is placeholder
    # will implement the MIC for triclinic later
    # https://pdfs.semanticscholar.org/a5bd/f949911c0d7333ffec488b0589e88cd722b6.pdf
        for i in range(3):
            cells[i] = np.ceil(2*cutoff/c.cell[i][i])
    return cells

cells = unitcells(cifname,cutoff)

f = open('simulation.input','w')
f.write('SimulationType  MonteCarlo\nNumberOfCycles  %d\nNumberOfInitializationCycles  %d\nPrintEvery  %d\n'%(ncycles,ninit,nprint))
f.write('Forcefield  GenericMOFs\nCutOffVDW  %.1f\n'%(cutoff))
f.write('Framework  0\nFrameworkName  %s\nUnitCells  %d %d %d\n'%(cifname.replace('.cif',''),cells[0],cells[1],cells[2]))
f.write('Movies  yes\nWriteMoviesEvery  %d\nExternalTemperature  %.1f\n'%(nmovie,temp))
f.write('Component 0 MoleculeName  %s\n            MoleculeDefinition  local\n            StartingBead  0\n            TranslationProbability  1.0\n            RotationProbability  1.0\n            ReinsertionProbability  1.0\n            CreateNumberOfMolecules  %d\n'%(adsname.replace('.pdb',''),nads))
f.close()



