"""
about:
convert Gaussview/Avogadro-generated pdb file to RASPA def file
also generates pseudo_atoms.def and force_field.def

notes:
only define rigid bond for now, may add flexible bond and angles/dihedrals later
rigid bonds should be fine as Gaussview-generated geometry is reasonable
can do monodentate and bidentate

usage:
python pdb2def.py xx.pdb idx_of_binding_atom_1(1-start, as in gaussview) length_of_binding_bond1(in A) [idx_of_binding_atom_2 length_of_binding_bond2]

Haoyuan Chen, 03.15.2020
"""

import sys

bidentate = 0
if len(sys.argv) > 4:  # bidentate
    bidentate = 1

fname = sys.argv[1]

f = open(fname,'r')
d = f.readlines()
f.close()

atoms = []
bonds = []

def conect2bond(ll):
    lll = list(map(int,ll[1:]))
    bonds = []
    for x in lll[1:]:
        if x > lll[0]:  # to avoid duplicates
            bonds.append(sorted([x-1,lll[0]-1]))  # gaussview is 1-start but raspa is 0-start
    return bonds

for i,l in enumerate(d):
    ll = l.strip().split()
    if ll[0] == 'HETATM' or ll[0] == 'ATOM':
        if len(ll) == 8:  # Gaussview
            atoms.append([ll[2],float(ll[4]),float(ll[5]),float(ll[6])])
        elif len(ll) == 11:  # Avogadro
            atoms.append([ll[2],float(ll[5]),float(ll[6]),float(ll[7])])
    elif ll[0] == 'CONECT':
        bs = conect2bond(ll)
        if len(bs):
            for b in bs:
                bonds.append(b)

bindidx = int(sys.argv[2])
atoms[bindidx-1][0] += '_Z0'
if bidentate:
    bindidx2 = int(sys.argv[4])
    atoms[bindidx2-1][0] += '_Z1'

natoms = len(atoms)
nbonds = len(bonds)

molname = fname.replace('.pdb','')

fname_1 = molname + '.def'

f1 = open(fname_1,'w')
f1.write('# critical constants: Temperature [T], Pressure [Pa], and Acentric factor [-]\n0.0\n0.0\n0.0\n# Number Of Atoms\n%d\n# Number Of Groups\n1\n# %s-group\nrigid\n# number of atoms\n%d\n# atomic positions\n'%(natoms,molname,natoms))
for i,a in enumerate(atoms):
    f1.write('%d %s %.3f %.3f %.3f\n'%(i,a[0],a[1],a[2],a[3]))
f1.write('# Chiral centers Bond  BondDipoles Bend  UrayBradley InvBend  Torsion Imp. Torsion Bond/Bond Stretch/Bend Bend/Bend Stretch/Torsion Bend/Torsion IntraVDW IntraCoulomb\n')
f1.write('0 %d 0 0 0 0 0 0 0 0 0 0 0 0 0\n'%(nbonds))  # hard-code all others with 0 for now
f1.write('#Bond stretch:atom n1-n2,type parameter\n')
for b in bonds:
    f1.write('%d %d RIGID_BOND\n'%(b[0],b[1]))
f1.write('# Number of config moves\n0\n')
f1.close()

elems = []
for a in atoms:
    elems.append(a[0])
elems = list(dict.fromkeys(elems))  # remove duplicates
nelems = len(elems)

f2 = open('pseudo_atoms.def','w')
f2.write('#number of pseudo atoms\n%d\n'%(nelems))
f2.write('#type      print   as    chem  oxidation   mass        charge   polarization B-factor radii  connectivity anisotropic anisotropic-type   tinker-type\n')
for e in elems:
    e_chem = e.split('_Z')[0]
    f2.write('%s yes %s %s 0 1.0 0.0 0.0 1.0 1.0 0 0 relative 0\n'%(e,e_chem,e_chem))
f2.close()

bindatom = atoms[bindidx-1][0]
binddist = float(sys.argv[3])/1.122  # convert minima to sigma
if bidentate:
    bindatom2 = atoms[bindidx2-1][0]
    binddist2 = float(sys.argv[5])/1.122

force_const = 10000.0  # can change

f3 = open('force_field.def','w')
f3.write('# rules to overwrite\n0\n# number of defined interactions\n%d\n# type      type2       interaction\n'%(bidentate+1))
f3.write('%s Z0 lennard-jones %.2f  %.2f\n'%(bindatom,force_const,binddist))
if bidentate:
    f3.write('%s Z1 lennard-jones %.2f  %.2f\n'%(bindatom2,force_const,binddist2))
f3.write('# mixing rules to overwrite\n0\n')
f3.close()


