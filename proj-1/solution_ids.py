def DLS_work(pegs, target, boundary, limit, depth):
    over_limit = False

    if len(pegs) == 1 and pegs == target:
        return True

    if depth == limit:
        return -1 # due to the limit of depth

    # expand
    # TODO

def DLS(board, limit):
    pegs = []
    boundary = board[:]

    for idx, row in enumerate(board): # find possible pegs, also which need to be removed
        for jdx, grid in enumerate(row):
            if grid == 1:
                pegs.append((idx, jdx))

    transform = {}
    transform[1] = 0
    transform[0] = 0
    transform[-1] = -1
    boundary = map(lambda x: map(lambda y: transform[y], x), boundary)
    print 'Boundary of Board >>>>'
    for i in boundary:
        print i
    print ''

    print 'Original Pegs >>>>'
    for i in pegs:
        print i
    print ''

    mapping_cnt = 0
    mapping = board[:]
    for idx, row in enumerate(board):
        for jdx, grid in enumerate(row):
            if grid != -1:
                mapping[idx][jdx] = mapping_cnt
                mapping_cnt += 1

    print 'Mapping'
    for i in mapping:
        print i
    print ''

    tar_peg = (len(board)/2, len(board[0])/2)
    DLS_work(pegs, tar_peg, boundary, limit, 0)

    return True

def IDS(board):
    '''
    Solution using Iterative Deepening Search
    '''
    print 'IDS >>>>'
    print ''

    limit = 0
    while True:
        if DLS(board, limit):
            return True
        limit += 1
