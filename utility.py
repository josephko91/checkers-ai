# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 2
# Checkers AI
# Author: Joseph Ko
# This module holds utility functions
# -------------------------------------------------------
from collections import deque
import copy
#import numpy as np

def create_jumps_dict(jumps):
    jumps_dict = {}
    while jumps: # while deque is not empty
        parent = jumps.popleft()
        child = jumps.popleft()
        if parent in jumps_dict:
            child_list = jumps_dict[parent]
            child_list.append(child)
            jumps_dict[parent] = child_list
        else:
            jumps_dict[parent] = [child]
    return jumps_dict

def create_jumps_sequences(jumps_dict, piece):
    loop_present = False
    jumps_sequences = [[piece]]
    for parent in jumps_dict:
        leaves = jumps_dict[parent]
        temp_list = []
        for i in range(len(jumps_sequences)):
            sequence = jumps_sequences[i]
            length_list = len(sequence)
            if sequence[length_list-1] == parent:
                for j in range(len(leaves)-1):
                    if leaves[j+1] == piece: # loop detect
                        loop_present = True
                    sequence_copy = copy.deepcopy(sequence)
                    sequence_copy.append(leaves[j+1])
                    temp_list.append(sequence_copy)
                sequence.append(leaves[0])
                if leaves[0] == piece: # loop detect
                    loop_present = True
        for i in range(len(temp_list)):
            jumps_sequences.append(temp_list[i])
        
    # # if there is a loop, only keep the biggest loop and eliminate invalid jumps sequences
    # if loop_present:
    #     sequences_to_remove = []
    #     longest_loop_length = 0
    #     for i in range(len(jumps_sequences)):
    #         sequence = jumps_sequences[i]
    #         # save index of sequences that loop to a position that is not the initial position
    #         if list_has_duplicates(sequence)[0]:
    #             duplicate = list_has_duplicates(sequence)[1]
    #             if duplicate != piece:
    #                 sequences_to_remove.append(i)
    #             else: # loops that end up back at initial position
    #                 if len(sequence) > longest_loop_length:
    #                     longest_loop_length = len(sequence) # update longest loop
    #     # remove sequences that loop to a position that is not the initial position
    #     jumps_sequences = np.delete(jumps_sequences, sequences_to_remove).tolist()
    #     # create list with only longest sequences
    #     longest_loops = []
    #     for i in range(len(jumps_sequences)):
    #         sequence = jumps_sequences[i]
    #         if len(sequence) == longest_loop_length:
    #             longest_loops.append(sequence) # append to longest sequence list
    #     # if a sequence is in the set of any of the longest sequences -> delete
    #     sequences_to_remove = []
    #     for i in range(len(jumps_sequences)):
    #         sequence = jumps_sequences[i]
    #         for j in range(len(longest_loops)):
    #             longest = longest_loops[j]
    #             if in_set(sequence, longest):
    #                 sequences_to_remove.append(i)
    #     # remove the sequences in the set of longest sequences
    #     jumps_sequences = np.delete(jumps_sequences, sequences_to_remove).tolist()
    # final return         
    return jumps_sequences

# def in_set(sequence, longest):
#     if len(sequence) == len(longest):
#         if (np.array(sequence) == np.array(longest)).all():
#             return False
#     set_of_sequence = set(sequence)
#     set_of_longest = set(longest)
#     for element in set_of_sequence:
#         if element not in set_of_longest:
#             return False
#     return True

# def list_has_duplicates(list):
#     set_of_elements = set()
#     for element in list:
#         if element in set_of_elements:
#             return True, element
#         else:
#             set_of_elements.add(element)
#     return False, None

def write_to_output(result, output):
    """ 
    This function takes the result array and writes it to output in correct format 
    input: result (list), output (file object)
    output: none
    """
    first_element = result[0]
    if first_element == "E": 
        print("E", convert_coord(result[1]), convert_coord(result[2]), file = output, end = "")
        print("E", convert_coord(result[1]), convert_coord(result[2])) # print to terminal, testing
    else:
        for i in range(1, len(result) - 1, 1):
            if i == len(result)-2:
                print("J", convert_coord(result[i]), convert_coord(result[i+1]), file = output, end = "")
                print("J", convert_coord(result[i]), convert_coord(result[i+1])) # print to terminal, testing
            else:
                print("J", convert_coord(result[i]), convert_coord(result[i+1]), file = output, end = "\n")
                print("J", convert_coord(result[i]), convert_coord(result[i+1])) # print to terminal, testing

def convert_coord(coord):
    """
    Converts coordinate tuple to format required for output
    """
    col_dictionary = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
    row = str(8 - coord[0])
    column = str(col_dictionary[coord[1]])
    position = column + row
    return position

def print_board(board):
    """ 
    This will print the board in a readable format 
    input: board (list)
    output: none
    """
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in board]))

def color_is_black(color): 
    if color == "BLACK":
        return True
    else:
        return False

def board_to_list(board):
    """
    converts from Board object to list format
    """
    board_list = [["." for j in range(8)] for i in range(8)]
    for position in board.positions_white:
        if board.positions_white[position] == "king":
            board_list[position[0]][position[1]] =  "W"
        else:
            board_list[position[0]][position[1]] =  "w"
    for position in board.positions_black:
        if board.positions_black[position] == "king":
            board_list[position[0]][position[1]] =  "B"
        else:
            board_list[position[0]][position[1]] =  "b"
    return board_list

def print_results(board, result, board_list, iteration_count, runtime):
    if board.active_player == True:
        player = "black"
    else:
        player = "white"
    print("============== iteration:", iteration_count, "==============")
    print("runtime:", runtime)
    print("player:", player)
    print("black pieces:", board.num_pieces_black, ", white pieces:", board.num_pieces_white)
    print("move:", result)
    for row in board_list:
        print(row)