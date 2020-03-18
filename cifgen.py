"""
about:
combine the framework CIF (original) and the adsorbate PDB (RASPA) to write combined CIFs
automatically write combined CIFs with the last frames so human visualization is not required

usage:
python cifgen.py MOF.cif n_last_frames_to_save

Haoyuan Chen, 03.17.2020
"""

import sys
import os
from ase.io import *
from ase import Atoms

mofcif = sys.argv[1]
ncifs = int(sys.argv[2])

cmd = 'cp Movies/System_0/Movie_*_allcomponents.pdb ./frames.pdb'
os.system(cmd)

f = open('frames.pdb','r')
d = f.readlines()
f.close()

nframes = 0
frame_start_idx = []
frame_end_idx = []

for i,l in enumerate(d):
    ll = l.strip().split()
    if 'MODEL' in ll[0]:
        nframes += 1
        frame_start_idx.append(i)
    elif 'ENDMDL' in ll[0]:
        frame_end_idx.append(i)

def readpdbpart(dd):
    cryst = []
    atoms = []
    symbols = ''
    for l in dd:
        ll = l.strip().split()
        if ll[0] == 'CRYST1':
            for i in range(6):
                cryst.append(float(ll[i+1]))
        elif ll[0] == 'ATOM':
            atoms.append([float(ll[4]),float(ll[5]),float(ll[6])])
            symbols += ll[2]
    return cryst,atoms,symbols

m = read(mofcif)

for i in range(ncifs):
    dd = d[frame_start_idx[-i-1]:frame_end_idx[-i-1]]
    cryst,atoms,symbols = readpdbpart(dd)
    a = Atoms(symbols, positions=atoms)
    a.set_pbc((True, True, True))
    a.set_cell(cryst)
    ma = m + a
    ma.write('combined_%d.cif'%(i))

