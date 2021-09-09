#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 20:40:45 2021

@author: avasisht
"""

from copy import copy
import heapq

def convert_list_to_matrix(input_list):
    matrix = []
    for i in range(3):
        matrix.append(input_list[i*3:(i*3)+3])
    return matrix

def heuristic(matrix):
    i = -1
    heuristic_total = 0 

    for row in matrix:
        i += 1
        j = -1
        for col in row:
            j += 1
            value = col
            if value == 0:
                continue
            current = [i, j]
            desired = [(value-1)//3, (value -1)%3] 
            
            x_curr, y_curr = current
            x_dest, y_dest = desired
               
            heuristic_total += abs(x_dest - x_curr) + abs(y_dest - y_curr) 
        
    return heuristic_total


def get_successors(input_list):
    empty = input_list.index(0) 

    zero_i, zero_j = empty // 3, empty % 3 

    neighbors = [(zero_i, zero_j-1), (zero_i,zero_j+1),(zero_i+1, zero_j), (zero_i-1, zero_j)]
    successors = [] 
    
    for new_i, new_j in neighbors:
        if new_i < 0 or new_i > 2 or new_j < 0 or new_j > 2: 
            continue
        successor = copy(input_list)
        value_location = new_i * 3 + new_j
        successor[empty] = successor[value_location]
        successor[value_location] = 0  
        successors.append(successor) 
    return sorted(successors)

def print_succ(input_list):
    successors = get_successors(input_list)
    for successor in successors:
        matrix = convert_list_to_matrix(successor)
        h_total = heuristic(matrix)
        print("{} h={}".format(successor, h_total))
        
def solve(input_list):
    priority_queue = [] 
    seen = set()
    max_queue_len = 0
    counter = 0
    
    print_list = {}
    trace_list = {}
    final_idx = -1
    
    heuristic_total = heuristic(convert_list_to_matrix(input_list))
    heapq.heappush(priority_queue,(heuristic_total , input_list, (0, heuristic_total, -1, counter)))
    while True:
        priority, current_list, (g,h,parent_idx, idx) = heapq.heappop(priority_queue)
        print_list[idx] = "{} h ={} moves: {}".format(current_list, h, g)
        trace_list[idx] = parent_idx
        if h == 0:
            final_idx = idx
            break
        successors = get_successors(current_list)
        parent_idx = idx
        for s in successors:
            s_str = "".join([str(val) for val in s])
            if s_str in seen:
                continue
            seen.add(s_str)
            heuristic_total = heuristic(convert_list_to_matrix(s))
            counter +=1
            heapq.heappush(priority_queue, (heuristic_total + g + 1, s, (g + 1,heuristic_total,parent_idx, counter)))
            max_queue_len = max(len(priority_queue),max_queue_len)
    idx = final_idx
    solution = []
    while idx != -1:
        solution.append(print_list[idx])
        idx = trace_list[idx]
    for string in reversed(solution):
        print(string)
    print("Max queue length: {}".format(max_queue_len))
    
solve([3,1,2,4,5,6,7,8,0])

