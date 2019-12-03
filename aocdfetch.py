#!/usr/bin/env python3

import argparse, re, itertools, collections, os, sys
import aocd

rootdir = "."
configfile = "aocd.config"
while os.path.exists(rootdir) and not os.path.exists(os.path.join(rootdir,configfile)):
    rootdir = os.path.join(rootdir,"..")
rootdir = os.path.realpath(rootdir)

configfile = os.path.join(rootdir,configfile)
if not os.path.exists(configfile):
    print("Could not determine config file")
    sys.exit(-1)

configdata = { l[0:l.index("=")].strip() : l[l.index("=")+1:].strip() for l in open(configfile).readlines() }

relpath = os.path.relpath(os.getcwd(), rootdir)
m = re.match("^(\d\d\d\d)/(\d+)$", relpath)
if m:
    defyear = int(m.group(1))
    defday = int(m.group(2))
else:
    defyear = 0
    defday = 0
    
parser = argparse.ArgumentParser()
parser.add_argument("year",type=int,nargs="?",default=defyear)
parser.add_argument("day",type=int,nargs="?",default=defday)

args = parser.parse_args()

if args.year == 0:
    years = [ int(f) for f in os.listdir(rootdir) if re.match("^\d\d\d\d$",f) ]
    if years:
        year = max(years)
    else:
        year = 0
else:
    year = args.year
yeardir = os.path.join(rootdir,str(year))
if not os.path.exists(yeardir):
    print("Year directory does not exist: %s" % (yeardir,))
    sys.exit(-1)
    
if args.day == 0:
    days = [ int(f) for f in os.listdir(yeardir) if re.match("^\d+$",f) ]
    if days:
        day = max(days)
    else:
        day = 0
else:
    day = args.day
daydir = os.path.join(yeardir,str(day))
if not os.path.exists(daydir):
    print("Day directory does not exist: %s" % (daydir,))
    sys.exit(-1)

if "session" not in configdata:
    print("Missing session in configdata")
    sys.exit(-1)
    
print("Fetching %s:%s" % (year, day,))

inputfile = os.path.join(daydir,"input")
if os.path.exists(inputfile):
    print("Input file already exists: %s" % (inputfile,))
    sys.exit(-1)
    
data = aocd.get_data(session=configdata["session"], day = day, year = year)
if data[-1] != "\n":
    data = data + "\n"

open(inputfile,"w").write(data)
