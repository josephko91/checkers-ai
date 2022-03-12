# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 2
# Checkers AI
# Author: Joseph Ko
# This is the main driver.
# -------------------------------------------------------
import os 
from play import play_single, play_game
from utility import write_to_output, print_board, color_is_black
from board import Board
import time

start = time.time()
# parse input file
with open("input.txt", "r") as input_file:
    game_mode = input_file.readline().rstrip() # 1st line: game mode
    color = input_file.readline().rstrip() # 2nd line: player color
    time_left = float(input_file.readline().rstrip()) # 3rd line: remaining time
    board_list = []
    for i in range(8): # next 8 lines: 2-d list representing the board
        board_list.append(list(input_file.readline().rstrip()))

# # read calibrate.txt
# with open("calibrate.txt", "r") as calibrate_file:
#     calibration_runtimes = [float(number) for number in calibrate_file.readline().split(",")]

# read playdata.txt
if not os.path.isfile("playdata.txt"): # if it's the first turn, there is no file that exists yet 
    original_total_time = time_left
    turn_count = 1 
    move_count_no_change = 1  
else:
    with open("playdata.txt", "r") as play_data:
        original_total_time = float(play_data.readline().rstrip()) # line 1: original total time
        turn_count = int(play_data.readline().rstrip()) # line 2: turn count
        move_count_no_change = int(play_data.readline().rstrip()) # line 3: number of last n moves with no changes
#end = time.time()
#print("time to read input data =", end - start)

# create board object
is_black = color_is_black(color)
start = time.time()
board = Board(board_list, is_black)
#end = time.time()
#print("time to make board object =", end - start)

# test prints
print('game mode = ', game_mode)
print('color = ', color)
print('time left = ', time_left)
print('type(time_left) = ', type(time_left))
print('============= BOARD IN ==============')
print_board(board_list)

#start = time.time()
# run in either single or game mode
if game_mode == "SINGLE": # single mode
    result = play_single(board) # result in the form of a 2-d list
else: # game mode
    result = play_game(board, original_total_time, time_left, turn_count, move_count_no_change)
#end = time.time()
#print("time to run single move =", end - start)

#start = time.time()
# write result to output file
with open('output.txt', 'w') as output:
    write_to_output(result, output)
end = time.time()
print("total time =", end - start)

