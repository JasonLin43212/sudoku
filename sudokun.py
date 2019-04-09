import sys

f = open("Sudoku-boards.txt",'r')
lines = f.read().split("\n")
sudoku_dict = {}
current_dict = {"data":[]}
got_desc = False

for i in range(len(lines)):
    if not got_desc:
        descriptions = lines[i].split(",")
        current_dict["name"] = descriptions[0]
        current_dict["difficulty"] = descriptions[1]
        current_dict["state"] = descriptions[2]
        got_desc = True
    elif lines[i] == '':
        sudoku_dict[current_dict["name"]] = current_dict
        current_dict = {"data":[]}
        got_desc = False
    else:
        nums = lines[i].split(",")
        current_arr = []
        for i in range(len(nums)):
            if nums[i] == '_':
                current_arr.append(0)
            else:
                current_arr.append(int(nums[i]))
        current_dict["data"] += current_arr

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

class Sudoku:

    def __init__(self,arr):
        self.data = arr
        self.past = []

    def print_sudoku(self):
        temp_arr = []
        for i in range(9):
            temp_arr.append(self.data[i*9:i*9+9])
        for row in temp_arr:
            line = ""
            for num in row:
                line += str(num) + " "
            print (line)
            line = ""
        print("\n")

    def solve(self):
        index = 0
        current_possibilities = set()
        has_previous_possiblility = False

        # While the current cell is not after the last cell
        while index != 81:
            if self.data[index] != 0:
                index += 1
                continue
            # Get the index of all of the cliques of the current cell
            # Removes repetition with sets
            all_cliques = set()
            for clique in cliques:
                if index in clique:
                    all_cliques = all_cliques.union(clique)
            all_cliques.remove(index)

            # If backtracking, then use the previous list of possibilities
            # If exploring new territory, then make the new list of possibilities
            possibilities = set([1,2,3,4,5,6,7,8,9])
            if has_previous_possiblility:
                possibilities = current_possibilities
            else:
                taken_values = set([self.data[x] for x in all_cliques])
                possibilities = possibilities.difference(taken_values)

            # Checks if it ran out of possibilities
            # Reverts to a previous state
            # Else, insert a random number from the list of possibilities
            # and move on to the next cell
            if len(possibilities) == 0:
                if len(self.past) == 0:
                    print("This sudoku is impossible")
                    break
                self.data = self.past[-1][0]
                current_possibilities = self.past[-1][1]
                index = self.past[-1][2]
                has_previous_possiblility = True
                self.past = self.past[:-1]
            else:
                test_insert = possibilities.pop()
                self.past.append((self.data[:],possibilities,index))
                self.data[index] = test_insert
                current_possibilities = set()
                has_previous_possiblility = False
                index += 1

s = Sudoku(sudoku_dict['A7-1']['data'])
s.solve()
s.print_sudoku()
