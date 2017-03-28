import numpy as np
import itertools

frontier_no = 0
frontiers = {}
breeze = {}
possible_world = {}


# def check(direction, i, j, type, map):
#     if direction == 0 and i > 1:
#         return map[i - 1, j] == type
#     elif direction == 1 and j < len(map[0]) - 1:
#         return map[i, j + 1] == type
#     elif direction == 2 and i < len(map) - 1:
#         return map[i + 1, j] == type
#     elif direction == 3 and j > 1:
#         return map[i, j - 1] == type
#     return False;

def check(i, j, map):
    if 0 <= i < len(map) and 0 <= j < len(map[0]):
        return True
    return False


def check2(i, j, map, func):
    if 0 <= i < len(map) and 0 <= j < len(map[0]):
        return func(i, j, map)
    return False


def check_neighbours(i, j, map, func):
    return \
        check2(i - 1, j, map, func) or \
        check2(i, j + 1, map, func) or \
        check2(i + 1, j, map, func) or \
        check2(i, j - 1, map, func)


# def create_frontier(i,j,map):


def create_f(i, j, map):
    if map[i, j] == '?':
        map[i, j] = str(frontier_no)
        frontiers[frontier_no].append((i, j))
    elif map[i, j].isdigit():
        # for ele in dicto[int(map[i, j])]:
        previous_frontier_no = int(map[i, j])
        while frontiers[previous_frontier_no]:
            ele = frontiers[previous_frontier_no].pop()
            map[ele[0], ele[1]] = str(frontier_no)
            frontiers[frontier_no].append(ele)
        del frontiers[previous_frontier_no]
        breeze[frontier_no].extend(breeze[previous_frontier_no])
        del breeze[previous_frontier_no]


fi = open("tests/uncertainty1.in", "r+")
input_file = fi.read()
# print(input_file)
input_file = input_file.split()
# print("Input file String is : \n", input_file)
fo = open("tests/uncertainty1.out", "r+")
output_file = fo.read()
print(output_file)
output_file = output_file.split()
# print("Output file String is : \n", output_file)
# print(fo.read())

y = input_file[0]
x = input_file[1]
# probability_pit = int(input_file[2])
probability_pit = 0.1
negative_probability_pit = 1 - probability_pit

# print(list(itertools.product('01', repeat=3)))
# print(y)
world = np.asarray([list(row) for row in input_file[3:]])

# print(world)

compute = np.ones([int(y), int(x)])

for i, row in enumerate(world):
    for j, element in enumerate(row):
        if element == 'O':
            compute[i, j] = 0
            if check(i - 1, j, world):
                if world[i - 1, j] == '?':
                    world[i - 1, j] = 'N'
            if check(i, j + 1, world):
                if world[i, j + 1] == '?':
                    world[i, j + 1] = 'N'
            if check(i + 1, j, world):
                if world[i + 1, j] == '?':
                    world[i + 1, j] = 'N'
            if check(i, j - 1, world):
                if world[i, j - 1] == '?':
                    world[i, j - 1] = 'N'

for i, row in enumerate(world):
    for j, element in enumerate(row):
        if element == 'B':
            frontiers[frontier_no] = []
            breeze[frontier_no] = []
            breeze[frontier_no].append((i, j))
            compute[i, j] = 0
            check_neighbours(i, j, world, create_f)
            # if check(i - 1, j, world):
            #     # if world[i - 1, j] == '?':
            #     #
            #     #     world[i - 1, j] = str(frontier_no)
            #     # elif world[i - 1, j].isdigit():
            #     #     world[i - 1, j] = str(frontier_no)
            #
            # if check(i, j + 1, world):
            #     if world[i, j + 1] == '?':
            #         world[i, j + 1] = str(frontier_no)
            # if check(i + 1, j, world):
            #     if world[i + 1, j] == '?':
            #         world[i + 1, j] = str(frontier_no)
            # if check(i, j - 1, world):
            #     if world[i, j - 1] == '?':
            #         world[i, j - 1] = str(frontier_no)
            frontier_no += 1

# print(compute)
# print(world)
# print(frontiers)
# print(breeze)
# possible_world = []

for frontier_key in frontiers:
    possible_world[frontier_key] = []
    for product in itertools.product('01', repeat=len(frontiers[frontier_key])):
        # print(world)
        frontier_value = frontiers[frontier_key]
        for i, element in enumerate(product):
            world[frontier_value[i][0], frontier_value[i][1]] = element
        possible = True
        for bree in breeze[frontier_key]:
            possible = possible and check_neighbours(bree[0], bree[1], world, lambda i, j, map: map[i, j] == '1')
        if possible:
            possible_world[frontier_key].append(product)
            # print(world)
            # print(world)
print(possible_world)
print(frontiers)

for frontier_key in frontiers:
    for i, element in enumerate(frontiers[frontier_key]):
        sum_hole_exist = 0
        sum_hole_not_exist = 0

        for possible in possible_world[frontier_key]:
            multipy = 1
            print(possible)
            for j, hole_frontier in enumerate(possible):
                if i != j:
                    if hole_frontier == '1':
                        multipy *= probability_pit
                    else:
                        multipy *= negative_probability_pit
            if possible[i] == '1':
                sum_hole_exist += multipy
            else:
                sum_hole_not_exist += multipy
        hole_exist = sum_hole_exist * probability_pit
        hole_not_exist = sum_hole_not_exist * negative_probability_pit
        alpha = 1 / (hole_exist + hole_not_exist)
        print(alpha)
        hole_exist *= alpha
        hole_not_exist *= alpha
        compute[element[0], element[1]] = round(hole_exist, 2)

print(compute)

fo.close()
