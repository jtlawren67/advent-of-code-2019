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
    with(open('data/day15.txt')) as f:
        inputs = f.readline()
    
    dt = defaultdict(int)
    for k,v in enumerate(inputs.split(',')):
        dt[k] = int(v)

    directions = {
        1 : (0, 1),
        2 : (0, -1),
        3 : (-1, 0),
        4 : (1, 0)
    }

    computer = Intcode(dt.copy())
    found_oxygen = False

    CURRENT_X = 0
    CURRENT_Y = 0

    pos_results = {}
    path = [(0,0)]
    to_visit = set()
    i = 0
    while(not found_oxygen or to_visit):
        i+=1

        # What are new ways we can go
        new_moves =[(idx, i) for (idx, i) in enumerate([
            (CURRENT_X + directions[1][0], CURRENT_Y + directions[1][1]),
            (CURRENT_X + directions[2][0], CURRENT_Y + directions[2][1]),
            (CURRENT_X + directions[3][0], CURRENT_Y + directions[3][1]),
            (CURRENT_X + directions[4][0], CURRENT_Y + directions[4][1]),
        ]) if i not in list(pos_results.keys())]

        #Track Places to Go
        to_visit.update([i for idx, i in new_moves])

        #Deal with Case when there are no new places to go; we need to backtrack
        if(len(new_moves)==0):
            #Undo the prior move
            path.pop(0)

            #Move Back to the last move
            new_moves =[(idx, i) for (idx, i) in enumerate([
                (CURRENT_X + directions[1][0], CURRENT_Y + directions[1][1]),
                (CURRENT_X + directions[2][0], CURRENT_Y + directions[2][1]),
                (CURRENT_X + directions[3][0], CURRENT_Y + directions[3][1]),
                (CURRENT_X + directions[4][0], CURRENT_Y + directions[4][1]),
            ]) if i == path[0]]
            #Pop off the place we're going to move to before we add it back later
            path.pop(0)

        #Try to Move First New Place
        dir_id = new_moves[0][0] + 1
        computer.send(dir_id)
        computer.run()
        status = computer.output.pop(0)

        #Update Status List
        pos_results[(CURRENT_X + directions[dir_id][0], 
                     CURRENT_Y + directions[dir_id][1])] = status

        if (CURRENT_X + directions[dir_id][0], 
            CURRENT_Y + directions[dir_id][1]) in to_visit:
                to_visit.remove((CURRENT_X + directions[dir_id][0], 
                                CURRENT_Y + directions[dir_id][1]))

        if status in [1, 2]:
            CURRENT_X += directions[dir_id][0]
            CURRENT_Y += directions[dir_id][1]
            path.insert(0, (CURRENT_X, CURRENT_Y))
            if status == 2: 
                found_oxygen = True
                oxygen_location = (CURRENT_X, CURRENT_Y)
    
    #Run BFS algo to find the shortest path
    pos_results[(0, 0)] = 1
    to_visit = []
    to_visit.append(((0, 0), 0))
    visited = set()

    while True:
        (node, dist) = to_visit.pop(0)
        visited.add(node)
        if pos_results[node] == 2:
            print("Moves to Oxygen:", dist)
            break

        for dir in directions.values():
            new_node = (node[0] + dir[0], node[1] + dir[1])
            if new_node in pos_results and pos_results[new_node] in [1, 2] and new_node not in visited:
                to_visit.append((new_node, dist + 1))

   #Part 2
    to_visit = []
    to_visit.append((oxygen_location, 0))
    visited = set()

    while to_visit:
        (node, dist) = to_visit.pop(0)
        visited.add(node)
        
        for dir in directions.values():
            new_node = (node[0] + dir[0], node[1] + dir[1])
            if new_node in pos_results and pos_results[new_node] in [1, 2] and new_node not in visited:
                to_visit.append((new_node, dist + 1))

    print("Part 2: ", dist)
