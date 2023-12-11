#!/usr/bin/env python3

import argparse, re, itertools, collections, math

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

lineRe = re.compile("^(?:([LR]+)|(?:([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)))$")

instrs = None
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
        
    # Process input line
    if m.group(1):
        instrs = m.group(1)
    else:
        data.append( ( m.group(2), m.group(3), m.group(4), ) )

print(f"Instrs: {instrs}")
for d in data:
    print(f"  {d}")
nodes = { x : (y,z) for x,y,z in data }
print(f"Nodes: {len(nodes)}")

def instrrange(instrs):
    while True:
        for i in instrs:
            yield i


def nextpos(pos, instr):
    if instr == "L":
        return nodes[pos][0]
    else:
        return nodes[pos][1]
            
if args.p1:
    print("Doing part 1")

    pos = "AAA"
    dest = "ZZZ"
    
    

    count = 0
    steps = iter(instrrange(instrs))
    while pos != dest:
        step = next(steps)

        pos = nextpos(pos, step)

        count = count + 1
        
    print(f"Count: {count}")
    
if args.p2:
    print("Doing part 2")

    #TODO: if instrs repeats, cut it down.
    
    nodes = { x : (y,z) for x,y,z in data }

    nodenames = set( k for k in nodes.keys() )

    startposes = set( i for i in nodenames if i[-1] == "A" )
    dests = set( i for i in nodenames if i[-1] == "Z" )

    #print(f"Path?: {startposes} -> {dests}")

    count = 0

    def solutions(initpos):
        solved = {}

        count = 0
        pos = initpos
        loop = None
        
        while True:
            ipos = count % len(instrs)
            step = instrs[ipos]

            npos = nextpos(pos, step)
            count = count + 1

            if npos[-1] == "Z":
                solid = (ipos, npos)

                if solid in solved:
                    # loop found
                    loop = ( solved[solid], count )
                    
                    break
                solved[solid] = count

            pos = npos

        print(f"Initpos: {initpos} solutions: {solved} LoopStart: {loop} (size = {loop[1]-loop[0]})")

        preloops = []
        postloops = []
        loopsize = loop[1] - loop[0]

        for solid, count in solved.items():
            if count < loop[0]:
                preloops.append(count)
            else:
                postloops.append(count - loop[0])

        postloops.sort()
                
        print(f"  Preloops: {preloops}  Loopsize: {loopsize} Loops: {postloops}")

        
        
        return ( tuple(preloops), loop, tuple(postloops) )

    solutiondata = {
        pos : solutions(pos) for pos in startposes
    }

    solvepoint = None
    solverepeat = None
    solvemin = 0


    if False:
      def iterdata( sd1 ):
          preloops1, loop1, postloops1 = sd1
  
          for x in preloops1:
              yield x
  
          loopsize = loop1[1] - loop1[0]
          base = loop1[0]
  
          while True:
              for x in postloops1:
                  yield base + x
              base = base + loopsize
                  
  
  
      solutions = []
      for key,sd in solutiondata.items():
          i = iterdata(sd)
          sditer = ( next(i), key, i )
          solutions.append(sditer)
          solutions.sort()
  
      mindiff = solutions[-1][0] - solutions[0][0]
      while solutions[0][0] != solutions[-1][0]:
          diff = solutions[-1][0] - solutions[0][0]
          if diff < mindiff:
              print(f"Diff: {diff}")
              mindiff = diff
              
          maxval = solutions[-1][0]
          newsolutions = []
          
          for n, key, sdi in solutions:
              #print(f"{key} -> {n}")
              
              while n < maxval:
                  n = next(sdi)
  
              if n > maxval:
                  maxval = n
                  
              newsolutions.append( (n,key,sdi) )
  
          newsolutions.sort()
          solutions = newsolutions
  
              
  
      print(f"Solution: {solutions[0][0]}")

    else:
        def nextval(sd, minval):
            preloops, loops, postloops = sd

            if minval < loops[0]:
                for v in preloops:
                    if v >= minval:
                        return v
                minval = loops[0]

            loopsize = loops[1] - loops[0]
                
            base = ((minval - loops[0]) // loopsize) * loopsize + loops[0]
            while True:
                for v in postloops:
                    r = base + v
                    if r >= minval:
                        return r
                base = base + loopsize

        minsolve = 0
        maxcount = 0
        while True:
            count = 0
            for key,sd in solutiondata.items():
                n = nextval(sd, minsolve)
                if n > minsolve:
                    nextmin = n
                    break
                count = count + 1
            if count > maxcount:
                maxcount = count
                print(f"Val: {minsolve} count: {count}")
                if count == len(solutiondata):
                    break
            minsolve = nextmin
            

        
