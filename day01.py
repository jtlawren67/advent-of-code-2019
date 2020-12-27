
def part1(num):
    return(num//3-2)

def part2(num):
    if(part1(num) <= 0):
        return(0)
    else:
        return(part1(num) + part2(part1(num)))

if __name__ == "__main__":
    with open("data/day01.txt") as f:
        l = f.readlines()
        p1 = sum([part1(int(line)) for line in l])
        p2 = sum([part2(int(line)) for line in l])
       

    print("Part 1=", p1)
    print("Part 2=", p2)

