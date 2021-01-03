import numpy as np
from collections import defaultdict
import math

def num_detected(location, asteroids): 
    a2 = [asteroids[i] for i in range(asteroids.shape[0]) if not all(asteroids[i] == location)]
    deltas = a2 - location
    return(len(np.unique(np.arctan2(deltas[:, 0], deltas[:, 1]))))

def laser200(location, asteroids):
    #Flip the Positions back
    location = location[::-1]
    a2 = [asteroids[i][::-1] for i in range(asteroids.shape[0]) if not all(asteroids[i] == location[::-1])]
    deltas = location - a2
    tangents = np.arctan2(deltas[:, 1], deltas[:, 0])*(180 / math.pi)
    alter_degree = lambda x: x if x >= 0 else x + 360
    tangents = np.array([alter_degree(x-90) for x in tangents])
    distances = np.array([math.sqrt((location[0]-i[0])**2 + (location[1]-i[1])**2) for i in a2])
    inds = distances.argsort()
    tangent_list = defaultdict(list)

    #Sort Tangent List and Asteroid List by Distances
    a2_sort = np.array(a2)[inds]
    tangent_sort = tangents[inds]

    #Load Points by Distance and by Tangent
    for i in range(len(a2_sort)):
        tangent_list[tangent_sort[i]].append(a2_sort[i])


    angles = np.unique(tangents)
    popped = 0
    idx = 0
    while(popped < 200):
        val = tangent_list[angles[idx%len(angles)]].pop(0)
        popped += 1
        idx += 1

    return(val)


            
if __name__ == '__main__':
    with open('data/day10.txt') as f:
        inputs = [list(l.strip()) for l in f.readlines()]

    m = np.array(inputs)

    #Get Number of And Location of Asteroids
    asteroids = np.asarray(np.where(m == '#')).T

    #Iterate Through Asteroid Locations And Count Number of Asteroids
    cnt_detected = [num_detected(location, asteroids.copy()) for location in asteroids]

    print("PART 1:", max(cnt_detected))

    """
    PART 2
    """
    p2 = laser200(asteroids[cnt_detected.index(max(cnt_detected))],
    asteroids.copy())
    print ("PART 2:", p2[0]*100+p2[1])
