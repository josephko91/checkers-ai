# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 2
# Checkers AI
# Author: Joseph Ko
# Board class and its methods
# -------------------------------------------------------
import copy
import itertools
from collections import deque
from utility import create_jumps_sequences, create_jumps_dict
from statistics import mean
from math import sqrt, floor, ceil
import random

class Board:
    def __init__(self, board_list, is_black):
        self.positions_black = {} # {(row, col):pawn_or_king}
        self.positions_white = {}
        self.positions_empty = set()
        self.num_pieces_black = 0
        self.num_pieces_white = 0
        self.num_kings_black = 0
        self.num_kings_white = 0
        self.nrows = len(board_list)
        self.ncols = len(board_list[0])
        self.active_player = is_black
        # iterate through board and fill out attributes
        for i in range(self.nrows):
            for j in range((i+1)%2, self.ncols + (i+1)%2, 2):
                if board_list[i][j] == ".": # empty square
                    self.positions_empty.add((i, j))
                elif board_list[i][j] == "b": # black pawn
                    self.positions_black[(i, j)] = "pawn"
                    self.num_pieces_black += 1
                elif board_list[i][j] == "B": # black king
                    self.positions_black[(i, j)] = "king"
                    self.num_kings_black += 1
                    self.num_pieces_black += 1
                elif board_list[i][j] == "w": # white pawn
                    self.positions_white[(i, j)] = "pawn" 
                    self.num_pieces_white += 1
                elif board_list[i][j] == "W": # white king
                    self.positions_white[(i, j)] = "king"
                    self.num_kings_white += 1
                    self.num_pieces_white += 1

# ============================== UNUSED CODE ============================== #
    # def __eq__(self, other):
    #     if len(self.positions_black) != len(other.positions_black) or len(self.positions_white) != len(other.positions_white):
    #         return False
    #     else:
    #         return self.positions_black == other.positions_black and self.positions_white == other.positions_white

    # def __hash__(self):
    #     hash_value = ""
    #     black_positions = self.positions_black.keys()
    #     sorted_black_positions = sorted(black_positions, key = lambda k: (k[0], k[1]))
    #     white_positions = self.positions_white.keys()
    #     sorted_white_positions = sorted(white_positions, key = lambda k: (k[0], k[1]))
    #     for key in sorted_black_positions:
    #         coord = str(key[0]) + str(key[1])
    #         if self.positions_black[key] == "pawn":
    #             letter = str(ord("b"))
    #         else:
    #             letter = str(ord("B"))
    #         hash_value = hash_value + coord + letter
    #     for key in sorted_white_positions:
    #         coord = str(key[0]) + str(key[1])
    #         if self.positions_white[key] == "pawn":
    #             letter = str(ord("w"))
    #         else:
    #             letter = str(ord("W"))
    #         hash_value = hash_value + coord + letter
    #     if self.active_player == True:
    #         color_switch = 1
    #     else:
    #         color_switch = 0
    #     hash_value = hash_value + str(color_switch)
    #     return int(hash_value)
