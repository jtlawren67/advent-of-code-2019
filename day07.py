from itertools import permutations  

# IntCode Computer from Day 2's Puzzle
def intcode(in_value1, in_value2, dt, pos = 0, int_value = 1):
    #pos = 0
    #int_value = 1
    while(dt[pos]%100!=99):
        op_code = dt[pos]%100
        #Figure out parameters
        params = [dt[pos]%1000//100, 
                dt[pos]%10000//1000, 
                dt[pos]%100000//10000,
                dt[pos]%1000000//100000
                ]

        #Apply Immediate Mode (1) vs. Position Mode (0)
        get_value = lambda parameter, pos: dt[pos] if params[parameter-1]==1 else dt[dt[pos]]

        if(op_code==1):
            dt[dt[pos+3]] = get_value(1, pos+1) + get_value(2, pos+2)
            pos += 4
        elif(op_code==2):
            dt[dt[pos+3]] = get_value(1, pos+1) * get_value(2, pos+2)
            pos += 4
        elif(op_code==3):
            if int_value == 1:
                dt[dt[pos+1]] = in_value1
            elif int_value == 2:
                dt[dt[pos+1]] = in_value2
            else:
                #Pause to wait for input
                return([output, dt, pos, int_value, "P"])
            int_value += 1
            pos += 2
        elif(op_code==4):
            output = get_value(1, pos+1)
            pos += 2
        elif(op_code==5):
            if(get_value(1, pos+1) != 0):
                pos = get_value(2, pos+2)
            else:
                pos += 3
        elif(op_code==6):
            if(get_value(1, pos+1) == 0):
                pos = get_value(2, pos+2)
            else:
                pos += 3
        elif(op_code==7):
            if(get_value(1, pos+1) < get_value(2, pos+2)):
                dt[dt[pos+3]] = 1
            else:
                dt[dt[pos+3]] = 0
            pos += 4
        elif(op_code==8):
            if(get_value(1, pos+1) == get_value(2, pos+2)):
                dt[dt[pos+3]] = 1
            else:
                dt[dt[pos+3]] = 0
            pos += 4

    return([output, dt, pos, int_value, "D"])

if __name__ == '__main__':

    with open('data/day07.txt') as f:
        dt =  [int(x) for x in f.readline().split(',')]

    """
    PART 1
    """
    # Generate All Potential Sequences 
    perms = permutations([0, 1, 2, 3, 4])

    # Run an Amplifier Series Given a sequence
    max_value = 0
    for p in list(perms):
        value = 0
        for i in range(5):
            value = intcode(p[i], value, dt.copy())[0]
        if value > max_value:
            max_value = value
            max_perm = p

    print("PART 1:", max_value, max_perm)

    """
    PART 2
    """

    perm2 = permutations([5, 6, 7, 8, 9])
    max_value2 = -999999
    for p in list(perm2):
        val = -999999

        #Initialize All States
        #(output, dt, pos, int_value, "D")
        amps = [[0, dt.copy(), 0, 1, "S"] for i in p]
        current_amp = 0

        #Run Until Completion
        while(amps[4][4] != 'D'):
            if amps[current_amp][4] == 'S':
                amps[current_amp] = intcode(
                    p[current_amp],
                    amps[current_amp][0],
                    amps[current_amp][1],
                    amps[current_amp][2],
                    amps[current_amp][3]
                )
            else:
                amps[current_amp] = intcode(
                    amps[current_amp][0],
                    amps[current_amp][0],
                    amps[current_amp][1],
                    amps[current_amp][2],
                    2
                )
            
            #Get Next AMP and Update Value
            val = amps[current_amp][0]
            current_amp = (current_amp + 1)%5
            amps[current_amp][0] = val

        #Check Against Max
        if val > max_value2:
            max_value2 = val
            max_perm2 = p

    print("PART 2:", max_value2, max_perm2)

    
