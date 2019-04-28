#! /usr/bin/python3
import sys
import time

# print_sudoku(sudoku_dict['oneunsolved']["data"])
cliques=[[0,1,2,3,4,5,6,7,8],\
[9,10,11,12,13,14,15,16,17],\
[18,19,20,21,22,23,24,25,26],\
[27,28,29,30,31,32,33,34,35],\
[36,37,38,39,40,41,42,43,44],\
[45,46,47,48,49,50,51,52,53],\
[54,55,56,57,58,59,60,61,62],\
[63,64,65,66,67,68,69,70,71],\
[72,73,74,75,76,77,78,79,80],\
[0,9,18,27,36,45,54,63,72],\
[1,10,19,28,37,46,55,64,73],\
[2,11,20,29,38,47,56,65,74],\
[3,12,21,30,39,48,57,66,75],\
[4,13,22,31,40,49,58,67,76],\
[5,14,23,32,41,50,59,68,77],\
[6,15,24,33,42,51,60,69,78],\
[7,16,25,34,43,52,61,70,79],\
[8,17,26,35,44,53,62,71,80],\
[0,1,2,9,10,11,18,19,20],\
[3,4,5,12,13,14,21,22,23],\
[6,7,8,15,16,17,24,25,26],\
[27,28,29,36,37,38,45,46,47],\
[30,31,32,39,40,41,48,49,50],\
[33,34,35,42,43,44,51,52,53],\
[54,55,56,63,64,65,72,73,74],\
[57,58,59,66,67,68,75,76,77],\
[60,61,62,69,70,71,78,79,80]\
]
all_nums = set([1,2,3,4,5,6,7,8,9])
def get_sudoku(data):
        temp_arr = []
        for i in range(9):
            temp_arr.append(data[i*9:i*9+9])
        output = ""
        for row in temp_arr:
            line = ""
            for num in row:
                line += str(num) + ","
            output += line[:-1] + "\n"
        return output[:-1]

def get_possibilities(data, index):
    # Get the index of all of the cliques of the current cell
    # Removes repetition with sets
    all_cliques = set()
    for clique in cliques:
        if index in clique:
            all_cliques = all_cliques.union(clique)
    all_cliques.remove(index)
    taken_values = set([data[x] for x in all_cliques])
    possibilities = all_nums.difference(taken_values)
    return possibilities

def fill_obvious(data):
    has_obvious = True
    while has_obvious:
        has_obvious = False
        for index in range(81):
            if data[index] == 0:
                possibilities = get_possibilities(data,index)
                if len(possibilities) == 1:
                    data[index] = possibilities.pop()
                    has_obvious = True
    return data

def get_next_index(data):
    best_index = -1
    least_num_possible = 10
    for i in range(81):
        if data[i] == 0:
            num_possible = len(get_possibilities(data,i))
            if num_possible < least_num_possible:
                best_index = i
                least_num_possible = num_possible
    return best_index

def solve(data, mode):
    past = []
    index = 0
    if mode == "2":
        index = get_next_index(data)
    current_possibilities = set()
    has_previous_possiblility = False
    ntrials = 0
    nback = 0
    while True:
        if (mode != "2" and index == 81) or (mode == "2" and index==-1):
            break
        if mode != "0":
            data = fill_obvious(data)
        ntrials += 1
        # if ntrials % 10000 == 0: print ('ntrials',ntrials)
        if data[index] != 0:
            if mode == "2":
                index = get_next_index(data)
            else:
                index += 1
            continue
        # If backtracking, then use the previous list of possibilities
        # If exploring new territory, then make the new list of possibilities
        possibilities = None
        if has_previous_possiblility:
            possibilities = current_possibilities
        else:
            possibilities = get_possibilities(data,index)
        # Checks if it ran out of possibilities
        # Reverts to a previous state
        # Else, insert a random number from the list of possibilities
        # and move on to the next cell
        if len(possibilities) == 0:
            if len(past) == 0:
                print("This sudoku is impossible")
                break
            nback += 1
            data = past[-1]["data"]
            current_possibilities = past[-1]["possibilities"]
            index = past[-1]["index"]
            has_previous_possiblility = True
            past = past[:-1]
        else:
            test_insert = possibilities.pop()
            past.append({"data":data[:],"possibilities":possibilities,"index":index})
            data[index] = test_insert
            current_possibilities = set()
            has_previous_possiblility = False
            if mode == "2":
                index = get_next_index(data)
            else:
                index += 1
    print("backtracks:",nback)
    return data


def getBoard(name):
    f = open(sys.argv[1],'r')
    lines = f.read().split("\n")
    rel_index =  lines.index(name)
    relevant_data = lines[rel_index+1:rel_index+10]
    data = []
    for sudoku_line in relevant_data:
        for num in sudoku_line.split(","):
            if num == "_":
                data.append(0)
            else:
                data.append(int(num))
    return data


write_output = ''

# Fourth Argument
# 0: Naive Solution
# 1: Fill in all obvious ones first\
# 2: Choose squares with least open spots
#
s = time.time()
solved_board = solve(getBoard(sys.argv[3]), sys.argv[4])
print(time.time() - s,"seconds")

write_output= get_sudoku(solved_board)

f = open(sys.argv[2],'w')
f.write(write_output)
f.close()
