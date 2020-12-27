def part1(dt):
    pos = 0
    while(dt[pos]!=99):
        if(dt[pos]==1):
            dt[dt[pos+3]] = dt[dt[pos+1]] + dt[dt[pos+2]]
        elif(dt[pos]==2):
            dt[dt[pos+3]] = dt[dt[pos+1]] * dt[dt[pos+2]]
        pos += 4
    return(dt)
        

if __name__ == "__main__":
    with open("data/day02.txt") as f:
        dt0 = [int(x) for x in f.readline().split(',')]

    """
    Part 1
    """
    dt1 = dt0.copy()
    dt1[1] = 12
    dt1[2] = 2
    dt1 = part1(dt1)

    #Part 1 Output
    print("Part 1 Answer:",dt1[0])

    """
    Part 2
    """
    candidates = [(noun, verb) for noun in range(100) for verb in range(100)]
    i = 1
    dt2 = dt0.copy()
    while(dt2[0] != 19690720):
        dt2 = dt0.copy()
        dt2[1] = candidates[i][0]
        dt2[2] = candidates[i][1]
        dt2 = part1(dt2)
        i = i + 1
    
    print("Part 2 Answer:", 100*candidates[i-1][0]+candidates[i-1][1])



        

        