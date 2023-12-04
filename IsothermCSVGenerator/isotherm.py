#!/usr/bin/python

'''
Compile an adsorption isotherm CSV file from a single RASPA GCMC simulation at multiple pressures

Usage: ./isotherm.py unit
'''

import os,sys

uni = sys.argv[1]

if uni == 'mg_per_g':
    cmd = "grep 'Average loading absolute \[milligram\/gram framework\]' Output/System_0/* > uptake_raw"
elif uni == 'mmol_per_g':
    cmd = "grep 'Average loading absolute \[mol\/kg framework\]' Output/System_0/* > uptake_raw"
elif uni == 'ml_per_g':
    cmd = "grep 'Average loading absolute \[cm^3 (STP)\/gr framework\]' Output/System_0/* > uptake_raw"
elif uni == 'ml_per_ml':
    cmd = "grep 'Average loading absolute \[cm^3 (STP)\/cm^3 framework\]' Output/System_0/* > uptake_raw"
os.system(cmd)

f = open("uptake_raw", 'r')
d = f.readlines()
f.close()

cmd = "rm uptake_raw"
os.system(cmd)

ps = []  # pressure
us = []  # loading
es = []  # stdev

for l in d:
    ll = l.strip().split()
    p = float(ll[0].split("_")[-1].replace(".data:",""))
    u = float(ll[-4])
    e = float(ll[-2])
    ps.append(p)
    us.append(u)
    es.append(e)

ps = sorted(ps)
us = sorted(us)
es = sorted(es)

f = open("isotherm.csv", 'w')
if uni == 'mg_per_g':
    f.write("Pressure(Pa),Uptake(mg/g),StandardDeviation(mg/g)\n")
elif uni == 'mmol_per_g':
    f.write("Pressure(Pa),Uptake(mmol/g),StandardDeviation(mmol/g)\n")
elif uni == 'ml_per_g':
    f.write("Pressure(Pa),Uptake(ml/g),StandardDeviation(ml/g)\n")
elif uni == 'ml_per_ml':
    f.write("Pressure(Pa),Uptake(ml/ml),StandardDeviation(ml/ml)\n")
for i in range(len(ps)):
    f.write("%f,%f,%f\n"%(ps[i],us[i],es[i]))
f.close()


