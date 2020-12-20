#!/usr/bin/env pypy

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

lineRe = re.compile("(?:Tile (\d+))|([\\.#]+)")
tilesraw = {}

currenttile = None
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        tilenum = int(m.group(1))
        currenttile = []
        tilesraw[tilenum] = currenttile
    else:
        currenttile.append(m.group(2))

def isqrt(n):
    if n > 0:
        x = 1 << (n.bit_length() + 1 >> 1)
        while True:
            y = (x + n // x) >> 1
            if y >= x:
                return x
            x = y
    elif n == 0:
        return 0

gridsize = isqrt(len(tilesraw))
tilesize = len(currenttile)

print("# of tiles (%s x %s) : %s (%s x %s)" % (tilesize,tilesize,len(tilesraw),gridsize,gridsize,))

seamonster = [ "                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   ", ]

class Monster:
    def __init__(self):
        self.visible = {}
        for y in range(0,len(seamonster)):
            for x in range(0, len(seamonster[0])):
                if seamonster[y][x] == "#":
                    self.visible[ (x,y) ] = "#"
        self.width = ( len(seamonster[0]), len(seamonster), )

monster = Monster()

class Tile:
    def __init__(self, num, data, orientation):
        self.num = num
        self.data = data
        self.orientation = orientation
        self.tilesize = len(data)

    def getElement(self, x, y):
        if self.orientation < 0:
            o = 4 + self.orientation
            x = self.tilesize-x - 1
        else:
            o = self.orientation
        for i in range(0,o):
            x, y = (y, self.tilesize - x - 1)
        return self.data[y][x]

    def isAdjacent(self, rhs, direction):
        for i in range(0,self.tilesize):
            if direction == 0:
                x1 = i
                y1 = 0
                x2 = i
                y2 = self.tilesize -1
            elif direction == 1:
                x1 = self.tilesize - 1
                y1 = i
                x2 = 0
                y2 = i
            elif direction == 2:
                x1 = i
                y1 = self.tilesize - 1
                x2 = i
                y2 = 0
            elif direction == 3:
                x1 = 0
                y1 = i
                x2 = self.tilesize - 1
                y2 = i
            if self.getElement(x1, y1) != rhs.getElement(x2,y2):
                return False
        return True

    def show(self):
        for y in range(0,self.tilesize):
            row = []
            for x in range(0,self.tilesize):
                row.append(self.getElement(x,y))
            print("".join(row))

    def hasMonster(self,x,y):
        for mloc in monster.visible.keys():
            vloc = ( x + mloc[0], y + mloc[1])
            seen = self.getElement(vloc[0], vloc[1])
            if seen != "#":
                return False
        return True    

tiles = [ Tile(num,data,0) for num,data in tilesraw.items() ]

#for t in tiles:
#    t.show()

dirdeltas = { 0 : (0, -1),
              1 : (1, 0),
              2 : (0, 1),
              3 : (-1, 0) }

class Board:
    def __init__(self,tiles):
        self.tiles = tiles

        self.placedTiles = { (0,0) : tiles[0] }
        self.corners = ( (0,0), (0,0) )

        self.tilelocs = { tiles[0].num : (0,0) }

        print("Initial Placement: %s:%s at %s" % (tiles[0].num, tiles[0].orientation, (0,0), ) )
        
    def placeTiles(self):
        if len(self.placedTiles) == len(self.tiles):
            return

        locs = []
        width = ( self.corners[1][0] - self.corners[0][0] + 1,
                  self.corners[1][1] - self.corners[0][1] + 1)
        if width[0] < gridsize :
            # try to extend in x direction
            #print("Extending E/W")
            wloc = None
            eloc = None
            for loc in self.placedTiles.keys():
                if not wloc and loc[0] == self.corners[0][0]:
                    wloc = (loc[0] - 1, loc[1],) 
                if not eloc and loc[0] == self.corners[1][0]:
                    eloc = (loc[0] + 1, loc[1],) 
                if wloc and eloc:
                    locs = [ wloc, eloc, ]
                    break
        elif width[1] < gridsize :
            # try to extend in y direction
            #print("Extending N/S")
            nloc = None
            sloc = None
            for loc in self.placedTiles.keys():
                if not nloc and loc[1] == self.corners[0][1]:
                    nloc = (loc[0], loc[1] - 1,) 
                if not sloc and loc[1] == self.corners[1][1]:
                    sloc = (loc[0], loc[1] + 1,)
                if nloc and sloc:
                    locs = [ nloc, sloc, ]
                    break
        else:
            # pick an unfilled spot adjacent to something to fill in
            #print("Finding Empty Spot")
            for x in range(self.corners[0][0], self.corners[1][0] + 1):
                for y in range(self.corners[0][1], self.corners[1][1] + 1):
                    if (x,y) in self.placedTiles:
                        continue
                    for delta in dirdeltas.values():
                        if (x + delta[0], y + delta[1]) in self.placedTiles:
                            locs.append( (x,y) )
                            break
                    if locs:
                        break
                if locs:
                    break

        if not locs:
            #print("No viable locations?")
            return
        
        #print("Seeking placements for: %s (Corners: %s)" % (locs,self.corners,))
        
        origcorners = self.corners

        for loc in locs:
            newcorners = ( (min(origcorners[0][0], loc[0]), min(origcorners[0][1], loc[1]),),
                           (max(origcorners[1][0], loc[0]), max(origcorners[1][1], loc[1]),), )
            for t in self.tiles:
                if t.num in self.tilelocs:
                    continue
                for orientation in range(-4,4):
                    rt = Tile(t.num, t.data, orientation)
                    if self.canPlace(loc,rt):
                        #print("Can place %s:%s at %s" % (rt.num, orientation, loc,) )

                        # try to place, then call placeTiles recursively
                        self.tilelocs[rt.num] = loc
                        self.corners = newcorners
                        self.placedTiles[ loc ]  = rt
                        
                        self.placeTiles()

                        if len(self.placedTiles) == len(self.tiles):
                            #print("FINISHED!")
                            return
                        #print("Undoing placement of %s:%s at %s" % (rt.num, orientation, loc,) )

                        del self.tilelocs[rt.num]
                        self.corners = origcorners
                        del self.placedTiles[loc]
                        
                        

    def canPlace(self, loc, tile):
        for ddir,delta in dirdeltas.items():
            dloc = ( loc[0] + delta[0], loc[1] + delta[1], )
            if dloc in self.placedTiles:
                otherTile = self.placedTiles[dloc]
                if not tile.isAdjacent(otherTile, ddir):
                    return False
        return True

    def realImage(self):
        grid = []
        for y in range(self.corners[0][1], self.corners[1][1] + 1):
            for ty in range(1,tilesize - 1):
                row = []
                for x in range(self.corners[0][0], self.corners[1][0] + 1):
                    t = self.placedTiles[ (x,y) ]
                    for tx in range(1,tilesize - 1):
                        row.append(t.getElement(tx,ty))
                grid.append("".join(row))
        return grid
                
                
board = Board(tiles)
board.placeTiles()

if args.p1:
    print("Doing part 1")


    print("Placed Tiles: %s" % (len(board.placedTiles),))

    corners = [ board.corners[0],
                board.corners[1],
                ( board.corners[0][0], board.corners[1][1], ),
                ( board.corners[1][0], board.corners[0][1], ), ]
    product = 1
    for c in corners:
        t = board.placedTiles[c]
        product *= t.num
        print("  Corner: %s tile: %s:%s" % (c, t.num, t.orientation, ) )
    print("Product: %s" % (product,))
    
if args.p2:
    print("Doing part 2")

    realImage = board.realImage()
    for orientation in range(-4,4):
        imageTile = Tile(-1, realImage, orientation)

        #print("Orientation: %s" % (orientation,))
        #imageTile.show()

        monsters = []
        for y in range(0, imageTile.tilesize - monster.width[1]):
            for x in range(0, imageTile.tilesize - monster.width[0]):
                if imageTile.hasMonster(x,y):
                    monsters.append( (x,y) )
        if monsters:
            print("Orientation: %s Monsters: %s" % (orientation,monsters,))

            allseen = {}
            for y in range(0, imageTile.tilesize):
                for x in range(0, imageTile.tilesize):
                    if imageTile.getElement(x,y) == "#":
                        allseen[ (x,y) ] = "#"
            
            for mloc in monsters:
                for mdelta in monster.visible.keys():
                    seenloc = ( mloc[0] + mdelta[0], mloc[1] + mdelta[1])
                    del allseen[seenloc]

            print("Choppy waters: %s" % (len(allseen),))
            
            break
