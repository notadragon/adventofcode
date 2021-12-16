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

lineRe = re.compile("[A-F0-9]+")
data = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data = x

binaryMapping = {
    "0" : "0000",
    "1" : "0001",
    "2" : "0010",
    "3" : "0011",
    "4" : "0100",
    "5" : "0101",
    "6" : "0110",
    "7" : "0111",
    "8" : "1000",
    "9" : "1001",
    "A" : "1010",
    "B" : "1011",
    "C" : "1100",
    "D" : "1101",
    "E" : "1110",
    "F" : "1111",
    }

bits = "".join([ binaryMapping[c] for c in data ])

print(f"Bits: {bits}")

def packets(bits, offset = 0):
    begin = 0
    while begin < len(bits) - 6:
        version = int(bits[begin:begin+3],2)
        typeid = int(bits[begin+3:begin+6],2)

        #print(f"{begin} / {len(bits)}  version: {version}  typeid: {typeid} ")

        if typeid == 4:
            x = begin+6
            number = [ bits[x+1:x+5] ]
            while bits[x] == "1":
                x = x + 5
                number.append(bits[x+1:x+5])
            number = "".join(number)
            end = x + 5
            yield ( offset + begin, offset + end, version, typeid, number )
            begin = end
        else:
            if len(bits) <= begin+6:
                break
            lengthtypeid = bits[begin+6]
            if lengthtypeid == "0":
                x = begin + 7
                if len(bits) <= x+15:
                    break
                totallength = int(bits[x:x+15],2)
                x = x + 15
                end = x + totallength

                subpackets = []
                for p in packets(bits[x:end], x + offset):
                    subpackets.append( p )
                
                yield ( offset + begin, offset + end, version, typeid, lengthtypeid, tuple(subpackets), ) 
                begin = end
            else:
                x = begin + 7
                numpackets = int(bits[x:x+11],2)
                x = x + 11

                subpackets = []
                if numpackets > 0:
                    subpacketgen = packets(bits[x:],x + offset)
                    for p in subpacketgen:
                        subpackets.append( p )
                        if len(subpackets) >= numpackets:
                            break
                    end = subpackets[-1][1] - offset
                else:
                    end = x

                yield ( offset + begin, offset + end, version, typeid, lengthtypeid, tuple(subpackets), )
                begin = end
        
    #yield (offset + begin,offset + len(bits),)
    #print(f"Remaining bits: {bits[begin:]}")
    
def versiontotal(packet):
    if len(packet) < 3:
        return 0
    
    output = packet[2]

    if packet[3] != 4:
        for p in packet[5]:
            output = output + versiontotal(p)

    return output


def show(packet,indent=""):
    #print(f"{packet}")
    if packet[3] == 4:
        print(f"{indent}v:{packet[2]} t:{packet[3]} l:{packet[4]}")
    else:
        print(f"{indent}v:{packet[2]} t:{packet[3]} lt:{packet[4]}")
        sindent = indent + "  "
        for p in packet[5]:
            show(p,sindent)
        
        
if args.p1:
    print("Doing part 1")

    for p in packets(bits):
        show(p)
        print(f"{versiontotal(p)}")

def calculate(packet):
    typeid = packet[3]
    if typeid== 4:
        return int(packet[4],2)

    vals = [ calculate(p) for p in packet[5] ]

    if typeid == 0:
        return sum(vals)
    elif typeid == 1:
        return math.prod(vals)
    elif typeid == 2:
        return min(vals)
    elif typeid == 3:
        return max(vals)
    elif typeid == 5:
        if vals[0] > vals[1]:
            return 1
        else:
            return 0
    elif typeid == 6:
        if vals[0] < vals[1]:
            return 1
        else:
            return 0
    elif typeid == 7:
        if vals[0] == vals[1]:
            return 1
        else:
            return 0        
    
if args.p2:
    print("Doing part 2")

    for p in packets(bits):
        val = calculate(p)
        print(f"Calculated Value: {val}")
