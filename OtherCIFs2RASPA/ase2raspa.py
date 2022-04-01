#!/Users/Haoyuan/anaconda3/bin/python

"""
convert ase-generated cifs (mostly from VASP CONTCAR) to raspa-compatible ones
"""

import sys

fname = sys.argv[1]
f = open(fname,'r')
d = f.readlines()
f.close()

outname = fname.replace(".cif","_raspa.cif")
f = open(outname,'w')

for l in d:
    if "_atom_site_occupancy" in l:
        f.write("  _atom_site_type_symbol\n")
    elif "_atom_site_thermal_displace_type" in l:
        pass
    elif "_atom_site_B_iso_or_equiv" in l:
        pass
    elif "_atom_site_type_symbol" in l:
        pass
    elif "Biso   1.000" in l:
        ll = l.strip().split()
        f.write(ll[0]+"  "+ll[-1]+"  "+ll[2]+"  "+ll[3]+"  "+ll[4]+"\n")
    else:
        f.write(l)

f.close()
