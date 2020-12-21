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

lineRe = re.compile("([a-z ]*) \(contains ([a-z, ]+)\)")

foods = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    ingredients = m.group(1).split(" ")
    allergens = [ x.strip() for x in m.group(2).split(",") ]
    foods.append( (ingredients,allergens,))

#for food in foods:
#    print("Food: %s" % (food,))

if True:
    
    allallergens = {}
    allingredients = set()
    for ingredients, allergens in foods:
        ingredientsset = set(ingredients)
        allingredients = allingredients.union(ingredientsset)
        for allergen in allergens:
            if allergen not in allallergens:
                allallergens[allergen] = set(ingredientsset)
            else:
                allallergens[allergen] = allallergens[allergen].intersection(ingredientsset)

    changed = True
    while changed:
        changed = False
        for allergen,possible in allallergens.items():
            if len(possible) == 1:
                ing = next(iter(possible))
                for other,otherpossible in allallergens.items():
                    if other != allergen and ing in otherpossible:
                        otherpossible.remove(ing)
                        changed = True

    safeingredients = set(allingredients)
    for allergen,possible in allallergens.items():
        safeingredients.difference_update(possible)
        #print("%s -> %s" % (allergen,possible,))

    print("Ingredients: %s  safe: %s" % (len(allingredients),len(safeingredients),))

if args.p1:
    print("Doing part 1")

    total = 0
    for ingredients, allergens in foods:
        total += len([ ing for ing in ingredients if ing in safeingredients])
    print("Total Safe Uses: %s" % (total,))
    
if args.p2:
    print("Doing part 2")

    sallergens = list(allallergens.keys())
    sallergens.sort()
    singredients = []
    for allergen in sallergens:
        ingredient = next(iter(allallergens[allergen]))
        singredients.append(ingredient)
        print("%s -> %s" % (allergen,ingredient,))

    print("Canonical: %s" % (",".join(singredients),))
