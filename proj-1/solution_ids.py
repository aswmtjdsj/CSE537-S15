import copy
from guppy import hpy

# TODO: use hashing to prevent revisited nodes

# @profile
def DLS_work(pegs, cur_board, target, limit, depth, v, flag):
    over_limit = False

    # profiling
    m_used = 0
    if flag == True:
        h = hpy()
        statistics = h.heap()
        m_used = statistics.size
    # print statistics.size

    num_no = 1

    if len(pegs) == 1 and pegs[0] == target: # Goal arrived
        return (True, num_no, v, m_used)
    if depth == limit: # depth limit reached
        return (-1, num_no, v, m_used)

    # expand
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # four directions
    in_board = lambda pos: pos[0] >= 0 and pos[0] < len(cur_board) and pos[1] >= 0 and pos[1] < len(cur_board[0]) and cur_board[pos[0]][pos[1]] != '-' # peg position legality checking
    move = lambda x, y: (x[0]+y[0], x[1]+y[1]) # peg move function
    for peg in pegs:
        for d in directions:
            next_peg = move(peg, d)
            if in_board(next_peg) and cur_board[next_peg[0]][next_peg[1]] == 'X': 
                # there's a peg in the next position
                jump_grid = move(next_peg, d)
                if in_board(jump_grid) and cur_board[jump_grid[0]][jump_grid[1]] == 'O':
                    # there's an empty grid in the next to next
                    cur_move = (peg, jump_grid)
                    next_board = copy.deepcopy(cur_board)
                    next_board[peg[0]][peg[1]] = 'O'
                    next_board[next_peg[0]][next_peg[1]] = 'O'
                    next_board[jump_grid[0]][jump_grid[1]] = 'X'
                    if ''.join(map(lambda x: ''.join(x), next_board)) not in v: # prevent re-visiting failed states
                        new_pegs = copy.deepcopy(pegs)
                        new_pegs.remove(peg)
                        new_pegs.remove(next_peg)
                        new_pegs.append(jump_grid)
                        result = DLS_work(new_pegs, next_board, target, limit, depth+1, v, flag)
                        num_no += result[1]
                        if flag:
                            m_used = max(m_used, result[3])
                        result = result[0]
                        if result == -1:
                            over_limit = True
                        elif result != False:
                            if result == True:
                                return ([cur_move], num_no, v, m_used)
                            else:
                                result.append(cur_move)
                                return (result, num_no, v, m_used)

    if over_limit == True:
        return (-1, num_no, v, m_used)
    else:
        # failed state, no expansion
        v.add(''.join(map(lambda x: ''.join(x), cur_board)))
        return (False, num_no, v, m_used)

# @profile
def DLS(board, limit, vh, flag):
    '''
    depth limited search
    '''
    print "Current Depth Limit: {0}".format(limit)
    print ''
    pegs = []
    boundary = copy.deepcopy(board)

    for idx, row in enumerate(board): # find possible pegs, also which need to be removed
        for jdx, grid in enumerate(row):
            if grid == 'X':
                pegs.append((idx, jdx))

    # print 'Original Pegs >>>>'
    # for i in pegs:
    #     print i
    # print ''

    tar_peg = (len(board)/2, len(board[0])/2)
    (result, num_no, vh, m_used) = DLS_work(pegs, board, tar_peg, limit, 0, vh, flag)

    if result == -1:
        print "Depth Limit {0} reached".format(limit)
        print ''
        return (result, num_no, vh, m_used)
    elif result == False:
        print 'DLS didn\'t find any solutions'
        print ''
        return (False, num_no, vh, m_used)
    else:
        return (result, num_no, vh, m_used)

# @profile
def IDS(board, flag):
    '''
    Solution using Iterative Deepening Search
    '''
    print 'IDS >>>>'
    print ''

    limit = 0
    max_limit = 0
    for i in board: # count max steps
        for j in i:
            if j == 'X':
                max_limit += 1

    max_limit -= 1
    print max_limit

    num_nodes = 0
    memory_used = 0

    visited_hash = set()

    while True:
        (result, once_nodes, visited_hash, once_mem_max) = DLS(board, limit, visited_hash, flag)
        print "Nodes Expanded in Current DLS: {0}".format(once_nodes)
        print ''
        print "Current Visited Status Set Size: {0}".format(len(visited_hash))
        print ''
        if flag == True:
            print "Peak Memory During Current DLS: {0:3f} KiB".format(once_mem_max/1024.)
            print ''
            memory_used = max(once_mem_max, memory_used)
        num_nodes += once_nodes

        if result == False:
            return (None, num_nodes, memory_used)
        elif result != -1:
            return (result, num_nodes, memory_used)

        limit += 1
        if limit > max_limit: # in case of infinite loop, but actually no such case
            print "Max Depth Limit {0} reached, algorithm to be stopped".format(max_limit)
            break

    return (None, num_nodes, memory_used)
