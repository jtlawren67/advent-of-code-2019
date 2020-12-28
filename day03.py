def expand_string2(s):
    result = list()
    current_pos = (0, 0)
    directions = s.split(',')
    for i in directions:
        d = i[0]
        n = int(i[1:])

        if d=='U':
            candidates = [(current_pos[0], i) for i in range(current_pos[1]+1, current_pos[1]+ n +1)]
            current_pos = (current_pos[0], current_pos[1] + n)
        elif d=="R":
            candidates = [(i, current_pos[1]) for i in range(current_pos[0]+1, current_pos[0]+ n +1)]
            current_pos = (current_pos[0] + n, current_pos[1])
        elif d=="D":
            candidates = [(current_pos[0], i) for i in range(current_pos[1]-1, current_pos[1]- n -1, -1)]
            current_pos = (current_pos[0], current_pos[1] - n)
        elif d=="L":
            candidates = [(i, current_pos[1]) for i in range(current_pos[0]-1, current_pos[0]- n -1, -1)]
            current_pos =  (current_pos[0] - n, current_pos[1])

        result += candidates

    return(result)

if __name__ == "__main__":

    with open('data/day03.txt') as f:
       input0 = f.readlines()

    s1 = expand_string2(input0[0])
    s2 = expand_string2(input0[1])

    p1 = min([abs(i[0])+abs(i[1]) for i in set(s1).intersection(set(s2))])
    print("Part 1 Answer:", p1)
    p2 = [s1.index(i)+s2.index(i)+2 for i in set(s1).intersection(set(s2))]
    print("Part 2 Answer", min(p2))