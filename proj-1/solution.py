import sys, os
from solution_ids import *

BOARD_ROW = 7
BOARD_COL = 7

mapping = {} # data mapping from string to board status
mapping['-'] = -1 # for unusable grid
mapping['O'] = 0 # for empty grid
mapping['X'] = 1 # for peg grid

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

    try:
        if sys.argv[2] == '--IDS':
            IDS()
        elif sys.argv[2] == '--ASTAR':
            ASTAR()
    except Exception as e:
        # print dir(e)
        if e.__class__ == NameError:
            raise Exception('ASTAR() or IDS() method hasn\'t been implemented')
        if e.__class__ == IndexError:
            raise Exception('''command should be "python solution.py <data_file> <strategy>"
            You Should Choose Strategy from "--IDS" or "--ASTAR"''')
