#!/usr/bin/python

'''
Compile an adsorption isotherm CSV file from a single RASPA GCMC simulation at multiple pressures

Usage: ./isotherm.py unit
'''

import os,sys

u = sys.argv[1]

if u == 'mg_per_g':
    cmd = "grep 'Average loading absolute \[milligram\/gram framework\]' Output/System_0/* > uptake_raw"
elif u == 'mmol_per_g':
    cmd = "grep 'Average loading absolute \[mol\/kg framework\]' Output/System_0/* > uptake_raw"
elif u == 'ml_per_g':
    cmd = "grep 'Average loading absolute \[cm^3 (STP)\/gr framework\]' Output/System_0/* > uptake_raw"
elif u == 'ml_per_ml':
    cmd = "grep 'Average loading absolute \[cm^3 (STP)\/cm^3 framework\]' Output/System_0/* > uptake_raw"
os.system(cmd)

f = open("uptake_raw", 'r')
d = f.readlines()
f.close()

cmd = "rm uptake_raw"
os.system(cmd)

ps = []
us = []

for l in d:
    ll = l.strip().split()
    p = float(ll[0].split("_")[-1].replace(".data:",""))
    u = float(ll[-4])
    ps.append(p)
    us.append(u)

ps = sorted(ps)
us = sorted(us)

f = open("isotherm.csv", 'w')
if u == 'mg_per_g':
    f.write("Pressure(Pa),Uptake(mg/g)\n")
elif u == 'mmol_per_g':
    f.write("Pressure(Pa),Uptake(mmol/g)\n")
elif u == 'ml_per_g':
    f.write("Pressure(Pa),Uptake(ml/g)\n")
elif u == 'ml_per_ml':
    f.write("Pressure(Pa),Uptake(ml/ml)\n")
for i in range(len(ps)):
    f.write("%f,%f\n"%(ps[i],us[i]))
f.close()


