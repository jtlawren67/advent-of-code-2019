from collections import defaultdict

# IntCode Computer from Day 2's Puzzle
def intcode(in_value, dt):
    pos = 0
    rel_base = 0
    while(dt[pos]%100!=99):

        op_code = dt[pos]%100
        #Figure out parameters
        params = [dt[pos]%1000//100, 
                dt[pos]%10000//1000, 
                dt[pos]%100000//10000,
                dt[pos]%1000000//100000
                ]

        insert_pos = get_insertion_position(3, pos+3, dt, params, rel_base)

        if(op_code==1):
            dt[insert_pos] = get_value(1, pos+1, dt, params, rel_base) + get_value(2, pos+2, dt, params, rel_base)
            pos += 4
        elif(op_code==2):
            dt[insert_pos] = get_value(1, pos+1, dt, params, rel_base) * get_value(2, pos+2, dt, params, rel_base)
            pos += 4
        elif(op_code==3):
            if(params[0]==2):
                dt[dt[pos+1]+rel_base] = in_value
            elif params[0]==0:
                dt[dt[pos+1]] = in_value
            else:
                print("Oops")
            pos += 2
        elif(op_code==4):
            print(get_value(1, pos+1, dt, params, rel_base))
            pos += 2
        elif(op_code==5):
            if(get_value(1, pos+1, dt, params, rel_base) != 0):
                pos = get_value(2, pos+2, dt, params, rel_base)
            else:
                pos += 3
        elif(op_code==6):
            if(get_value(1, pos+1, dt, params, rel_base) == 0):
                pos = get_value(2, pos+2, dt, params, rel_base)
            else:
                pos += 3
        elif(op_code==7):
            if(get_value(1, pos+1, dt, params, rel_base) < get_value(2, pos+2, dt, params, rel_base)):
                dt[insert_pos] = 1
            else:
                dt[insert_pos] = 0
            pos += 4
        elif(op_code==8):
            if(get_value(1, pos+1, dt, params, rel_base) == get_value(2, pos+2, dt, params, rel_base)):
                dt[insert_pos] = 1
            else:
                dt[insert_pos] = 0
            pos += 4
        elif(op_code==9):
            rel_base += get_value(1, pos+1, dt, params, rel_base)
            pos += 2

    return(dt)

def get_insertion_position(parameter, pos, dt, params, rel_base):
    if params[parameter-1]==0:
            ix = dt[pos]
    elif params[parameter-1]==2:
            ix = dt[pos]+rel_base
    return(ix)

def get_value(parameter, pos, dt, params, rel_base):
        if params[parameter-1]==1:
            ix = pos
        elif params[parameter-1]==0:
            ix = dt[pos]
        elif params[parameter-1]==2:
            ix = dt[pos]+rel_base

        return(dt[ix])


if __name__ == '__main__':
    with open('data/day09.txt') as f:
        inputs = f.readline()

    dt = defaultdict(int)
    for k,v in enumerate(inputs.split(',')):
        dt[k] = int(v)

    print("PART 1") 
    p1 = intcode(1, dt.copy())
    print("PART 2")
    p2 = intcode(2, dt.copy())
