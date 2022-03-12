from board import Board
from algorithm import minimax_alpha_beta
import time
from statistics import mean
from math import sqrt, floor

board_list_start = [[".",  "b",  ".",  "b",  ".",  "b",  ".",  "b"],
        ["b",  ".",  "b",  ".",  "b",  ".",  "b",  "."],
        [".",  "b",  ".",  "b",  ".",  "b",  ".",  "b"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["w",  ".",  "w",  ".",  "w",  ".",  "w",  "."],
        [".",  "w",  ".",  "w",  ".",  "w",  ".",  "w"],
        ["w",  ".",  "w",  ".",  "w",  ".",  "w",  "."]]

board_list_middle = [[".",  "b",  ".",  ".",  ".",  ".",  ".",  "."],
        ["b",  ".",  "b",  ".",  "b",  ".",  "b",  "."],
        [".",  ".",  ".",  ".",  ".",  ".",  ".",  "b"],
        [".", ".", "w", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "b", ".", "w"],
        [".",  ".",  ".",  ".",  "b",  ".",  ".",  "."],
        [".",  "w",  ".",  "w",  ".",  "w",  ".",  "."],
        [".",  ".",  "w",  ".",  ".",  ".",  "w",  "."]]

board_list_end = [[".",  ".",  ".",  ".",  ".",  "W",  ".",  "."],
        [".",  ".",  ".",  ".",  ".",  ".",  "b",  "."],
        [".",  ".",  ".",  ".",  ".",  ".",  ".",  "b"],
        [".", "w", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "w"],
        [".",  "b",  ".",  ".",  ".",  ".",  ".",  "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "B", ".", "w", "."]]

start = time.time()
board_start = Board(board_list_start, True)
board_middle = Board(board_list_middle, True)
board_end = Board(board_list_end, True)
end = time.time()

# Measure algorithm runtime for start board 
start_runtimes = []
for depth in range(1, 10, 1): # run from depth 1-9
    start = time.time()
    minimax_alpha_beta.count = 0
    minimax_alpha_beta(board_start, depth, float("-Inf"), float("Inf"), True)
    end = time.time()
    start_runtimes.append(end-start)

# Measure algorithm runtime for middle board 
middle_runtimes = []
for depth in range(1, 10, 1): # run from depth 1-9
    start = time.time()
    minimax_alpha_beta.count = 0
    minimax_alpha_beta(board_middle, depth, float("-Inf"), float("Inf"), True)
    end = time.time()
    middle_runtimes.append(end-start)

# Measure algorithm runtime for end board 
end_runtimes = []
for depth in range(1, 10, 1): # run from depth 1-9
    start = time.time()
    minimax_alpha_beta.count = 0
    minimax_alpha_beta(board_middle, depth, float("-Inf"), float("Inf"), True)
    end = time.time()
    end_runtimes.append(end-start)    

mean_runtimes = []
# average cases into one array
for i in range(len(start_runtimes)):
    mean_value = mean([start_runtimes[i], middle_runtimes[i], end_runtimes[i]])
    mean_runtimes.append(mean_value)

# write mean runtimes to calibrate.txt
with open('calibrate.txt', 'w') as output:
    for i in range(len(mean_runtimes)):
        if i == len(mean_runtimes)-1:
            print(mean_runtimes[i], file = output, end = "")
        else:
            print(mean_runtimes[i], file = output, end = ",")