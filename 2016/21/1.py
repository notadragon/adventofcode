#!/usr/bin/env python

import re, md5

password = "abcdefgh"

for l in open("input").readlines():
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
        i = int(splitup[2])
        j = int(splitup[5])

        newpw = [x for x in password]

        c = newpw[i]
        del newpw[i]
        newpw = newpw[0:j] + [c,] + newpw[j:]
        
        password = "".join(newpw)
        
        continue
    elif splitup[0] == "rotate":
        ramt = 0
        if splitup[1] == "left":
            ramt = -int(splitup[2])
        elif splitup[1] == "right":
            ramt = int(splitup[2])
        elif splitup[1] == "based":
            l = splitup[6]
            ramt = password.index(l)
            if ramt >= 4:
                ramt = ramt + 1
            ramt = ramt + 1
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
