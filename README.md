# MOF Big Adsorbate Initializer (MBAI)
A quick way to add (big) adsorbate molecules on specified binding sites on MOFs with a decent geometry (which can serve as initial structures for periodic DFT optimizations). This has been a pain for me (maybe for you too) in several projects as CIF files are hard to edit with GUI. Name is blatantly plagiarized from Andrew's [MAI](https://github.com/arosen93/mof-adsorbate-initializer).

![TOC](toc.png)

## Publications that used MBAI

First publication that used MBAI is published on JACS! [Drout et al. JACS, 2020](https://pubs.acs.org/doi/10.1021/jacs.0c04668). The example in examples/nu1000_glyphosate_bidentate is from this paper. 

## Quick Start
Different from Andrew's approach in MAI (which is for adsorbates with <=3 atoms, AFAIK), the basic idea of MBAI is to use Monte Carlo (through RASPA) to guide the adsorbates to the binding sites you want, because systematic construction approach as in MAI might get untractable when the adsorbate is large. To make this work, super strong Lennard-Jones parameters are assigned to the pair(s) of atoms you want to bind.  Basically what you need to do is to **draw your adsorbate** in Gaussview/Avogadro and save as a PDB, **change the label of the binding site(s) on the MOF** to 'Z0' (if bidentate, change the other site to 'Z1') in the CIF file, then **modify the script mbai.py and run it**! For a quick start, please take a look at the examples I provided.

## Troubleshooting
If the binding geometry doesn't look good, just re-run the simulation (maybe with more cycles, especially for bi-dentate binding). You can also try changing the temperature (in simgen.py) but I found that 100K (the default) is kind of optimal because at 298K it's too easy for non-binding configurations to be accepted. I tried 1K too but it'll just freeze at the initial configuration. You can also tune the epsilon of the special Lennard-Jones potential (in pdb2def.py), but the default value (10000K) seems to be pretty good from trial and error.

## Prerequisites
[Gaussview](https://gaussian.com/gaussview6/) or [Avogadro](https://avogadro.cc/), [RASPA](https://www.iraspa.org/RASPA/index.html), [ase](https://wiki.fysik.dtu.dk/ase/)

## To-Do
Flexible adsorbates (read OPLS/TraPPE from RASPA and assign bonds/angles/torsions), multiple adsorbates (need to let the adsorbates repel each other)

## Documentation
TBD
