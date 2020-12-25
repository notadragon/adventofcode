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

lineRe = re.compile(".*")
ivals = []


for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    ivals.append(int(x))

print("Ivals: %s" % (ivals,))

def transformVal(subjectNumber,loopSize):
    val = 1
    for i in range(0,loopSize):
        val *= subjectNumber
        val %= 20201227
    return val

def loopSize(subjectNumber,key):
    val = 1
    if key == 1:
        return 0
    
    loopSize = 0
    while True:
        val *= subjectNumber
        val %= 20201227
        
        loopSize += 1
        
        if val == key:
            return loopSize
        
if False:
    cardLoopSize = "?"
    doorLoopSize = "?"
    
    cardPublicKey = transformVal(7,cardLoopSize)
    doorPublicKey = transformVal(7,doorLoopSize)

    encryptionKey = transformVal(doorPublicKey,cardLoopSize)
    encryptionKey = transformVal(cardPublicKey,doorLoopSize)

if args.p1:
    print("Doing part 1")

    cardPublicKey = ivals[0]
    doorPublicKey = ivals[1]

    cardLoopSize = loopSize(7,cardPublicKey)
    doorLoopSize = loopSize(7,doorPublicKey)

    encryptionKey1 = transformVal(doorPublicKey,cardLoopSize)
    encryptionKey2 = transformVal(cardPublicKey,doorLoopSize)
    
    print("Card Public Key: %s Loop Size: %s" % (cardPublicKey,cardLoopSize,))
    print("Door Public Key: %s Loop Size: %s" % (doorPublicKey,doorLoopSize,))

    print("EncryptionKey: %s / %s" % (encryptionKey1,encryptionKey2,))
    
if args.p2:
    print("Doing part 2")

    print("Get all stars")
