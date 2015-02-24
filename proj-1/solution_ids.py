import copy

# TODO: use hashing to prevent revisited nodes

def DLS_work(pegs, cur_board, target, boundary, limit, depth, num_no):
    over_limit = False

    if len(pegs) == 1 and pegs[0] == target: # Goal arrived
        return (True, num_no)
    if depth == limit: # depth limit reached
        return (-1, num_no)

    # expand
    num_no += 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # four directions
    in_board = lambda pos: pos[0] >= 0 and pos[0] < len(boundary) and pos[1] >= 0 and pos[1] < len(boundary[0]) and boundary[pos[0]][pos[1]] != -1 # peg position legality checking
    move = lambda x, y: (x[0]+y[0], x[1]+y[1]) # peg move function
    for peg in pegs:
        for d in directions:
            next_peg = move(peg, d)
            if in_board(next_peg) and cur_board[next_peg[0]][next_peg[1]] == 1: 
                # there's a peg in the next position
                jump_grid = move(next_peg, d)
                if in_board(jump_grid) and cur_board[jump_grid[0]][jump_grid[1]] == 0:
                    # there's an empty grid in the next to next
                    cur_move = (peg, jump_grid)
                    next_board = copy.deepcopy(cur_board)
                    next_board[peg[0]][peg[1]] = 0
                    next_board[next_peg[0]][next_peg[1]] = 0
                    next_board[jump_grid[0]][jump_grid[1]] = 1
                    new_pegs = copy.deepcopy(pegs)
                    new_pegs.remove(peg)
                    new_pegs.remove(next_peg)
                    new_pegs.append(jump_grid)
                    result = DLS_work(new_pegs, next_board, target, boundary, limit, depth+1, num_no)
                    num_no = result[1]
                    result = result[0]
                    if result == -1:
                        over_limit = True
                    elif result != False:
                        if result == True:
                            return ([cur_move], num_no)
                        else:
                            result.append(cur_move)
                            return (result, num_no)

    if over_limit == True:
        return (-1, num_no)
    else:
        return (False, num_no)

def DLS(board, limit, num_no):
    '''
    depth limited search
    '''
    print "Current Depth Limit: {0}".format(limit)
    print ''
    pegs = []
    boundary = copy.deepcopy(board)

    for idx, row in enumerate(board): # find possible pegs, also which need to be removed
        for jdx, grid in enumerate(row):
            if grid == 1:
                pegs.append((idx, jdx))

    transform = {}
    transform[1] = 0
    transform[0] = 0
    transform[-1] = -1

    boundary = map(lambda x: map(lambda y: transform[y], x), boundary)
    # print 'Boundary of Board >>>>'
    # for i in boundary:
    #     print i
    # print ''

    # print 'Original Pegs >>>>'
    # for i in pegs:
    #     print i
    # print ''

    tar_peg = (len(board)/2, len(board[0])/2)
    (result, num_no) = DLS_work(pegs, board, tar_peg, boundary, limit, 0, num_no)

    if result == -1:
        print "Depth Limit {0} reached".format(limit)
        print ''
        return (result, num_no)
    elif result == False:
        print 'DLS didn\'t find any solutions'
        print ''
        return (False, num_no)
    else:
        return (result, num_no)

def IDS(board):
    '''
    Solution using Iterative Deepening Search
    '''
    print 'IDS >>>>'
    print ''

    limit = 0
    max_limit = 0
    for i in board:
        for j in i:
            if j == 1:
                max_limit += 1


    num_nodes = 0

    while True:
        (result, num_nodes) = DLS(board, limit, num_nodes)

        if result == False:
            return (None, num_nodes)
        elif result != -1:
            return (result, num_nodes)

        limit += 1
        if limit > max_limit: # in case of infinite loop, but actually no such case
            print "Max Depth Limit {0} reached, algorithm to be stopped".format(max_limit)
            break

    return (None, num_nodes)
