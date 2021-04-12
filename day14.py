from collections import defaultdict
import math

def make_fuel(what_i_need):
    leftovers = defaultdict(int)
    #While I need more than just Ore
    while(set(what_i_need.keys()) != set(base_elements)):
        tmp = defaultdict(int)
        for element, quantity in what_i_need.items():
            #Carry Base Elements
            if element in base_elements:
                tmp[element] += quantity
            else:
                #Apply Leftovers if they exist
                if(leftovers[element] >= 0):
                    adjusted_quantity = quantity - min(quantity, leftovers[element])
                    mult = math.ceil(float(adjusted_quantity) / quantities[element])
                    leftovers[element]-= min(quantity, leftovers[element])
                else:
                    mult = math.ceil(float(quantity) / quantities[element])
                    adjusted_quantity = quantity

                #Add Leftovers If we've created them
                leftovers[element] += max((quantities[element]*mult)-adjusted_quantity, 0)

                for q, e in rules[element]:
                    tmp[e]+=q*mult
        what_i_need = tmp

    #Finishing Steps Once Everything is in Base Elements
    ore = 0
    for element, quantity in what_i_need.items():
        mult = math.ceil(float(quantity) / quantities[element])
        for q, e in rules[element]:
            ore+=q*mult
    
    return(ore)

if __name__ == '__main__':
    with(open('data/day14.txt')) as f:
        dt = f.readlines()

    rules = defaultdict(list)
    quantities = {}
    #base elements are things that ORE directly converts into
    base_elements = []

    for s in dt:
        splt = s.replace('\n','').split(' => ')
        #Process Resulting Reaction
        res = splt[1].split(' ')
        quantities[res[1]] = int(res[0])
        #Process Inputs
        for ing in splt[0].split(', '):
            tmp = ing.split(' ')
            rules[res[1]].append((int(tmp[0]), tmp[1]))
            if tmp[1] == "ORE":
                base_elements.append(res[1])
    
    ###Part 1: Solve for 1 Fuel
    what_i_need = defaultdict(int)
    for amt, element in [x for x in rules['FUEL']]:
        what_i_need[element] += amt
    
    print("PART 1:", make_fuel(what_i_need))

    ###Part 2
    def init_array(fuel_to_make):
        what_i_need = defaultdict(int)
        for amt, element in [x for x in rules['FUEL']]:
            what_i_need[element] += amt*fuel_to_make
        return(what_i_need)

    s = 1000000
    e = 1500000

    while(abs(s-e) > 1):
        chk = round((s+e)/2)
        res = make_fuel(init_array(chk))
        if res <= 1000000000000:
            s = chk
        else:
            e = chk
    
    print("PART 2:", s)
    