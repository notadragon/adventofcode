#!/usr/bin/env pypy

import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("(?:([a-zA-Z]+) => ([a-zA-Z]+))|([a-zA-Z]+)")

replacements = {}

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        if not m.group(1) in replacements:
            replacements[m.group(1)] = []
        replacements[m.group(1)].append(m.group(2))
    else:
        molecule = m.group(3)

print("Replacements: %s" % (replacements,))
print("Molecule: %s" % (molecule,))

reversereplacements = {}
for k,r in replacements.items():
    for repl in r:
        if not repl in reversereplacements:
            reversereplacements[repl] = []
        reversereplacements[repl].append(k)
    

def generateMolecules(r,m):
    maxkey = max( [ len(k) for k in r.keys() ] )
    for i in range(0,len(m)):
        for j in range(i+1,min(len(m),i+maxkey)+1):
            if m[i:j] in r:
                for repl in r[m[i:j]]:
                    yield m[0:i] + repl + m[j:]
if args.p1:
    print("Doing part 1")

    generated = set(generateMolecules(replacements,molecule))
    #for g in generated:
    #    print("Generated: %s" % (g,))
    print("Generated: %s" % (len(generated),))
    
if args.p2:
    print("Doing part 2")

    if False:
        molecules = set(["e"])
        allmolecules = set(["e"])
        steps = 0
        while not molecule in molecules:
            nextmolecules = set()
            for m in molecules:
                for g in generateMolecules(replacements,m):
                    if len(g) > len(molecule):
                        continue
                    if g in allmolecules:
                        continue
                    allmolecules.add(g)
                    nextmolecules.add(g)
            molecules = nextmolecules
            steps = steps + 1

            print("Step: %s Molecules: %s" % (steps,len(molecules,)))
        print("Steps: %s" % (steps,))
    elif False:
        molecules = set([molecule])
        allmolecules = set([molecule])
        steps = 0
        while molecules and not "e" in molecules:
            nextmolecules = set()
            for m in molecules:
                for g in generateMolecules(reversereplacements,m):
                    if g in allmolecules:
                        continue
                    allmolecules.add(g)
                    nextmolecules.add(g)
            minsize = min(len(m) for m in nextmolecules)
            molecules = [ m for m in nextmolecules if len(m) == minsize ]
            steps = steps + 1

            print("Step: %s All Molecules: %s minsize: %s Molecules: %s" % (steps,len(allmolecules),len(molecules,)))
        print("Steps: %s" % (steps,))
    else:
            
            
