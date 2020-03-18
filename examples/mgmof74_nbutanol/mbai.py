"""
about:
main script (wrapper) of MBAI

usage:
python mbai.py

Haoyuan Chen, 03.17.2020
"""

import os

# set up the calculation here
raspa_dir = '/home/hcu7189/RASPA-2.0'  # do 'echo $RASPA_DIR' to see
adsorbate = 'nbutanol.pdb'  # xx.pdb, saved from Gaussview or Avogadro
mof = 'MgMOF-74.cif'  # xx.cif, the binding site(s) should be labeled as 'Z0' (and 'Z1' if bidentate)
nsites = 1  # 1 if monodentate, 2 if bidentate
site1 = 14  # index of binding atom 1 which will bind to Z0, 1-start
dist1 = 2.00  # length of 1st bond in A
ncifs = 5  # save the last x frames from MC
# if nsites==2
#site2 = 2  # index of binding atom 2 which will bind to Z1, 1-start
#dist2 = 2.00  # length of 2nd bond in A

# generates the script that does everything
f = open('mbai.sh','w')
if nsites == 1:
    f.write('python pdb2def.py %s %d %.2f\n'%(adsorbate,site1,dist1))
elif nsites == 2:
    f.write('python pdb2def.py %s %d %.2f %d %.2f\n'%(adsorbate,site1,dist1,site2,dist2))
f.write('python simgen.py %s %s\n'%(mof,adsorbate))
f.write('%s/bin/simulate simulation.input\n'%(raspa_dir))
f.write('python cifgen.py %s %d\n'%(mof,ncifs)) 
f.close()

# this will run MBAI
os.system('mbai.sh')

