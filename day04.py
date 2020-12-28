from collections import Counter

def part1(start, stop):
    vals = [i for i in range(start, stop+1) 
    if len(str(i)) == 6 and checkValid(i)
    ]

    return(vals)

def checkValid(num):
    double_digit = False
    all_increasing = True
    digits = list(str(num))
    for i in range(1, len(digits)):
        if(digits[i-1]==digits[i]):
             double_digit = True
        if(digits[i-1] > digits[i]):
            all_increasing = False
    
    return(all_increasing and double_digit)

def part2(num):
    instances = {n: ct for n, ct in Counter(list(str(num))).items() if ct == 2}
    return(len(instances) > 0)


if __name__ == "__main__":
    p1 = part1(284639, 748759)
    p2 = [x for x in p1 if part2(x)]
    print("PART 1 Answer:", len(p1))
    print("PART 2 Answer:", len(p2))
