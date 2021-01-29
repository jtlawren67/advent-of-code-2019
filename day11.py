from collections import defaultdict
import numpy as np

# IntCode Computer from Day 2's Puzzle
def intcode(dt):
    pos = 0
    rel_base = 0
    output = None
    in_value = None
    while(True):

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
            in_value = yield output
            output = None
            if(params[0]==2):
                dt[dt[pos+1]+rel_base] = in_value
            elif params[0]==0:
                dt[dt[pos+1]] = in_value
            else:
                print("Oops")
            pos += 2
        elif(op_code==4):
            if output is not None:
                temp = yield output
                assert temp is None
            output = get_value(1, pos+1, dt, params, rel_base)
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
        elif(op_code==99):
            yield output
            return
        else:
            print("Something has gone wrong")

    return(dt[pos], dt)

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
    with open('data/day11.txt') as f:
        inputs = f.readline()

    dt = defaultdict(int)
    for k,v in enumerate(inputs.split(',')):
        dt[k] = int(v)

    directions = {
        0: (0, 1),
        1: (-1, 0),
        2: (0, -1),
        3: (1, 0)
    }

    current_pos = (0, 0)
    current_dir = 0

    white_tiles = set()
    black_tiles = set()

    #Set up Generator
    p1 = intcode(dt.copy())
    assert next(p1) is None
    i = 0

    while True:
        i += 1
        try:
            if current_pos in white_tiles:
                color = p1.send(1)
            else:
                color = p1.send(0)

            direction = next(p1)
    
            #Paint Tiles
            if(color == 0): #Paint Black
                black_tiles.add(current_pos)
                white_tiles.discard(current_pos)
            elif(color == 1): #Paint White
                black_tiles.discard(current_pos)
                white_tiles.add(current_pos)

            #Change Direction
            current_dir =  (current_dir + 1)%4 if direction == 0 else (current_dir - 1)%4
            #Move
            current_pos = (current_pos[0] + directions[current_dir][0],
                            current_pos[1] + directions[current_dir][1]
            )

        except StopIteration:
            break

    
    print("PART 1")
    print(len(black_tiles) + len(white_tiles))
    
    print("PART 2")
    # Re-run but start on a white panel
    current_pos = (0, 0)
    current_dir = 0

    white_tiles = set([(0, 0)])
    black_tiles = set()

    #Set up Generator
    p1 = intcode(dt.copy())
    assert next(p1) is None
    i = 0

    while True:
        i += 1
        try:
            if current_pos in white_tiles:
                color = p1.send(1)
            else:
                color = p1.send(0)

            direction = next(p1)
    
            #Paint Tiles
            if(color == 0): #Paint Black
                black_tiles.add(current_pos)
                white_tiles.discard(current_pos)
            elif(color == 1): #Paint White
                black_tiles.discard(current_pos)
                white_tiles.add(current_pos)

            #Change Direction
            current_dir =  (current_dir + 1)%4 if direction == 0 else (current_dir - 1)%4
            #Move
            current_pos = (current_pos[0] + directions[current_dir][0],
                            current_pos[1] + directions[current_dir][1]
            )

        except StopIteration:
            break

    ##PAINT LETTERS
    ####Build Grid
    x_min = min([i[0] for i in white_tiles.union(black_tiles)])
    x_max = max([i[0] for i in white_tiles.union(black_tiles)])
    y_min = min([i[1] for i in white_tiles.union(black_tiles)])
    y_max = max([i[1] for i in white_tiles.union(black_tiles)])

    m = np.zeros((y_max-y_min+1, x_max-x_min+1))

    m = [[' ' for x in range(x_max-x_min+1)] for y in range(y_max-y_min+1)]

    #####Paint
    for i in white_tiles:
        m[i[1]+abs(y_min)][i[0]] = '1'

    for i in m[::-1]:
        print(''.join(i))