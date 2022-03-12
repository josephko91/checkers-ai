# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 2
# Checkers AI
# Author: Joseph Ko
# This holds the various gameplaying algorithms
# -------------------------------------------------------
from board import Board
import copy
import time
import random

def minimax(board, depth, max_player): 
    """
    The basic minimax algorithm with no modifications
    input: board (Board), depth (int), max_player (Bool)
    output: tuple of best move sequence e.g. ('E', (1,2), (2,3))
    """
    minimax.count += 1
    # If you reached a terminal node or game is over
    if depth == 0 or board.game_over():
        return board.evaluate(max_player), ()
    if max_player: # maximizing player
        value = float('-inf')
        for move, child_board in board.possible_moves().items():
            child_board = copy.deepcopy(child_board)
            minimax_value = minimax(child_board, depth - 1, False)[0]
            if minimax_value > value: 
                value = minimax_value
                best_move = move
        return value, best_move
    else: # minimizing player
        value = float('inf')
        board.active_player = not board.active_player # switch the player
        for move, child_board in board.possible_moves().items():
            child_board = copy.deepcopy(child_board)
            child_board.active_player = not child_board.active_player
            value = min(value, minimax(child_board, depth - 1, True)[0])
        return value, ()

# def minimax_alpha_beta(board, depth, alpha, beta, max_player): 
#     """
#     Minimax with alpha-beta pruning
#     input: board (Board), depth (int), max_player (Bool)
#     output: tuple of best move sequence e.g. ('E', (1,2), (2,3))
#     """
#     minimax_alpha_beta.count += 1
#     # If you reached a terminal node or game is over
#     if depth == 0 or board.game_over():
#         return board.evaluate(max_player), ()
#     if max_player: # maximizing player
#         value = float('-inf')
#         for move, child_board in board.possible_moves().items():
#             child_board = copy.deepcopy(child_board)
#             child_board.active_player = not child_board.active_player
#             minimax_value = minimax_alpha_beta(child_board, depth - 1, alpha, beta, False)[0]
#             if minimax_value > value: 
#                 value = minimax_value
#                 best_move = move
#             # in case of equal value, update based on random binary generator
#             if minimax_value == value:
#                 random_num = random.randint(1, 101)
#                 if random_num > 50:
#                 #if bool(random.getrandbits(1)): # random T or F
#                     best_move = move # update best move with random probability
#             alpha = max(alpha, value)
#             if alpha > beta:
#                 break
#             elif alpha == beta:
#                 random_num = random.randint(1, 101)
#                 if random_num > 50:
#                 #if bool(random.getrandbits(1)): # random T or F
#                     break
#         return value, best_move, child_board
#     else: # minimizing player
#         value = float('inf')
#         #board_copy = copy.deepcopy(board)
#         #board.active_player = not board.active_player # switch the player
#         for move, child_board in board.possible_moves().items():
#             child_board = copy.deepcopy(child_board)
#             child_board.active_player = not child_board.active_player
#             value = min(value, minimax_alpha_beta(child_board, depth - 1, alpha, beta, True)[0])
#             beta = min(beta, value)
#             if beta < alpha:
#                 break
#             elif beta == alpha: 
#                 random_num = random.randint(1, 101)
#                 if random_num > 50:
#                 #if bool(random.getrandbits(1)): # random T or F
#                     break
#         return value, ()

