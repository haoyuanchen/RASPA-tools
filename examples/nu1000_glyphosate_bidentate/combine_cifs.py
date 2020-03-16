"""
about:
combine the framework CIF (original) and the adsorbate CIF (iRASPA) to write a combined CIF

usage:
python combine_cifs.py MOF.cif frame-xx.cif

Haoyuan Chen, 03.15.2020
"""

import sys
from ase.io import *

mofcif = sys.argv[1]
adscif = sys.argv[2]

a = read(mofcif)
b = read(adscif)

c = a + b
c.write('combined.cif')
