#!/usr/bin/python

import sys, os
import copy
from solution_ids import IDS
from solution_astar import *

BOARD_ROW = 7
BOARD_COL = 7

mapping = {} # data mapping from string to board status
mapping['-'] = -1 # for unusable grid
mapping['O'] = 0 # for empty grid
mapping['X'] = 1 # for peg grid
back_mapping = {}
back_mapping[-1] = '-'
back_mapping[0] = 'O'
back_mapping[1] = 'X'

original_board = [] # hold the input string arrays
board = [] # supposed to be 7 * 7 array

if __name__ == '__main__':
    # print sys.argv
    try:
        with open(sys.argv[1]) as f:
            for line in f:
                original_board.append(line.strip())
                board.append(map(lambda x: mapping[x], list(line.strip())))
    except Exception as e:
        if e.__class__ == IndexError:
            raise Exception('''command should be "python solution.py <data_file> <strategy>"
            You Should Specify a data/input file''')
        else:
            raise e

    print ''
    print 'Board Information >>>>'

    for i in original_board:
        print i
    print ''

    if len(board) != BOARD_ROW:
        raise Exception("[ERROR] Board Row != {0}".format(BOARD_ROW))
    print "Row: {0}".format(len(board))
    if len(board[0]) != BOARD_COL:
        raise Exception("[ERROR] Board Column != {0}".format(BOARD_COL))
    print "Column: {0}".format(len(board[0]))
    print ''

    print "Converted Board Status:"
    for i in board:
        print i
    print ''

    index_mapping_cnt = 0
    index_mapping = copy.deepcopy(board)
    for idx, row in enumerate(board):
        for jdx, grid in enumerate(row): # use for (x, y) to (mapping_id) tranformation
            if grid != -1:
                index_mapping[idx][jdx] = index_mapping_cnt
                index_mapping_cnt += 1

    print 'Index Mapping'
    for i in index_mapping:
        print i
    print ''

    try:
        result = None
        number_of_nodes = 0 # count number of expanded nodes

        if sys.argv[2] == '--IDS':
            (result, number_of_nodes) = IDS(board)
        elif sys.argv[2] == '--ASTAR':
            (result, number_of_nodes) = ASTAR(board)
        
        print "Number of Expanded Nodes: {0}".format(number_of_nodes)
        print ''

        if result != None:
            result.reverse()
            show_result = map(lambda x: (index_mapping[x[0][0]][x[0][1]], index_mapping[x[1][0]][x[1][1]]), result)

            print 'Solution Found >>>>'
            # print result
            print show_result
            print ''

            print 'Solution moves >>>>'
            print ''

            move_cnt = 0
            print move_cnt
            move_board = copy.deepcopy(board)
            for i in original_board: print i
            print ''

            for i in result:
                move_cnt += 1
                print move_cnt
                from_peg = i[0]
                to_grid = i[1]
                next_peg = ((i[0][0]+i[1][0])/2, (i[0][1]+i[1][1])/2)
                # print from_peg
                # print next_peg
                # print to_grid
                move_board[from_peg[0]][from_peg[1]] = 0
                move_board[next_peg[0]][next_peg[1]] = 0
                move_board[to_grid[0]][to_grid[1]] = 1
                draw_board = map(lambda x: ''.join(map(lambda y: back_mapping[y], x)), move_board)
                for j in draw_board:
                    print j
                print ''

    except Exception as e:
        # print dir(e)
        # if e.__class__ == NameError:
        #     raise Exception('ASTAR() or IDS() method hasn\'t been implemented')
        if e.__class__ == IndexError:
            raise Exception('''command should be "python solution.py <data_file> <strategy>"
            You Should Choose Strategy from "--IDS" or "--ASTAR"''')
        else:
            raise e
