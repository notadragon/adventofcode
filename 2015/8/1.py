#!/usr/bin/env python

import re

lineRe = re.compile("\"(.*)\"")

escapeRe = re.compile("\\\\\\\\|\\\\\"|\\\\x[0-9a-f][0-9a-f]")

codesize=0
datasize=0
escapedsize=0

def encode(line):
    m = lineRe.match(line)
    if not m:
        print "Invalid String %s" % (line,)
        return None

    string = m.group(1)
    
    out = ""
    escaping = False
    hexnum = ""
    
    for x in string:
        if x == "\"":
            if escaping == 1:
                out = out + "\""
                escaping = escaping - 1
            else:
                print "Unescaped \" in %s" % (line,)
                return None
        elif x == "\\":
            if escaping:
                out = out + "\\"
                escaping = 0
            else:
                escaping = 1
        elif x == "x":
            if escaping == 1:
                escaping = 2
            else:
                out = out + x
        elif x in "0123456789abcdef":
            if escaping == 2:
                hexnum = x
                escaping = 3
            elif escaping == 3:
                hexnum = hexnum + x
                out = out + chr(int(hexnum,16))
                escaping = 0
            else:
                out = out + x
        else:
            if escaping != 0:
                print "Invalid escape %s in %s" % (x, line,)
                return None
            else:
                out = out + x
    return out

def escape(line):
    out = ""
    for x in line:
        if x == "\"":
            out = out + "\\\""
        elif x == "\\":
            out = out + "\\\\"
        elif x not in "abcdefghijklmnopqrstuvwxyz01234567890":
            out = out + "\\" + hex(ord(x))[1:]
        else:
            out = out + x
    return "\"" + out + "\""

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    fixedLine = encode(line)
    escapedLine = escape(line)
    
    codesize = codesize + len(line)
    datasize = datasize + len(fixedLine)
    escapedsize = escapedsize + len(escapedLine)

    reescaped = encode(escapedLine)
    if reescaped != line:
        print "Re-escaping does not work %s != %s" % (line,reescaped,)
        break

    
    reencoded = escape(fixedLine)
    #theree are ascii characters encoded using \x.. 
    #if reencoded != line:
    #    print "Re-encoding does not work %s != %s" % (line,reencoded,)
    #    break        
    
    print "Line (%i): %s Value(%i): %s Escaped(%i): %s" % (len(line),line,len(fixedLine),fixedLine,len(escapedLine),escapedLine)

print "Total Code: %i Total Data: %i  Result: %i  Total Escaped: %i Result2: %i" % (codesize, datasize, codesize-datasize, escapedsize, escapedsize-codesize)
