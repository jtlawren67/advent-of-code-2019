
# IntCode Computer from Day 2's Puzzle
def intcode(in_value, dt):
    pos = 0
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
            dt[dt[pos+1]] = in_value
            pos += 2
        elif(op_code==4):
            print(get_value(1, pos+1))
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

    return(dt)

if __name__ == '__main__':
    #in_values = '1002,4,3,4,33'

    with open('data/day05.txt') as f:
        dt =  [int(x) for x in f.readline().split(',')]

    #Part 1
    intcode(1, dt.copy())

    #Part 2
    intcode(5, dt.copy())