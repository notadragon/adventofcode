#!/usr/bin/env python

import re, md5

password = "fbgdceah"

for l in open("input").readlines()[::-1]:
    l = l.strip()

    print password
    print l

    splitup = l.split(" ")
    if splitup[0] == "swap":
        if splitup[1] == "letter":
            l1 = splitup[2]
            l2 = splitup[5]
            newpw = []
            for p in password:
                if p == l1:
                    newpw.append(l2)
                elif p == l2:
                    newpw.append(l1)
                else:
                    newpw.append(p)
            password = "".join(newpw)
        elif splitup[1] == "position":
            pos1 = int(splitup[2])
            pos2 = int(splitup[5])
            newpw = [x for x in password]
            tmp = newpw[pos1]
            newpw[pos1] = newpw[pos2]
            newpw[pos2] = tmp
            password = "".join(newpw)
        continue
    elif splitup[0] == "move":
        j = int(splitup[2])
        i = int(splitup[5])

        newpw = [x for x in password]

        c = newpw[i]
        del newpw[i]
        newpw = newpw[0:j] + [c,] + newpw[j:]
        
        password = "".join(newpw)
        
        continue
    elif splitup[0] == "rotate":
        ramt = 0
        if splitup[1] == "left":
            ramt = int(splitup[2])
        elif splitup[1] == "right":
            ramt = -int(splitup[2])
        elif splitup[1] == "based":
            l = splitup[6]
            lpos = password.index(l)
            ramt = 0
            for i in range(0,len(password)):
                if i >= 4:
                    iamt = i + 2
                else:
                    iamt = i + 1
                if lpos == ((i + iamt) % len(password)):
                    ramt = -iamt
                    break
            if ramt == 0:
                print "WTF"
                
        if ramt > 0:
            ramt = ramt % len(password)
            password = password[-ramt:] + password[0:-ramt]
        elif ramt < 0:
            ramt = -ramt
            ramt = ramt % len(password)
            password = password[ramt:] + password[0:ramt]
        continue
    elif splitup[0] == "reverse":
        start = int(splitup[2])
        end = int(splitup[4])
        password = password[0:start] + password[start:end+1][::-1] + password[end+1:]
        continue


print password
