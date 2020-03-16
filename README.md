# MOF Big Adsorbate Initializer (MBAI)
A quick way to add (big) adsorbate molecules on specified binding sites on MOFs with a decent geometry (which can serve as initial structures for DFT optimizations or MD). This has been a pain for me (maybe you too) in several projects as CIF files are hard to edit with GUI. Name is blatantly plagiarized from Andrew's MAI.

![TOC](toc.png)

## Quick Start
Different from Andrew's approach in MAI (which is for adsorbates with <=3 atoms, AFAIK), the basic idea of MBAI is to use Monte Carlo (in RASPA) to guide the adsorbates to the binding sites you want, because systematic construction approach as in MAI might get untractable when the adsorbate is large. To make this work, super strong LJ parameters will be assigned to the pair of atoms you want to bind.  Basically what you need to do is to draw your adsorbate in Gaussview and save as a PDB, change the label of the binding site on the MOF to 'Z0' in the CIF file, let the program know which atom on the adsorbate will be binding, then you're good to go!   For a quick start, please take a look at the examples I provided.

## Troubleshooting
If the binding geometry doesn't look good, just re-run the simulation (maybe with more cycles, especially for bi-dentate binding). You can also try changing the temperature but I found that 100K is kind of optimal because 298K might be too high--within 100 cycles the adsorbate might not get there. I tried 1K too but it'll just freeze at the initial configuration.

## Prerequisites
Gaussview (will try to support other programs), RASPA, iRASPA, ase

## To-Do
Read other formats of the adsorbate structure file than Gaussview-PDB (as long as it has the connectivity info), flexible adsorbates (read OPLS/TraPPE from RASPA and assign bonds/angles/torsions), multiple adsorbates (need to let the adsorbates repel each other)

## Documentation
TBD
