#!/usr/bin/env pypy

import argparse, re, itertools, collections

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

lineRe = re.compile("(-?\d+)(?:,(-?\d+))*.*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    instructions = [ int(c) for c in x.split(",") ]

#print("Instructions: %s" % (instructions,))

def params(pmode, paramtypes, pos, relbase, values):
    #print("pmode: %s paramtypes: %s pos: %s values: %s" % (pmode, paramtypes, pos, values,))
    output = []
    i = 0
    while i < len(paramtypes):
        p = values.get(pos + 1 + i,0)
        imode = pmode % 10
        itype = paramtypes[i]
        #print("i: %s pmode: %s itype: %s imode: %s p: %s" % (i,pmode,itype,imode,p,))
        if itype == 1:
            if imode == 0:
                p = values.get(p,0)
            elif imode == 1:
                p = p
            elif imode == 2:
                p = values.get(p + relbase,0)
        elif itype == 0:
            if imode == 0:
                p = p
            elif imode == 2:
                p = p + relbase
        output.append(p)
        i = i + 1
        pmode /= 10
    #print("output: %s" % (output,))
    return tuple(output)

def genoutput(values, input):
    pos = 0
    relbase = 0
    vals = { i:v for i,v in enumerate(values) }
    while True:
        #print("Vals: %s" % (vals,))
        instruction = vals.get(pos,0)
        opcode = instruction % 100
        pmode = instruction / 100
        #print("pos: %s opcode: %s pmode: %s" % (pos,opcode, pmode, ))
        if opcode == 99:
            #print("HALTING")
            return
        elif opcode == 1:
            i1,i2,i3 = params(pmode, (1,1,0), pos, relbase, vals)
            vals[i3] = i1 + i2
            pos = pos + 4
        elif opcode == 2:
            i1,i2,i3 = params(pmode, (1,1,0), pos, relbase, vals)
            vals[i3] = i1 * i2
            pos = pos + 4
        elif opcode == 3:
            (i1,) = params(pmode, (0,), pos, relbase, vals)
            ival = input.next()
            if ival == None:
                yield None
                continue
            vals[i1] = ival
            pos = pos + 2
        elif opcode == 4:
            (i1,) = params(pmode, (1,), pos, relbase, vals)
            yield i1
            pos = pos + 2
        elif opcode == 5:
            (i1,i2) = params(pmode, (1,1,), pos, relbase, vals)
            if i1 != 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 6:
            (i1,i2) = params(pmode, (1,1,), pos, relbase, vals)
            #print("i1,i2: %s" % ( (i1,i2,), ) )
            if i1 == 0:
                pos = i2
            else:
                pos = pos + 3
        elif opcode == 7:
            (i1,i2,i3) = params(pmode, (1,1,0), pos, relbase, vals)
            if i1 < i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        elif opcode == 8:
            (i1,i2,i3) = params(pmode, (1,1,0), pos, relbase, vals)
            if i1 == i2:
                vals[i3] = 1
            else:
                vals[i3] = 0
            pos = pos + 4
        elif opcode == 9:
            (i1,) = params(pmode, (1,), pos, relbase, vals)
            relbase = relbase + i1
            pos = pos + 2
        else:
            print("Unknown opcode: %s" % (opcode,))
            return

if True:
    g = genoutput(instructions, iter([]))

    lines = []
    l = []
    for o in g:
        if o == ord('\n'):
            if l:
                lines.append("".join(l))
            l = []
        else:
            l.append(chr(o))


grid = lines[:]
#for l in lines:
#    print(l)
            
if args.p1:
    print("Doing part 1")

    aparams =0
    for x in range(1,len(grid[0])-1):
        for y in range(1,len(grid)-1):
            if grid[y][x-1:x+2] == "###" and grid[y-1][x] == "#" and grid[y+1][x] == "#":
                aparams += x*y

    print("Total Params: %s" % (aparams,))
    
def genpath(grid):
    directions = {
        "^" : (0,-1),
        "v" : (0,1),
        "<" : (-1,0),
        ">" : (1,0),
    }
    turns = {
        ( "^", ">" ) : ( "R", ), 
        ( "^", "v" ) : ( "R", "R", ), 
        ( "^", "<" ) : ( "L", ), 
        ( ">", "v" ) : ( "R", ), 
        ( ">", "<" ) : ( "R", "R", ), 
        ( ">", "^" ) : ( "L", ), 
        ( "v", "<" ) : ( "R", ), 
        ( "v", "^" ) : ( "R", "R", ), 
        ( "v", ">" ) : ( "L", ), 
        ( "<", "^" ) : ( "R", ), 
        ( "<", ">" ) : ( "R", "R", ), 
        ( "<", "v" ) : ( "L", ),
    }

    # pad grid
    newgrid = []
    newgrid.append( "." * ( len(grid[0]) + 2 ) )
    newgrid.extend([ "." + c + "." for c in grid ])
    newgrid.append( "." * ( len(grid[0]) + 2 ) )
    grid = newgrid

    w = len(grid[0])
    h = len(grid)

    #print("w: %s h: %s" % (w,h,))

    unvisitted = set()
    for x,y in itertools.product(range(0,w),range(0,h)):
        #print("x: %s y: %s yw:%s" % (x,y,len(grid[y]),))
        if grid[y][x] in directions:
            loc = (x,y)
            dirlabel = grid[y][x]
            heading = directions[dirlabel]
        elif grid[y][x] == "#":
            unvisitted.add( (x,y) )

    print("Location: %s heading: %s unvisitted: %s" % (loc,heading,len(unvisitted),))

    output = []

    while unvisitted:
        nextloc = (loc[0] + heading[0], loc[1] + heading[1])
        if grid[nextloc[1]][nextloc[0]] == "#":
            if isinstance(output[-1],int):
                output[-1] = output[-1] + 1
            else:
                output.append(1)
            loc = nextloc
            if nextloc in unvisitted:
                unvisitted.remove(nextloc)
            continue

        newdir = None
        for v,h in directions.items():
            nextloc = (loc[0] + h[0], loc[1] + h[1])
            if nextloc not in unvisitted:
                continue
            if grid[nextloc[1]][nextloc[0]] == "#":
                newdir = v
                break
        if newdir:
            output.extend( turns[ (dirlabel, newdir) ] )
            
            dirlabel = newdir
            heading = directions[dirlabel]
            continue

        raise "Direct path does not work"
    
    return output

def findindices(full, prefix):
    for i in range(0,len(full)):
        if full[i:i+len(prefix)] == prefix:
            yield i

def zippath(path):
    MAIN=[]
    FUNCS=[ [], [], [], ]
    FUNCNAMES="ABC "

    for f in range(0,3):
        funcstart = None
        for i in range(0,len(path)):
            if str(path[i]) in FUNCNAMES:
                continue
            funcstart = path[i:i+4]
            break

        if not funcstart:
            break

        indices = tuple(findindices(path,funcstart))
        reduction = len(",".join([str(c) for c in funcstart])) * len(indices)

        #print("Start %s Indices: %s Reduction: %s" % (funcstart, indices, reduction))
        
        while (len(path) >= indices[0] + len(funcstart) + 2) and path[indices[0] + len(funcstart) + 1] != " ":
            testfuncstart = path[indices[0]:indices[0] + len(funcstart) + 2]
            testindices = tuple(findindices(path,testfuncstart))
            testreduction = len(",".join([str(c) for c in testfuncstart])) * len(testindices)
            #print("Start %s Indices: %s Reduction: %s" % (testfuncstart, testindices, testreduction))
            if not testindices:
                break
            if testreduction >= reduction:
                indices = testindices
                funcstart = testfuncstart
                reduction = testreduction
            else:
                break

        FUNCS[f] = ",".join([str(c) for c in funcstart])

        for c in indices:
            path[c] = FUNCNAMES[f]
            for i in range(c+1,c+len(funcstart)):
                path[i] = " "

        #print("New Path: %s" % (path,))

    MAIN = ",".join(list([ c for c in path if c != " " ]))

    return [MAIN,] + FUNCS
    
if args.p2:
    print("Doing part 2")

    instrs = instructions[:]
    instrs[0] = 2
    
    MAIN = "A,B,A,C,B,C,B,C,A,C"
    A = "L,10,R,12,R,12"
    B = "R,6,R,10,L,10"
    C = "R,10,L,10,L,12,R,6"
    CONTINUOUS = "n"

    path = genpath(grid)

    print("Path (%s): %s" % (len(",".join([str(c) for c in path])),",".join([str(c) for c in path]),))

    MAIN,A,B,C = zippath(path)

    print("zipped up: %s [ %s %s %s]" % (MAIN, A, B, C, ))
    
    input = [ ord(c) for x in ( MAIN, "\n", A, "\n", B, "\n", C, "\n", CONTINUOUS, "\n", ) for c in x ]

    print("Input: %s" % (input,))
    
    g = genoutput(instrs, iter(input))

    lines = []
    l = []
    for o in g:
        if o >= 0 and o <= 255:
            if o == ord('\n'):
                print("".join(l))
                l = []
            else:
                l.append(chr(o))
        else:
            print("Output: %s" % (o,))
