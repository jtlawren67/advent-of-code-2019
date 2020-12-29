
def cnt_orbits(it):
    if(len(orbits[it])==0):
        return(0)
    elif orbits[it]=='COM':
        return(1)
    else:
        return(1+cnt_orbits(orbits[it]))


if __name__ == '__main__':

    orbits = {}
    with(open('data/day06.txt')) as f:
    #with(open('data/test.txt')) as f:
        for i in f.readlines():
            orbits[i.strip().split(')')[1]]=i.strip().split(')')[0]
    
    """
    PART 1
    """
    p1 = sum([cnt_orbits(k) for k in orbits.keys()])
    
    print("PART 1:", p1)

    """
    PART 2
    """
    transfers = 0
    candidates = [orbits['YOU']]
    while(orbits['SAN'] not in candidates):
        prior_candidates = candidates.copy()
        transfers += 1
        backwards = [orbits[k] for k in prior_candidates if k != 'COM']
        forwards = [k for k, v in orbits.items() if v in prior_candidates]
        candidates = list(set(forwards + backwards))
    print("PART 2:", transfers)


