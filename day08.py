LAYER_WIDTH = 25
LAYER_HEIGHT = 6

if __name__ == '__main__':
    with open('data/day08.txt') as f:
        inputs = f.readline().strip()

    #inputs = '123456789012'
    
    #Build Empty Grid
    grid = [[0 for i in range(LAYER_HEIGHT*LAYER_WIDTH)] for j in range(len(inputs)//(LAYER_WIDTH*LAYER_HEIGHT))]
    
    #Populate Layer
    for idx, val in enumerate(inputs):
        grid[idx//(LAYER_HEIGHT*LAYER_WIDTH)][idx%(LAYER_WIDTH*LAYER_HEIGHT)] = int(val)
    
    """
    PART 1
    """
    zeros = [i.count(0) for i in grid]
    min_idx = zeros.index(min(zeros))
    print("PART 1:", grid[min_idx].count(1)*grid[min_idx].count(2))

    """
    PART 2
    """
    final = grid[0]
    comp = 1
    outer_layer = lambda x, y: x if x == 0 or x==1 else y
    while(max(final) == 2):
        final = [outer_layer(l1, l2) for l1, l2 in zip(final, grid[comp])]
        comp += 1

    #Display Message
    for i in range(LAYER_HEIGHT):
        print(final[i*LAYER_WIDTH:((i+1)*LAYER_WIDTH)])





    