import sys, os

BOARD_ROW = 7
BOARD_COL = 7

mapping = {} # data mapping from string to board status
mapping['-'] = -1
mapping['O'] = 0
mapping['X'] = 1

board = [] # supposed to be 7 * 7 array

for line in sys.stdin:
    board.append(map(lambda x: mapping[x], list(line.strip())))

print "Board Information >>>>"

if len(board) != BOARD_ROW:
    raise Exception("[ERROR] Board Row != {0}".format(BOARD_ROW))
print "Row: {0}".format(len(board))

if len(board[0]) != BOARD_COL:
    raise Exception("[ERROR] Board Column != {0}".format(BOARD_COL))
print "Column: {0}".format(len(board[0]))

for i in board:
    print i
