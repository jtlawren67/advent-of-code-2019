from collections import defaultdict

class Intcode:
    def __init__(self, program):
        self.pos = 0
        self.rel_base = 0
        self.output = []
        self.in_value = []

        self.dt = program
        self.finished = False

    def get_insertion_position(self, parameter, pos, dt, params, rel_base):
        if params[parameter-1]==0:
                ix = dt[pos]
        elif params[parameter-1]==2:
                ix = dt[pos]+rel_base
        return(ix)

    def get_value(self, parameter, pos, dt, params, rel_base):
            if params[parameter-1]==1:
                ix = pos
            elif params[parameter-1]==0:
                ix = dt[pos]
            elif params[parameter-1]==2:
                ix = dt[pos]+rel_base

            return(dt[ix])

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.output) == 0: raise StopIteration()
        return self.output.pop(0)

    def run(self):
        while(True):

            op_code = self.dt[self.pos]%100
            #Figure out parameters
            params = [self.dt[self.pos]%1000//100, 
                    self.dt[self.pos]%10000//1000, 
                    self.dt[self.pos]%100000//10000,
                    self.dt[self.pos]%1000000//100000
                    ]

            insert_pos = self.get_insertion_position(3, self.pos+3, self.dt, params, self.rel_base)

            if(op_code==1):
                self.dt[insert_pos] = self.get_value(1, self.pos+1, self.dt, params, self.rel_base) + self.get_value(2, self.pos+2, self.dt, params, self.rel_base)
                self.pos += 4
            elif(op_code==2):
                self.dt[insert_pos] = self.get_value(1, self.pos+1, self.dt, params, self.rel_base) * self.get_value(2, self.pos+2, self.dt, params, self.rel_base)
                self.pos += 4
            elif(op_code==3):
                if len(self.in_value) == 0: return
                if(params[0]==2):
                    self.dt[self.dt[self.pos+1]+self.rel_base] = self.in_value.pop(0)
                elif params[0]==0:
                    self.dt[self.dt[self.pos+1]] = self.in_value.pop(0)
                else:
                    print("Oops")
                self.pos += 2
            elif(op_code==4):
                self.output.append(self.get_value(1, self.pos+1, self.dt, params, self.rel_base))
                self.pos += 2
            elif(op_code==5):
                if(self.get_value(1, self.pos+1, self.dt, params, self.rel_base) != 0):
                    self.pos = self.get_value(2, self.pos+2, self.dt, params, self.rel_base)
                else:
                    self.pos += 3
            elif(op_code==6):
                if(self.get_value(1, self.pos+1, self.dt, params, self.rel_base) == 0):
                    self.pos = self.get_value(2, self.pos+2, self.dt, params, self.rel_base)
                else:
                    self.pos += 3
            elif(op_code==7):
                if(self.get_value(1, self.pos+1, self.dt, params, self.rel_base) < self.get_value(2, self.pos+2, self.dt, params, self.rel_base)):
                    self.dt[insert_pos] = 1
                else:
                    self.dt[insert_pos] = 0
                self.pos += 4
            elif(op_code==8):
                if(self.get_value(1, self.pos+1, self.dt, params, self.rel_base) == self.get_value(2, self.pos+2, self.dt, params, self.rel_base)):
                    self.dt[insert_pos] = 1
                else:
                    self.dt[insert_pos] = 0
                self.pos += 4
            elif(op_code==9):
                self.rel_base += self.get_value(1, self.pos+1, self.dt, params, self.rel_base)
                self.pos += 2
            elif(op_code==99):
                self.finished = True
                return
            else:
                print("Something has gone wrong")

    def send(self, value):
        self.in_value.append(value)

if __name__ == '__main__':
    with(open('data/day17.txt')) as f:
        inputs = f.readline()
    
    dt = defaultdict(int)
    for k,v in enumerate(inputs.split(',')):
        dt[k] = int(v)

    computer = Intcode(dt.copy())
    computer.run()

    break_ids = []

    #Get the dimensions of the board
    for (ix, i) in enumerate(computer.output):
        if(i==10):
            break_ids.append(ix)

    BOARD_ROWS = len(break_ids)
    BOARD_COLS = break_ids[0]

    # board[y][x]
    board = [['' for c in range(BOARD_COLS)] for r in range(BOARD_ROWS)]

    # fill board
    x = 0
    y = 0

    for ele in computer.output:
        if ele != 10:
            board[y][x] = chr(ele)
            x += 1
        elif ele == 10:
            x = 0
            y += 1
    
    #Check for Intersections
    intersections = []
    for y in range(1, BOARD_ROWS-1):
        for x in range(1, BOARD_COLS-1):
            if board[y][x]=="#" and board[y-1][x]=="#" and board[y+1][x]=="#" and board[y][x-1]=="#" and board[y][x+1]=="#":
                intersections.append(x*y)


    print("PART 1:", sum(intersections))

    #PART 2
    dt2 = dt.copy()
    dt2[0] = 2
    pt2 = Intcode(dt2)

    #Develop Inputs
    main_sequence = 'A,B,B,A,C,A,C,A,C,B'
    seq_a = 'L,6,R,12,R,8'
    seq_b = 'R,8,R,12,L,12'
    seq_c = 'R,12,L,12,L,4,L,4'

    #Send items
    all_items = [ord(i) for i in main_sequence]
    all_items.append(10)
    all_items += [ord(i) for i in seq_a]
    all_items.append(10)
    all_items += [ord(i) for i in seq_b]
    all_items.append(10)
    all_items += [ord(i) for i in seq_c]
    all_items.append(10)
    all_items.append(ord('n'))
    all_items.append(10)
    
    for i in all_items: pt2.send(i)

    pt2.run()

    print("PART 2", pt2.output[-1])