# ==================================================================================== #

    def change_to_king(self, new_position):
        """
        Change pawn to a king
        """
        if self.active_player: # active player is BLACK
            self.positions_black[new_position] = "king"
            self.num_kings_black += 1

        else: # active player is WHITE
            self.positions_white[new_position] = "king"
            self.num_kings_white += 1

    def simple_move(self, old_position, new_position):
        """
        Move a piece from one coordinate to another
        """
        self.positions_empty.add(old_position) # add an empty space where old position was
        self.positions_empty.remove(new_position) # remove new position from empty

        if self.active_player: # active player is BLACK
            piece_type = self.positions_black[old_position]
            del self.positions_black[old_position] # remove old entry from dictionary
            self.positions_black[new_position] = piece_type # add new position to dictionary
            # if land on last row, change to kind
            if piece_type == "pawn" and new_position[0] == 7:
                self.change_to_king(new_position)

        else: # active player is WHITE
            piece_type = self.positions_white[old_position]
            del self.positions_white[old_position] # remove old entry from dictionary
            self.positions_white[new_position] = piece_type # add new position to dictionary
            # if land on last row, change to kind
            if piece_type == "pawn" and new_position[0] == 0:
                self.change_to_king(new_position)

    def jump_move(self, old_position, new_position):
        """
        Jump active piece and remove the jumped piece 
        """
        jumped_position = (int((old_position[0]+new_position[0])/2), int((old_position[1]+new_position[1])/2))
        self.positions_empty.add(old_position) # add an empty space where old position was
        self.positions_empty.add(jumped_position) # add an empty space where jumped piece was
        self.positions_empty.remove(new_position) # remove new position from empty

        if self.active_player: # active player is BLACK
            # exit if there is a failed jump
            if jumped_position not in self.positions_white:
                return "fail"
            piece_type = self.positions_black[old_position]
            del self.positions_black[old_position] # remove old entry from dictionary
            self.positions_black[new_position] = piece_type # add new position to dictionary
            if self.positions_white[jumped_position] == "king":
                self.num_pieces_white -= 1
                self.num_kings_white -= 1
            else:
                self.num_pieces_white -= 1
            del self.positions_white[jumped_position] # remove jumped opp piece
            # if land on last row, change to kind
            if piece_type == "pawn" and new_position[0] == 7:
                self.change_to_king(new_position)
        else: # active player is WHITE
            # exit if there is a failed jump
            if jumped_position not in self.positions_black:
                return "fail"
            piece_type = self.positions_white[old_position]
            del self.positions_white[old_position] # remove old entry from dictionary
            self.positions_white[new_position] = piece_type # add new position to dictionary
            if self.positions_black[jumped_position] == "king":
                self.num_pieces_black -= 1
                self.num_kings_black -= 1
            else:
                self.num_pieces_black -= 1
            del self.positions_black[jumped_position] # remove jumped opp piece
            # if land on last row, change to kind
            if piece_type == "pawn" and new_position[0] == 0:
                self.change_to_king(new_position)

    def evaluate(self, color, static_board): 
        """
        Evaluation heuristic function of the board
        - most recent moves were made by opposite of self.active_player
        """
        if color: # active player is BLACK

            # value = 0 # initialize
            # # if player has won 
            # if self.num_pieces_white == 0 and self.num_pieces_black > 0:
            #     return 1000000000
            # elif self.num_pieces_black == 0 and self.num_pieces_white > 0:
            #     return -1000000000
            # else: # if player has not won yet
            #     num_in_king_row = 0
            #     num_in_middle_center = 0
            #     num_in_middle_sides = 0
            #     # iterate through pieces on board
            #     n = 0
            #     sum_x = 0
            #     sum_y = 0 
            #     for position in self.positions_black:
            #         # calculations for mean
            #         n += 1
            #         sum_x += position[0]
            #         sum_y += position[1]
            #         # assign value to pieces
            #         if self.positions_black[position] == "pawn":
            #             value += 6000
            #         else:
            #             value += 9000
            #         # count number of pieces in king row (i.e. home row)
            #         if position[0] == 0:
            #             num_in_king_row += 1
            #         # count board positioning 
            #         if position[0] > 2 and position[0] < 5: # middle two rows
            #             if position[1] > 1 and position[1] < 6:
            #                 num_in_middle_center += 1
            #             else:
            #                 num_in_middle_sides += 1
            #     # calculate mean
            #     mean_x = sum_x/n
            #     mean_y = sum_y/n
            #     # calculate RMS
            #     running_sum_x = 0
            #     running_sum_y = 0
            #     for position in self.positions_black:
            #         running_sum_x += (position[0] - mean_x)**2
            #         running_sum_y += (position[1] - mean_y)**2
            #     rms = ((running_sum_x + running_sum_y)/n)**(1/2)
            #     if rms == 0:
            #         rms_value = 1
            #     else:
            #         rms_value = ceil(1/rms)
            #     # early to mid game
            #     if static_board.num_pieces_black > 10 and static_board.num_pieces_white > 10:
            #         value += (2*num_in_middle_center + num_in_middle_sides + num_in_king_row)*100 + (1/rms_value)*20
            #     else: # later game
            #         value += 10*((static_board.num_pieces_white - self.num_pieces_white) - (static_board.num_pieces_black - self.num_pieces_black)) + (1/rms_value)*10
            #     # add random value for last digit of value
            #     #value += random.randint(0, 9)
            # return value

            if self.num_pieces_white == 0 and self.num_pieces_black > 0:
                return 1000000000
            elif self.num_pieces_black == 0 and self.num_pieces_white > 0:
                return -1000000000
            elif self.num_pieces_black > 8 and self.num_pieces_white > 8:
                num_in_king_row = 0
                num_in_center = 0
                for position in self.positions_black:
                    # heuristic for king row pawns
                    if self.positions_black[position] == "pawn":
                        if position[0] == 0:
                            num_in_king_row += 1
                    # heuristic for being in center of board
                    if position[1] > 1 and position[1] < 6:
                        num_in_center += 1
                if static_board.num_pieces_black > 10:
                    return 10*(self.num_pieces_black - self.num_kings_black) + 15*self.num_kings_black + 2*num_in_king_row
                else:
                    return 10*(self.num_pieces_black - self.num_kings_black) + 15*self.num_kings_black + num_in_king_row
            else:

                if static_board.num_pieces_black >= static_board.num_pieces_white:
                    num_lost_black = static_board.num_pieces_black - self.num_pieces_black
                    num_lost_white = static_board.num_pieces_white - self.num_pieces_white
                    if num_lost_black <= num_lost_white:
                        trades = min(num_lost_white, num_lost_black) + 1
                        return 10*(self.num_pieces_black - self.num_kings_black) + 15*self.num_kings_black + 10*trades
                    else:
                        return 10*(self.num_pieces_black - self.num_kings_black) + 15*self.num_kings_black
                else:
                    return 10*(self.num_pieces_black - self.num_kings_black) + 15*self.num_kings_black
            
            #return 10*self.num_pieces_black

            #return 20*(self.num_pieces_black-self.num_kings_black) + 30*self.num_kings_black + 10*(self.num_pieces_black-self.num_pieces_white)
            #return 100*(self.num_pieces_black - self.num_kings_black) + 150*(self.num_kings_black) + 10*(self.num_pieces_black - self.num_pieces_white)
            # if self.num_pieces_black < 10:
            # #========================= hard-coded assignment based on location ======================#
            #     piece_value = {(0,1):4, (0,3):4, (0,5):4, (0,7):4,
            #                 (1,0):4, (1,2):3, (1,4):3, (1,6):3,
            #                 (2,1):3, (2,3):2, (2,5):2, (2,7):4,
            #                 (3,0):4, (3,2):2, (3,4):1, (3,6):3,
            #                 (4,1):3, (4,3):1, (4,5):2, (4,7):4,
            #                 (5,0):4, (5,2):2, (5,4):1, (5,6):3,
            #                 (6,1):3, (6,3):2, (6,5):2, (6,7):4,
            #                 (7,0):4, (7,2):4, (7,4):4, (7,6):4}
            #     h_value = 0
            #     for key in self.positions_black:
            #         h_value += piece_value[key]
            #     return h_value + self.num_kings_black + 5*(self.num_pieces_black-self.num_kings_white)
            # else:
            #     return 4*(self.num_pieces_black - self.num_kings_black) + 8*self.num_kings_black
            #=======================================================================================#  
            #if game over for any player 

            # if self.num_pieces_white == 0 or self.num_pieces_black == 0:
            #     heuristic = (self.num_pieces_black - self.num_kings_black) + 3*(self.num_kings_black) + 20*self.num_pieces_black
            #     return heuristic
            # # calculate heuristics 
            # num_in_king_row = 0
            # num_in_center = 0
            # x_white = []
            # y_white = []
            # x_black = []
            # y_black = []
            # for position in self.positions_black:
            #     # heuristic for king row pawns
            #     if self.positions_black[position] == "pawn":
            #         if position[0] == 7:
            #             num_in_king_row += 1
            #     # heuristic for being in center of board
            #     if position[1] > 1 and position[1] < 6:
            #         num_in_center += 1
            #     # store x and y coords in list
            #     x_black.append(position[0])
            #     y_black.append(position[1])
            # for position in self.positions_white:
            #     # store x and y coords in list
            #     x_white.append(position[0])
            #     y_white.append(position[1])
            # # calculate centroids
            # centroid_white = (mean(x_white), mean(y_white))
            # centroid_black = (mean(x_black), mean(y_black))
            # # calculate distance between centroids
            # dist_bw_centroids = sqrt(pow(centroid_white[0]-centroid_black[0], 2) + pow(centroid_white[1]-centroid_black[1], 2))
            # if self.num_pieces_black > 10: # early in the game
            #     heuristic = 10*(self.num_pieces_black - self.num_kings_black) + 20*num_in_king_row + 5*num_in_center
            # elif self.num_pieces_white < 3:
            #     idling_kings = 0
            #     for position in self.positions_black:
            #         # heuristic to deter kings away from idling at kings row
            #         if self.positions_black[position] == "king":
            #             if position[0] == 0:
            #                 idling_kings += 2
            #             if position[0] == 1 or position[0] == 2:
            #                 idling_kings += 1
            #     heuristic = 10*(self.num_pieces_black) - 5*idling_kings - floor(5*dist_bw_centroids)
            # else: 
            #     heuristic = 10*(self.num_pieces_black - self.num_kings_black) + 30*(self.num_kings_black) + 10*(self.num_pieces_black - self.num_pieces_white)
            # return heuristic
        else: # active player is WHITE
            #return 10*self.num_pieces_white

            if self.num_pieces_black == 0 and self.num_pieces_white > 0:
                return 1000000000
            elif self.num_pieces_white == 0 and self.num_pieces_black > 0:
                return -1000000000
            elif self.num_pieces_black > 8 and self.num_pieces_white > 8:
                num_in_king_row = 0
                num_in_center = 0
                for position in self.positions_white:
                    # heuristic for king row pawns
                    if self.positions_white[position] == "pawn":
                        if position[0] == 0:
                            num_in_king_row += 1
                    # heuristic for being in center of board
                    if position[1] > 1 and position[1] < 6:
                        num_in_center += 1
                if static_board.num_pieces_white > 10:
                    return 10*(self.num_pieces_white - self.num_kings_white) + 15*self.num_kings_white + 2*num_in_king_row
                else:
                    return 10*(self.num_pieces_white - self.num_kings_white) + 15*self.num_kings_white + num_in_king_row
            else:

                if static_board.num_pieces_white >= static_board.num_pieces_black:
                    num_lost_black = static_board.num_pieces_black - self.num_pieces_black
                    num_lost_white = static_board.num_pieces_white - self.num_pieces_white
                    if num_lost_white <= num_lost_black:
                        trades = min(num_lost_white, num_lost_black) + 1
                        return 10*(self.num_pieces_white - self.num_kings_white) + 15*self.num_kings_white + 10*trades
                    else:
                        return 10*(self.num_pieces_white - self.num_kings_white) + 15*self.num_kings_white
                else:
                    return 10*(self.num_pieces_white - self.num_kings_white) + 15*self.num_kings_white

            # #if game over for any player 
            # if self.num_pieces_white == 0 or self.num_pieces_black == 0:
            #     heuristic = (self.num_pieces_white - self.num_kings_white) + 3*(self.num_kings_white) + 20*self.num_pieces_white
            #     return heuristic
            # # calculate heuristics 
            # num_in_king_row = 0
            # num_in_center = 0
            # x_white = []
            # y_white = []
            # x_black = []
            # y_black = []
            # for position in self.positions_white:
            #     # heuristic for king row pawns
            #     if self.positions_white[position] == "pawn":
            #         if position[0] == 7:
            #             num_in_king_row += 1
            #     # heuristic for being in center of board
            #     if position[1] > 1 and position[1] < 6:
            #         num_in_center += 1
            #     # store x and y coords in list
            #     x_white.append(position[0])
            #     y_white.append(position[1])
            # for position in self.positions_black:
            #     # store x and y coords in list
            #     x_black.append(position[0])
            #     y_black.append(position[1])
            # # calculate centroids
            # centroid_white = (mean(x_white), mean(y_white))
            # centroid_black = (mean(x_black), mean(y_black))
            # # calculate distance between centroids
            # dist_bw_centroids = sqrt(pow(centroid_white[0]-centroid_black[0], 2) + pow(centroid_white[1]-centroid_black[1], 2))
            # if self.num_pieces_white > 10: # early in the game
            #     heuristic = 10*(self.num_pieces_white - self.num_kings_white) + 20*num_in_king_row + 5*num_in_center
            # elif self.num_pieces_black < 3:
            #     idling_kings = 0
            #     for position in self.positions_white:
            #         # heuristic to deter kings away from idling at kings row
            #         if self.positions_white[position] == "king":
            #             if position[0] == 0:
            #                 idling_kings += 2
            #             if position[0] == 1 or position[0] == 2:
            #                 idling_kings += 1
            #     heuristic = 10*(self.num_pieces_white) - 5*idling_kings - floor(5*dist_bw_centroids)
            # else: 
            #     heuristic = 10*(self.num_pieces_white - self.num_kings_white) + 30*(self.num_kings_white) + 10*(self.num_pieces_white - self.num_pieces_black)
            # return heuristic

    def game_over(self):
        """
        Check if board is in a game over state
        """
        # if self.num_pieces_black < 3 or self.num_pieces_white < 3:
        #     if self.num_pieces_black == 0 or self.num_pieces_white == 0 or len(self.possible_moves()) == 0:
        #         return True 
        #     else:
        #         return False
        # else:
        #     if self.num_pieces_black == 0 or self.num_pieces_white == 0: #or len(self.possible_moves()) == 0:
        #         return True 
        #     else:
        #         return False

        if self.num_pieces_black == 0 or self.num_pieces_white == 0: #or len(self.possible_moves()) == 0:
            return True 
        else:
            return False

    def empty_here(self, coord):
        """
        Returns true if the coordinate is empty (and on the board)
        """
        if coord in self.positions_empty:
            return True
        else:
            return False

    def opp_here(self, coord):
        """
        Returns true if there is an opponent's piece in the coordinate 
        """
        if self.active_player: # active player is BLACK
            if coord in self.positions_white:
                return True
            else:
                return False
        else: # active player is WHITE
            if coord in self.positions_black:
                return True
            else:
                return False

    def possible_moves(self):
        """ 
        Finds all possible next moves (i.e., all possible next boards)
        input: self (Board)
        output: moves (Dictionary) e.g. {(J, (coord_old), (coord_jump_1), (coord_jump_2)) : new_board}
        """
        moves = {}
        jumps_available = False
        if self.active_player: # active player is BLACK
            for piece in self.positions_black: # loop through all available pieces
                piece_type = self.positions_black[piece]
                # check if jump available (MUST jump if available)
                jumps_queue = self.jumps_available(piece, piece_type, deque())
                if jumps_queue != None:
                    jumps_dict = create_jumps_dict(jumps_queue)
                    jumps_sequences = create_jumps_sequences(jumps_dict, piece)
                    for sequence in jumps_sequences:
                        jumps_available = True
                        board_copy = copy.deepcopy(self)
                        origin = piece
                        for i in range(1, len(sequence)):
                            landing_spot = sequence[i]
                            board_copy = copy.deepcopy(board_copy)
                            if board_copy.jump_move(origin, landing_spot) == "fail":
                                break
                            origin = landing_spot
                        else:
                            sequence.insert(0, "J")
                            sequence = tuple(sequence)    
                            moves[sequence] = board_copy
            if jumps_available == False: # if there are no jumps available to any piece 
                for piece in self.positions_black: 
                    piece_type = self.positions_black[piece]
                    # check if simple move available
                    for move in self.simple_moves_available(piece, piece_type):
                        board_copy = copy.deepcopy(self)
                        board_copy.simple_move(piece, move)
                        move_sequence = ('E', piece, move)
                        moves[move_sequence] = board_copy
        else: # active player is WHITE
            for piece in self.positions_white: # loop through all available pieces
                piece_type = self.positions_white[piece]
                # check if jump available (MUST jump if available)
                jumps_queue = self.jumps_available(piece, piece_type, deque())
                if jumps_queue != None:
                    jumps_dict = create_jumps_dict(jumps_queue)
                    jumps_sequences = create_jumps_sequences(jumps_dict, piece)
                    for sequence in jumps_sequences:
                        jumps_available = True
                        board_copy = copy.deepcopy(self)
                        origin = piece
                        for i in range(1, len(sequence)):
                            landing_spot = sequence[i]
                            board_copy = copy.deepcopy(board_copy)
                            if board_copy.jump_move(origin, landing_spot) == "fail":
                                break
                            origin = landing_spot
                        else:
                            sequence.insert(0, "J")
                            sequence = tuple(sequence)    
                            moves[sequence] = board_copy
            if jumps_available == False: # if there are no jumps available to any piece 
                for piece in self.positions_white: 
                    piece_type = self.positions_white[piece]
                    # check if simple move available
                    for move in self.simple_moves_available(piece, piece_type):
                        board_copy = copy.deepcopy(self)
                        board_copy.simple_move(piece, move)
                        move_sequence = ('E', piece, move)
                        moves[move_sequence] = board_copy
        return moves
            
    def simple_moves_available(self, piece, piece_type):
        """
        Checks which simple moves can be made and returns a list
        """
        moves_available = []
        if piece_type == "king": # check all four diagonals
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    if self.empty_here((piece[0]+i, piece[1]+j)):
                        moves_available.append((piece[0]+i, piece[1]+j))
        else: # piece is a pawn
            if self.active_player: # active player is BLACK
                for j in range(-1, 2, 2): # only moves DOWN (i.e., index goes UP)
                    if self.empty_here((piece[0]+1, piece[1]+j)):
                        moves_available.append((piece[0]+1, piece[1]+j))
            else: # active player is WHITE
                for j in range(-1, 2, 2): # only moves UP (i.e., index goes DOWN)
                    if self.empty_here((piece[0]-1, piece[1]+j)):
                        moves_available.append((piece[0]-1, piece[1]+j))
        return moves_available

    def jumps_available(self, piece, piece_type, jumps): 
        """
        Checks to see if there is a jump available from this piece's coordinate 
        and returns available jumps in list of sequences
        """
        no_jumps = True
        if piece_type == "king": # check all four diagonals
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    if self.opp_here((piece[0]+i, piece[1]+j)) and self.empty_here((piece[0]+2*i, piece[1]+2*j)): 
                        jumps.append(piece)
                        no_jumps = False
                        landing_coord = (piece[0]+2*i, piece[1]+2*j)
                        jumps.append(landing_coord)
                        board_copy = copy.deepcopy(self)
                        board_copy.jump_move(piece, landing_coord)
                        board_copy.jumps_available(landing_coord, piece_type, jumps) # recursive call here
            if no_jumps:
                    return   
        else: # it's a pawn piece
            if self.active_player: # active player is BLACK
                for j in range(-1, 2, 2): # only moves DOWN (i.e., index goes UP)
                    if self.opp_here((piece[0]+1, piece[1]+j)) and self.empty_here((piece[0]+2, piece[1]+2*j)):
                        jumps.append(piece)
                        no_jumps = False
                        landing_coord = (piece[0]+2, piece[1]+2*j)
                        jumps.append(landing_coord)
                        board_copy = copy.deepcopy(self)
                        board_copy.jump_move(piece, landing_coord)
                        board_copy.jumps_available(landing_coord, piece_type, jumps) # recursive call here
                if no_jumps:
                    return   
            else: # active player is WHITE
                for j in range(-1, 2, 2): # only moves UP (i.e., index goes DOWN)
                    if self.opp_here((piece[0]-1, piece[1]+j)) and self.empty_here((piece[0]-2, piece[1]+2*j)): # jump available
                        jumps.append(piece)
                        no_jumps = False
                        landing_coord = (piece[0]-2, piece[1]+2*j)
                        jumps.append(landing_coord)
                        board_copy = copy.deepcopy(self)
                        board_copy.jump_move(piece, landing_coord)
                        board_copy.jumps_available(landing_coord, piece_type, jumps) # recursive call here
                if no_jumps:
                    return         
        return jumps
        # jumps_dict = create_jumps_dict(jumps)
        # jumps_sequences = create_jumps_sequences(jumps_dict, piece)
        # return jumps_sequences