import copy
import itertools
import math
import random
import matplotlib.pyplot as plt

from warnings import resetwarnings


def load_instance(filename):
    vertices = []
    with open(filename, 'r') as f:
        data = f.readlines()
        data = data[6:-1]
    for line in data:
        vertices.append([int(v) for v in line.split()[1:]])
    return vertices


def create_distance_matrix(vertices):
    matrix = []
    for i in vertices:
        line = []
        for j in vertices:
            distance = round(math.sqrt((i[0] - j[0]) ** 2 + (i[1] - j[1]) ** 2))
            line.append(distance)
        matrix.append(line)
    return matrix


def calculate_score(vertices, distance_matrix, cycle=True):
    score = 0
    for i in range(len(vertices) - 1):
        score += distance_matrix[vertices[i]][vertices[i+1]]
    if cycle and len(vertices) > 2:
        score += distance_matrix[vertices[0]][vertices[-1]]
    return score


def swap_vertices(vertices, vertices2, distance_matrix, vertex, vertex2):
    v1 = copy.deepcopy(vertices)
    v2 = copy.deepcopy(vertices2)
    score = calculate_score(v1, distance_matrix) + calculate_score(v2, distance_matrix)

    if vertex in v1 and vertex2 in v1:
        index = v1.index(vertex)
        index2 = v1.index(vertex2)
        v1[index], v1[index2] = v1[index2], v1[index]
    elif vertex in v1 and vertex2 in v2:
        index = v1.index(vertex)
        index2 = v2.index(vertex2)
        v2[index2], v1[index] = v1[index], v2[index2]
    elif vertex in v2 and vertex2 in v1:
        index = v2.index(vertex)
        index2 = v1.index(vertex2)
        v1[index2], v2[index] = v2[index], v1[index2]
    else:
        index = v2.index(vertex)
        index2 = v2.index(vertex2)
        v2[index], v2[index2] = v2[index2], v2[index]

    if calculate_score(v1, distance_matrix) + calculate_score(v2, distance_matrix) < score:
        return v1, v2
    return vertices, vertices2


def local_search_1(vertices, vertices2, distance_matrix):
    v1 = copy.deepcopy(vertices)
    v2 = copy.deepcopy(vertices2)

    if random.randint(0, 1):
        v = v1
    else:
        v = v2
    index1 = v[random.randint(0, len(v) - 1)]
    vs = sorted(distance_matrix[index1])[1:11]
    vs = [distance_matrix[index1].index(x) for x in vs]
    index2 = vs[random.randint(0, len(vs)) - 1]

    v1, v2 = swap_vertices(v1, v2, distance_matrix, index1, index2)

    return v1, v2


def iterated_local_search(vertices, vertices2, distance_matrix):
    v1 = copy.deepcopy(vertices)
    v2 = copy.deepcopy(vertices2) 

    for i in range(1000):
        v1, v2 = local_search_1(v1, v2, distance_matrix)

    return v1, v2


def get_best_insertion(vertices, vertices2, distance_matrix, position=True, cycle=False):
    best_vertex = None
    best_score = None
    best_position = None

    for i in range(len(distance_matrix)):
        if i in vertices + vertices2:
            continue
        for position in range(len(vertices) + 1):
            temp_vertices = copy.copy(vertices)
            temp_vertices.insert(position, i)
            score = calculate_score(temp_vertices, distance_matrix, cycle=True)
            if best_score is None or score < best_score:
                best_score = score
                best_vertex = i
                best_position = position

    return best_vertex, best_position, best_score


def local_search_2(vertices, vertices2, distance_matrix):
    v1 = copy.deepcopy(vertices)
    v2 = copy.deepcopy(vertices2)
    score = calculate_score(v1, distance_matrix) + calculate_score(v2, distance_matrix)

    if random.randint(0, 1):
        v = v1
    else:
        v = v2
    index1 = v[random.randint(0, len(v) - 1)]
    vs = sorted(distance_matrix[index1])[1:int(len(distance_matrix) * 0.2 - 1)]
    vs = [distance_matrix[index1].index(x) for x in vs]
    for v in vs:
        if v in v1:
            v1.remove(v)
        if v in v2:
            v2.remove(v)

    d = False
    for vertex_i in vs:
        if d:
            break
        x = sorted(distance_matrix[vertex_i])
        x = [distance_matrix[vertex_i].index(y) for y in x]
        for k in x:
            if len(v1) + len(v2) == len(distance_matrix):
                d = True
                break
            if k in vs:
                continue
            if k in v1:
                best_vertex, best_position, _ = get_best_insertion(v1, v2, distance_matrix)
                v1.insert(best_position, best_vertex)
                break
            else:
                best_vertex, best_position, _ = get_best_insertion(v2, v1, distance_matrix)
                v2.insert(best_position, best_vertex)
                break

    if calculate_score(v1, distance_matrix) + calculate_score(v2, distance_matrix) < score:
        return v1, v2
    return vertices, vertices2


def iterated_local_search_2(vertices, vertices2, distance_matrix):
    v1 = copy.deepcopy(vertices)
    v2 = copy.deepcopy(vertices2) 

    for i in range(50):
        v1, v2 = local_search_2(v1, v2, distance_matrix)

    return v1, v2


def plot(instance, data1, data2):
    path1_x = []
    path1_y = []
    
    path2_x = []
    path2_y = []

    for d in data1:
        path1_x.append(instance[d][0])
        path1_y.append(instance[d][1])
    for d in data2:
        path2_x.append(instance[d][0])
        path2_y.append(instance[d][1])

    plt.plot(path1_x, path1_y)
    plt.plot(path2_x, path2_y)
    plt.show()
