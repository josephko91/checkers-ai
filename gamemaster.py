import os 
from utility import write_to_output, print_board, color_is_black, board_to_list, print_results
from board import Board
import time
from algorithm import minimax, minimax_alpha_beta, minimax_alpha_beta_final, minimax_alpha_beta_rand
from math import sqrt, floor

start = time.time()
# parse input file
with open("input.txt", "r") as input_file:
    game_mode = input_file.readline().rstrip() # 1st line: game mode
    color = input_file.readline().rstrip() # 2nd line: player color
    time_left = float(input_file.readline().rstrip()) # 3rd line: remaining time
    board_list = []
    for i in range(8): # next 8 lines: 2-d list representing the board
        board_list.append(list(input_file.readline().rstrip()))

# create initial board object
is_black = color_is_black(color)
start = time.time()
board = Board(board_list, is_black)
end = time.time()
print("time to make board object =", end - start)

# write mean runtimes to calibrate.txt
with open('test.txt', 'w') as output:
    
    # print description of game
    print("d_b = 4; d_w  = 4; simple heuristic for both b/w", file = output)
    #print("v3 changes: changed king weight from 30 to 20, added delta weight to small opp piece case", file = output)
    # play 100 games and store in game_results_1.txt
    black_wins = 0
    white_wins = 0
    timeouts = 0
    for i in range(10):
        start = time.time()
        # parse input file
        with open("input.txt", "r") as input_file:
            game_mode = input_file.readline().rstrip() # 1st line: game mode
            color = input_file.readline().rstrip() # 2nd line: player color
            time_left = float(input_file.readline().rstrip()) # 3rd line: remaining time
            board_list = []
            for i in range(8): # next 8 lines: 2-d list representing the board
                board_list.append(list(input_file.readline().rstrip()))

        # create initial board object
        is_black = color_is_black(color)
        start = time.time()
        board = Board(board_list, is_black)
        end = time.time()
        print("time to make board object =", end - start)

        max_iterations = 100
        iteration_count = 1
        total_time_black = 0
        total_time_white = 0
        # loop until someone wins or maximum iterations exceeded
        while True:
            start = time.time()
            minimax_alpha_beta_rand.count = 0
            minimax_alpha_beta_final.count = 0
            move_count = floor(iteration_count/2)
            if board.active_player: # black's turn
                # if iteration_count > 50:
                #     if move_count % 2 == 0:
                #         value, result, new_board = minimax_alpha_beta(board, board.active_player, 1, float("-inf"), float("inf"), True, (), board)
                #     # elif move_count % 9 == 0:
                #     #     value, result, new_board = minimax_alpha_beta(board, 8, float("-inf"), float("inf"), True)
                #     else:
                #        value, result, new_board = minimax_alpha_beta(board, board.active_player, 6, float("-inf"), float("inf"), True, (), board) 

                if move_count%2 == 0:
                    value, result, new_board = minimax_alpha_beta_final(board, board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)
                else:
                    value, result, new_board = minimax_alpha_beta_final(board, board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)

                # if move_count < 5: 
                #     value, result, new_board = minimax_alpha_beta(board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)
                # elif board.num_pieces_black < 4:
                #     if move_count%2 == 0:
                #         value, result, new_board = minimax_alpha_beta(board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)
                #     else:
                #         value, result, new_board = minimax_alpha_beta(board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)
                # else:
                #     if move_count%2 == 0:
                #         value, result, new_board = minimax_alpha_beta(board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)
                #     else:
                #         value, result, new_board = minimax_alpha_beta(board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)
            else: # white's turn
                # value, result, new_board = minimax_alpha_beta(board, board.active_player, 4, 4, float("-inf"), float("inf"), True, (), board)

                if move_count%2 == 0:
                    value, result, new_board = minimax_alpha_beta_rand(board, board, board.active_player, 2, 2, float("-inf"), float("inf"), True, (), board)
                else:
                    value, result, new_board = minimax_alpha_beta_rand(board, board, board.active_player, 2, 2, float("-inf"), float("inf"), True, (), board)

            end = time.time()
            runtime = end - start

            # if we run into a blocked board with lots of pieces left (i.e. it wasn't caught in game_over method): 
            if result == None: 
                print("total time black =", total_time_black)
                print("total time white =", total_time_white)
                if board.num_pieces_black == 0:
                    white_wins += 1
                elif board.num_pieces_white == 0:
                    black_wins += 1
                else: 
                    timeouts += 1
                break
            # set up new board 
            board = new_board
            # create new board_list (for printing later)
            board_list = board_to_list(board)
            # print result to game_output.txt
            print_results(board, result, board_list, iteration_count, runtime)
            # accumulate total runtime
            if board.active_player: # black's total time
                total_time_black  += runtime
            else: # white's total time
                total_time_white += runtime
            # switch player
            board.active_player = not board.active_player
            # break loop if someone won or exceeded max iterations
            if board.game_over() or iteration_count >= max_iterations:
                print("total time black =", total_time_black)
                print("total time white =", total_time_white)
                if board.num_pieces_black == 0:
                    white_wins += 1
                elif board.num_pieces_white == 0:
                    black_wins += 1
                else: 
                    timeouts += 1
                break
            iteration_count += 1
    # print final results to file
    print("black wins =", black_wins, file = output)
    print("white wins =", white_wins, file = output)
    print("timeouts =", timeouts, file = output)

# def print_results(board, result, board_list, iteration_count, runtime):
#     if board.active_player == True:
#         player = "black"
#     else:
#         player = "white"
#     print("iteration:", iteration_count)
#     print("runtime:", runtime)
#     print("player:", player)
#     print("move:", result)
#     for row in board_list:
#         print(row)