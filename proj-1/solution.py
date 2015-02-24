#!/usr/bin/python

import sys, os
import copy
from solution_ids import IDS
from solution_astar import *

from guppy import hpy

BOARD_ROW = 7
BOARD_COL = 7

board = [] # supposed to be 7 * 7 array

if __name__ == '__main__':
    # print sys.argv
    if len(sys.argv) < 2: 
        raise Exception('''command should be "python solution.py <data_file> <strategy> {--option=\'--memory_profile\'}"
        You Should Specify a file name''')

    if len(sys.argv) < 3: 
        raise Exception('''command should be "python solution.py <data_file> <strategy> {--option=\'--memory_profile\'}"
        You Should Choose Strategy from "--IDS" or "--ASTAR"''')

    try:
        with open(sys.argv[1]) as f:
            for line in f:
                board.append(list(line.strip()))
    except Exception as e:
        if e.__class__ == IOError:
            raise Exception('''command should be "python solution.py <data_file> <strategy> {--option=\'--memory_profile\'}"
            File does not exist! You Should Specify a valid data/input file''')
        else:
            raise e

    profile_flag = False
    if len(sys.argv) > 3 and sys.argv[3] == '--memory_profile':
        profile_flag = True

    print ''
    print 'Board Information >>>>'

    for i in board:
        print ''.join(i)
    print ''

    if len(board) != BOARD_ROW:
        raise Exception("[ERROR] Board Row != {0}".format(BOARD_ROW))
    print "Row: {0}".format(len(board))
    if len(board[0]) != BOARD_COL:
        raise Exception("[ERROR] Board Column != {0}".format(BOARD_COL))
    print "Column: {0}".format(len(board[0]))
    print ''

    index_mapping_cnt = 0
    index_mapping = copy.deepcopy(board)
    for idx, row in enumerate(board):
        for jdx, grid in enumerate(row): # use for (x, y) to (mapping_id) tranformation
            if grid != '-':
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
            (result, number_of_nodes, memory_profiled) = IDS(board, profile_flag)
        elif sys.argv[2] == '--ASTAR':
            (result, number_of_nodes, memory_profiled) = ASTAR(board, profile_flag)
        
        print "Number of Expanded Nodes: {0}".format(number_of_nodes)
        print ''
        if profile_flag == True:
            print "Peak Memory During Search Procedure: {0:f} KiB".format(memory_profiled/1024.)
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
            for i in board:
                print ''.join(i)
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
                move_board[from_peg[0]][from_peg[1]] = 'O'
                move_board[next_peg[0]][next_peg[1]] = 'O'
                move_board[to_grid[0]][to_grid[1]] = 'X'
                for j in move_board:
                    print ''.join(j)
                print ''

    except Exception as e:
        # print dir(e)
        # if e.__class__ == NameError:
        #     raise Exception('ASTAR() or IDS() method hasn\'t been implemented')
        raise e
