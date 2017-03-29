import numpy as np
import itertools
import sys

frontier_no = 0
frontiers = {}
breeze = {}
possible_world = {}


def check(i, j, map, func):
    if 0 <= i < len(map) and 0 <= j < len(map[0]):
        return func(i, j, map)
    return False


def check_exposed(i, j, map):
    if map[i, j] == '?':
        map[i, j] = 'N'
        compute[i, j] = 0
        return True
    return False


def check_neighbours(i, j, map, func):
    check(i - 1, j, map, func)
    check(i, j + 1, map, func)
    check(i + 1, j, map, func)
    check(i, j - 1, map, func)


def exist_neighbours(i, j, map, func):
    return \
        check(i - 1, j, map, func) or \
        check(i, j + 1, map, func) or \
        check(i + 1, j, map, func) or \
        check(i, j - 1, map, func)


def create_frontier(i, j, map):
    if map[i, j] == '?':
        map[i, j] = str(frontier_no)
        frontiers[frontier_no].append((i, j))
    elif map[i, j].isdigit():
        previous_frontier_no = int(map[i, j])
        if previous_frontier_no == frontier_no:
            return
        if not previous_frontier_no in frontiers:
            return
        while frontiers[previous_frontier_no]:
            ele = frontiers[previous_frontier_no].pop()
            map[ele[0], ele[1]] = str(frontier_no)
            frontiers[frontier_no].append(ele)
        del frontiers[previous_frontier_no]
        breeze[frontier_no].extend(breeze[previous_frontier_no])
        del breeze[previous_frontier_no]


fi = open(sys.argv[1], "r+")
input_file = fi.read().split()
fi.close()

y = input_file[0]
x = input_file[1]

probability_pit = float("{0:.2f}".format(float(input_file[2])))
negative_probability_pit = 1 - probability_pit
world = np.asarray([list(row) for row in input_file[3:]])
compute = np.ones([int(y), int(x)])
compute.fill(probability_pit)

for i, row in enumerate(world):
    for j, element in enumerate(row):
        if element == 'O':
            compute[i, j] = 0
            check_neighbours(i, j, world, check_exposed)

for i, row in enumerate(world):
    for j, element in enumerate(row):
        if element == 'B':
            frontiers[frontier_no] = []
            breeze[frontier_no] = []
            breeze[frontier_no].append((i, j))
            compute[i, j] = 0
            check_neighbours(i, j, world, create_frontier)
            frontier_no += 1

for frontier_key in frontiers:
    possible_world[frontier_key] = []
    for product in itertools.product('01', repeat=len(frontiers[frontier_key])):
        frontier_value = frontiers[frontier_key]
        for i, element in enumerate(product):
            world[frontier_value[i][0], frontier_value[i][1]] = element
        possible = True
        for bree in breeze[frontier_key]:
            possible = possible and exist_neighbours(bree[0], bree[1], world, lambda i, j, map: map[i, j] == '1')
        if possible:
            possible_world[frontier_key].append(product)

for frontier_key in frontiers:
    for i, element in enumerate(frontiers[frontier_key]):
        sum_hole_exist = 0
        sum_hole_not_exist = 0

        for possible in possible_world[frontier_key]:
            multiply = 1
            for j, hole_frontier in enumerate(possible):
                if i != j:
                    if hole_frontier == '1':
                        multiply *= probability_pit
                    else:
                        multiply *= negative_probability_pit
            if possible[i] == '1':
                sum_hole_exist += multiply
            else:
                sum_hole_not_exist += multiply
        hole_exist = sum_hole_exist * probability_pit
        hole_not_exist = sum_hole_not_exist * negative_probability_pit
        alpha = 1 / (hole_exist + hole_not_exist)
        hole_exist *= alpha
        hole_not_exist *= alpha
        compute[element[0], element[1]] = round(hole_exist, 2)

compute_string = ""
for row in compute:
    compute_string = compute_string + str(['{:.2f}'.format(cell) for cell in row]) + '\n'

fo = open(sys.argv[2], "w+")
fo.write(''.join(c for c in compute_string if c not in ',[]\''))
fo.close()