def minimax_alpha_beta(board, color, root, depth, alpha, beta, max_player, moves_list, board_list): 
    """
    Minimax with alpha-beta pruning
    input: board (Board), depth (int), max_player (Bool)
    output: tuple of best move sequence e.g. ('E', (1,2), (2,3))
    """
    minimax_alpha_beta.count += 1
    # If you reached a terminal node or game is over
    if depth == 0 or board.game_over():
        return board.evaluate(color), ()
    if max_player: # maximizing player
        value = float('-inf')
        for move, max_child in board.possible_moves().items():
            max_child_copy = copy.deepcopy(max_child)
            max_child_copy.active_player = not max_child_copy.active_player
            minimax_value = minimax_alpha_beta(max_child_copy, color, root, depth - 1, alpha, beta, False, moves_list, board_list)[0]
            if minimax_value >= value: 
                value = minimax_value
                if depth == root: 
                    moves_list.append(move)
                    board_list.append(max_child)
            
            # # TESTING 
            # if move[0] == "J": # JUMP heuristic 
            #     value += 10*(len(move)-2)

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        # pick best move
        if depth == root:
            if len(moves_list) == 0:
                return value, None, None
            else:
                random_num = random.randint(0,len(moves_list)-1)
                #random_num = 0
                best_move = moves_list[random_num]
                best_board = board_list[random_num]
                return value, best_move, best_board
        else:
            return value, ()
    else: # minimizing player
        value = float('inf')
        #board_copy = copy.deepcopy(board)
        #board.active_player = not board.active_player # switch the player
        for move, min_child in board.possible_moves().items():
            min_child_copy = copy.deepcopy(min_child)
            min_child_copy.active_player = not min_child_copy.active_player
            value = min(value, minimax_alpha_beta(min_child_copy, color, root, depth - 1, alpha, beta, True, moves_list, board_list)[0])
            beta = min(beta, value)
            
            # # TESTING 
            # if move[0] == "J": # JUMP heuristic 
            #     value -= 5*(len(move)-2)

            if beta <= alpha:
                break
        return value, ()



def minimax_alpha_beta_final(static_board, board, color, root, depth, alpha, beta, max_player, best_move, best_board): 
    """
    Minimax with alpha-beta pruning
    input: board (Board), depth (int), max_player (Bool)
    output: tuple of best move sequence e.g. ('E', (1,2), (2,3))
    """
    minimax_alpha_beta_final.count += 1
    # If you reached a terminal node or game is over
    if depth == 0 or board.game_over():
        return board.evaluate(color, static_board), None, None
    # maximizing player
    if max_player: 
        value = float('-inf')
        moves_dict = board.possible_moves()
        for move, max_child in moves_dict.items():
            max_child_copy = copy.deepcopy(max_child)
            max_child_copy.active_player = not max_child_copy.active_player
            minimax_value = minimax_alpha_beta_final(static_board, max_child_copy, color, root, depth - 1, alpha, beta, False, best_move, best_board)[0]
            if minimax_value > value: 
                value = minimax_value
                best_move = move
                best_board = max_child
            if depth == root and minimax_value == value: 
                if bool(random.getrandbits(1)): # random T/F
                    value = minimax_value
                    best_move = move
                    best_board = max_child
            alpha = max(alpha, value)
            if alpha >= beta:
                break
                #return float('inf'), None, None 
        return value, best_move, best_board
    # minimizing player
    else: 
        value = float('inf')
        moves_dict = board.possible_moves()
        for move, min_child in moves_dict.items():
            min_child_copy = copy.deepcopy(min_child)
            min_child_copy.active_player = not min_child_copy.active_player
            value = min(value, minimax_alpha_beta_final(static_board, min_child_copy, color, root, depth - 1, alpha, beta, True, best_move, best_board)[0])
            beta = min(beta, value)
            if beta <= alpha:
                break
                #return float('-inf'), None, None
        return value, None, None


def minimax_alpha_beta_rand(static_board, board, color, root, depth, alpha, beta, max_player, best_move, best_board): 
    """
    Minimax with alpha-beta pruning
    input: board (Board), depth (int), max_player (Bool)
    output: tuple of best move sequence e.g. ('E', (1,2), (2,3))
    """
    minimax_alpha_beta_rand.count += 1
    # If you reached a terminal node or game is over
    if depth == 0 or board.game_over():
        return board.evaluate(color, static_board), None, None
    # maximizing player
    if max_player: 
        value = float('-inf')
        for move, max_child in board.possible_moves().items():
            max_child_copy = copy.deepcopy(max_child)
            max_child_copy.active_player = not max_child_copy.active_player
            minimax_value = minimax_alpha_beta_rand(static_board, max_child_copy, color, root, depth - 1, alpha, beta, False, best_move, best_board)[0]

            if minimax_value > value: 
                value = minimax_value
                best_move = move
                best_board = max_child
            if depth == root and minimax_value == value: 
                if bool(random.getrandbits(1)): # random T/F
                    value = minimax_value
                    best_move = move
                    best_board = max_child
            
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value, best_move, best_board
    # minimizing player
    else: 
        value = float('inf')
        #board_copy = copy.deepcopy(board)
        #board.active_player = not board.active_player # switch the player
        for move, min_child in board.possible_moves().items():
            min_child_copy = copy.deepcopy(min_child)
            min_child_copy.active_player = not min_child_copy.active_player
            value = min(value, minimax_alpha_beta_rand(static_board, min_child_copy, color, root, depth - 1, alpha, beta, True, best_move, best_board)[0])

            beta = min(beta, value)

            if beta <= alpha:
                break
        
        return value, None, None

