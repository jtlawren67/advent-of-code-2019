def run_phase(input, base_pattern):
    iter = 1
    output = []
    for digit in input:
        pos = 1
        new_base = [item for item in base_pattern for i in range(iter)]
        value = 0
        for digit in input:
            value += int(digit)*new_base[pos]
            pos = (pos + 1) % len(new_base)
        output.append(abs(value) % 10)
        iter+=1
    
    return output



if __name__ == '__main__':
    with(open('data/day16.txt')) as f:
         orig = [int(i) for i in f.readline().strip()]

    output = orig.copy()
    NUM_PHASES = 100
    output = [1, 1, 1, 1, 1, 1, 1, 1]

    base_pattern = [0, 1, 0, -1]

    for i in range(NUM_PHASES):
        output = run_phase(output, base_pattern)
        #print("PHASE",i,":", output)

    output = [str(i) for i in output]
    print("PART 1:", ''.join(output[:8]))

    ##PART 2
    output = orig*10000

    tmp = [str(i) for i in output]
    offset = int(''.join(tmp[:7]))

    for i in range(NUM_PHASES):
        for j in range(offset):
            output[j] = 0

        tmp = output[::-1]
        for k in range(len(tmp)//2):
            if(k>0): 
                tmp[k] = abs(tmp[k-1] + tmp[k])%10
        output = tmp[::-1]

    output = [str(i) for i in output]
    print("PART 2:", ''.join(output[offset:offset+8]))



