import numpy as np
import itertools

frontier_no = 0
frontiers = {}


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
        func(i, j, map)


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


fi = open("tests/uncertainty1.in", "r+")
input_file = fi.read()
print(input_file)
input_file = input_file.split()
# print("Input file String is : \n", input_file)
fo = open("tests/uncertainty1.out", "r+")
output_file = fo.read()
print(output_file)
output_file = output_file.split()
# print("Output file String is : \n", output_file)
print(fo.read())

y = input_file[0]
x = input_file[1]
probability_pit = input_file[2]

# print(list(itertools.product('01', repeat=3)))
# print(y)
world = np.asarray([list(row) for row in input_file[3:]])

print(world)

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
            compute[i, j] = 0
            check2(i - 1, j, world, create_f)
            check2(i, j + 1, world, create_f)
            check2(i + 1, j, world, create_f)
            check2(i, j - 1, world, create_f)
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

print(compute)
print(world)
print(frontiers)

for frontier_key in frontiers:
    for product in itertools.product('01', repeat=len(frontiers[frontier_key])):
        print(world)
        frontier_value = frontiers[frontier_key]
        for a, el in enumerate(product):
            world[frontier_value[a][0], frontier_value[a][1]] = el
        print(world)

fo.close()