# ================ UNFINISHED AND UNUSED CODE ====================== #
# def iterative_deepening(board, max_player, time_limit): 
#     """
#     Minimax with alpha-beta pruning and iterative deepening
#     input: board (Board), depth (int), max_player (Bool)
#     output: tuple of best move sequence e.g. ('E', (1,2), (2,3))
#     """
#     minimax_alpha_beta.count = 0
#     start_time = time.time()
#     depth = 0
#     condition = True
#     result_matrix = []
#     hash_table = {}
#     while condition == True:
#         try:
#             result = minimax_alpha_beta(board, depth, float("-inf"), float("inf"), True, start_time, time_limit, hash_table)
#         except: 
#             break
#         depth += 1
#         result_matrix[depth] = result
#     return result_matrix[len(result_matrix)], minimax_alpha_beta.count, depth # return last available result

#     # define minimax_alpha_beta here
#     def minimax_alpha_beta(board, depth, alpha, beta, max_player, start_time, time_limit, hash_table): 
#         ### throw timeout exception ###
#         if (time_limit - (current_time - start_time)) < 0.01*time_limit or (current_time - start_time) > time_limit:
#             raise Exception("timeout!")
#         ### retrieve stored bounds from transposition table ###
#         if hash(board) in hash_table:

#         minimax_alpha_beta.count += 1 # keep count of all recursive function calls (i.e. # of nodes)
#         # If you reached a terminal node or game is over
#         if depth == 0 or board.game_over():
#             return board.evaluate(max_player), ()
#         if max_player: # maximizing player
#             value = float('-inf')
#             for move, child_board in board.possible_moves().items():
#                 child_board = copy.deepcopy(child_board)
#                 minimax_value = minimax_alpha_beta(child_board, depth - 1, alpha, beta, False, start_time, time_limit, hash_table)[0]
#                 if minimax_value > value: 
#                     value = minimax_value
#                     best_move = move
#                 alpha = max(alpha, value)
#                 if alpha >= beta:
#                     break
#             return value, best_move
#         else: # minimizing player
#             value = float('inf')
#             board.active_player = not board.active_player # switch the player
#             for move, child_board in board.possible_moves().items():
#                 child_board = copy.deepcopy(child_board)
#                 child_board.active_player = not child_board.active_player
#                 value = min(value, minimax_alpha_beta(child_board, depth - 1, alpha, beta, True, start_time, time_limit, hash_table)[0])
#                 beta = min(beta, value)
#                 if beta <= alpha:
#                     break
#             return value, ()
#         ### Store bounds in transposition table ###
#         # fail low result -> upper bound
#         if value <= alpha:
#             if hash(board) in hash_table:
#                 updated_entry = {"upper" = value}
#                 hash_table[hash(board)].update(updated_entry) # update upper bound
#             else: # create new entry
#                 hash_table[hash(board)] = {"upper" = value, "lower" = float("-inf")} 
#         # exact minimax value
#         if value > alpha and value < beta:
#             hash_table[hash(board)] = {"upper" = value, "lower" = value} # overwrite 
#         # fail high result -> lower bound
#         if value >= beta:
#             if hash(board) in hash_table:
#                 updated_entry = {"lower" = value}
#                 hash_table[hash(board)].update(updated_entry) # update upper bound
#             else: # create new entry
#                 hash_table[hash(board)] = {"upper" = float("inf"), "lower" = value} 