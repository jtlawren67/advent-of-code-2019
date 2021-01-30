import re
import numpy as np

def run_step(p, v):

    #For Each Moon
    for i, moon in enumerate(p):
        #Compare to Each Other Moon
        gravity = [0 for x in range(len(moon))]
        for j, comp in enumerate(p):
            if i != j:
                #+1 if the comp is higher, -1 if comp is lower
                gravity += np.sign(comp-moon)
        v[i] += gravity
        
        #Update all Positions
        p_new = [p[i] + v[i] for i in range(len(p))]
        
    return(p_new, v)

def find_iteration(p):
    p_start = p
    v = np.array([0 for i in range(len(p))])

    ctr = 0
    while True:
        ctr += 1
        
        #Run Updater
        for i, base in enumerate(p):
            gravity = np.array([0 for i in range(len(p))])
            for j, comp in enumerate(p):
                if(i != j):
                    gravity[i] += np.sign(comp-base)
            v += gravity

        p_new = [p[i] + v[i] for i in range(len(p))]
        p = p_new

        #Escape Condition
        if(np.all(p == p_start) and np.all(v==0)):
            break

    return(ctr)



if __name__ == '__main__':
    with open('data/day12.txt') as f:
        positions = [np.array(list(map(int, re.findall(r'-?\d+', line)))) for line in f.readlines()]

    velocity = [np.array([0, 0, 0]) for i in range(len(positions))]


    for i in range(1000):
        positions, velocity = run_step(positions, velocity)

    #Print Total Energy
    tot = sum([sum(np.abs(positions[i]))*sum(np.abs(velocity[i])) for i in range(len(positions))])
    print("PART 1")
    print(tot)

    ##Part 2
    with open('data/day12.txt') as f:
        positions = np.array([list(map(int, re.findall(r'-?\d+', line))) for line in f.readlines()])

    p2 = np.array([find_iteration(positions[:,i]) for i in range(positions.shape[1])], dtype='int64')
    print("PART 2")
    print(p2)
    print(np.lcm.reduce(p2))



    