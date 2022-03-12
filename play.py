# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 2
# Checkers AI
# Author: Joseph Ko
# This module controls the flow of game play
# -------------------------------------------------------
from algorithm import minimax, minimax_alpha_beta, minimax_alpha_beta_final
from board import Board
import random
import time
from utility import print_board, board_to_list

def play_single(board):
    """ 
    plays a single valid move using all the remaining time 
    input: board (list), color (str)
    output: result (list)
    """
    # Note: any valid move accepted for single play mode
    depth = 2 # will always be << 1 second
    minimax_alpha_beta.count = 0
    minimax_alpha_beta_final.count = 0
    minimax.count = 0
    start = time.time()
    #result = minimax(board, depth, True)
    result = minimax_alpha_beta_final(board, board, board.active_player, depth, depth, float('-inf'), float('inf'), True, (), board)[1]
    end = time.time()
    #print("runtime minimax = ", end-start)
    print("runtime minimax_alpha_beta = ", end-start)
    print("depth =", depth)
    #print("# of recursive calls: ", minimax.count)
    print("# of recursive calls: ", minimax_alpha_beta_final.count)
    print("results:", result)
    return result

def play_game(board, original_total_time, time_left, turn_count, move_count_no_change):
    """ 
    plays the best move using a portion of remaining time 
    input: board (list), time_left (float), turn_count (int)
    output: result (tuple) -> e.g. ("E", (5, 2), (4, 3))
    """
    num_pieces_board_in = board.num_pieces_black + board.num_pieces_white
    minimax_alpha_beta_final.count = 0

    # ========================== If less than 10% of original time remains ========================== #
    if time_left < 0.1*original_total_time:
        result = minimax_alpha_beta_final(board, board, board.active_player, 4, 4, float('-inf'), float('inf'), True, (), board)
    # ====================================================================== #
    else: 
        # ========================== HARD-CODED FIRST MOVES ========================== #
        if turn_count == 1 and board.active_player: # hard-coded first move if BLACK
            result = [None, ("E", (2, 5), (3, 4)), None] # black: f6 -> e5
        elif turn_count == 1 and not board.active_player: # hard-coded counter moves if WHITE and first turn
            if (3, 4) in board.positions_black and (2, 5) in board.positions_empty: # black: f6 -> e5, white: c3 -> b4
                result = [None, ("E", (5, 2), (4, 1)), None]
            elif (3, 2) in board.positions_black and (2, 1) in board.positions_empty: # black: b6 -> c5, white: c3 -> d4
                result = [None, ("E", (5, 2), (4, 3)), None]
            elif (3, 6) in board.positions_black and (2, 5) in board.positions_empty: # black: f6 -> g5, white: e3 -> d4
                result = [None, ("E", (5, 4), (4, 3)), None]
            elif (3, 4) in board.positions_black and (2, 3) in board.positions_empty: # black: d6 -> e5, white: a3 -> b4
                result = [None, ("E", (5, 0), (4, 1)), None]
            elif (3, 2) in board.positions_black and (2, 3) in board.positions_empty: # black: d6 -> c5, white: g3 -> f4
                result = [None, ("E", (5, 6), (4, 5)), None]
            elif (3, 6) in board.positions_black and (2, 7) in board.positions_empty: # black: h6 -> g5, white: g3 -> h4
                result = [None, ("E", (5, 6), (4, 7)), None]
            elif (3, 0) in board.positions_black and (2, 1) in board.positions_empty: # black: b6 -> a5, white: c3 -> d4
                result = [None, ("E", (5, 2), (4, 3)), None]
            else: # for safety 
                result = minimax_alpha_beta_final(board, board, board.active_player, 2, 2, float('-inf'), float('inf'), True, (), board)
        # ====================================================================== #

        # ========================== Ramp up depth ========================== #
        elif turn_count < 5:
            result = minimax_alpha_beta_final(board, board, board.active_player, 2, 2, float('-inf'), float('inf'), True, (), board)
        # ====================================================================== #

        else: # main chunk of looping
            result = minimax_alpha_beta_final(board, board, board.active_player, 6, 6, float('-inf'), float('inf'), True, (), board)
    
    # write info to playdata.txt
    if turn_count == 1:
        move_count_no_change += 1
    else:
        board_out = result[2]
        num_pieces_board_out = board_out.num_pieces_black + board_out.num_pieces_white

        ### TESTING: print board out ###
        board_out_list = board_to_list(board_out)
        print("================ BOARD OUT ================")
        print_board(board_out_list)

        if num_pieces_board_in == num_pieces_board_out:
            move_count_no_change += 1
        else:
            move_count_no_change = 0
    turn_count += 1 # increment turn count
    with open('playdata.txt', 'w') as playdata:
        print(original_total_time, file = playdata) # line 1
        print(turn_count, file = playdata) # line 2
        print(move_count_no_change, file = playdata) # line 3 

    return result[1] # return only the move in tuple form