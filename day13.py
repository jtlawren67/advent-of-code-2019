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
    with open('data/day13.txt') as f:
        inputs = f.readline()

    dt = defaultdict(int)
    for k,v in enumerate(inputs.split(',')):
        dt[k] = int(v)

    #Set up Class
    p1 = Intcode(dt.copy())

    p1.run()
    panels = defaultdict(list)
    for x, y, tile_id in zip(*[p1] * 3):
        panels[tile_id].append((x, y))

    print("PART 1:", len(panels[2]))

    #How big is the board

    ####PART 2
    score = 0
    dt2 = dt.copy()
    dt2[0] = 2
    p2 = Intcode(dt2)
    panels = [[0 for _ in range(38)] for _ in range(21)]

    while(not p2.finished):
        p2.run()
        
        for x, y, tile_id in (zip(*[p2] * 3)):

            if(x == -1 and y == 0):
                score = tile_id
            else:
                panels[y][x] = tile_id

            if tile_id == 3:
                paddle = x
            elif tile_id == 4:
                ball = x

        if ball > paddle:
            p2.send(1)
        elif ball < paddle:
            p2.send(-1)
        else:
            p2.send(0)

    print("FINAL SCORE: ", score)   
        
