import copy
import math
import random


def load_instance(filename):
    vertices = []
    with open(filename, 'r') as f:
        data = f.readlines()
        data = data[6:-1]
    for line in data:
        vertices.append([int(v) for v in line.split()[1:]])
    return vertices


def get_second_vertex(first_vertex, distance_matrix):
    max_distance = max(distance_matrix[first_vertex])
    return distance_matrix[first_vertex].index(max_distance)


def create_distance_matrix(vertices):
    matrix = []
    for i in vertices:
        line = []
        for j in vertices:
            distance = round(math.sqrt((i[0] - j[0]) ** 2 + (i[1] - j[1]) ** 2))
            line.append(distance)
        matrix.append(line)
    return matrix


def calculate_score(vertices, distance_matrix, cycle=False):
    score = 0
    for i in range(len(vertices) - 1):
        score += distance_matrix[vertices[i]][vertices[i+1]]
    if cycle and len(vertices) > 2:
        score += distance_matrix[vertices[0]][vertices[-1]]
    return score


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


def greedy(distance_matrix, start_vertex=0):
    vertices1 = []
    vertices2 = []
    vertices1.append(start_vertex)
    vertices2.append(get_second_vertex(start_vertex, distance_matrix)) # wybieranie najdaljszego

    matrix_len = len(distance_matrix)

    for l in range(matrix_len - 2):
        if l % 2 == 0:
            vertices = vertices1
        else:
            vertices = vertices2
        best_vertex = None
        best_score = None
        index = None

        for i in vertices:
            for j in range(len(distance_matrix)):
                if i == j or j in vertices1 + vertices2:
                    continue
                score = distance_matrix[i][j]
                if best_score is None or score < best_score:
                    best_score = score
                    best_vertex = j

        vertices.append(best_vertex)
    return vertices1 + vertices1[:1], vertices2 + vertices2[:1]


def greedy_cycle(distance_matrix, start_vertex=0):
    vertices1 = []
    vertices1.append(start_vertex)
    vertices2 = []
    vertices2.append(get_second_vertex(start_vertex, distance_matrix))

    matrix_len = len(distance_matrix)

    for l in range(matrix_len - 2):
        if l % 2 == 0:
            vertices, vertices_2 = vertices1, vertices2
        else:
            vertices, vertices_2 = vertices2, vertices1
        best_vertex, best_position, _ = get_best_insertion(vertices, vertices_2, distance_matrix)
        vertices.insert(best_position, best_vertex)
    return vertices1 + vertices1[:1], vertices2 + vertices2[:1]


def regret_heuristics(distance_matrix, start_vertex=0):
    vertices1 = []
    vertices1.append(start_vertex)
    vertices2 = []
    vertices2.append(get_second_vertex(start_vertex, distance_matrix))

    matrix_len = len(distance_matrix)

    for l in range(matrix_len - 4):
        if l % 2 == 0:
            vertices, vertices_2 = vertices1, vertices2
        else:
            vertices, vertices_2 = vertices2, vertices1
        temp1 = copy.copy(vertices)
        temp2 = copy.copy(vertices)
        best_vertex_1, best_position_1, _ = get_best_insertion(temp1, vertices_2, distance_matrix)
        temp1.insert(best_position_1, best_vertex_1)
        best_vertex_2, best_position_2, _ = get_best_insertion(temp1, vertices_2, distance_matrix)
        temp1.insert(best_position_2, best_vertex_2)

        temp2.insert(best_position_2, best_vertex_2)
        temp2.insert(best_position_1, best_vertex_1)
        if calculate_score(temp2, distance_matrix) < calculate_score(temp1, distance_matrix):
            vertices.insert(best_position_2, best_vertex_2)
        else:
            vertices.insert(best_position_1, best_vertex_1)

    for i in range(matrix_len):
        if i not in vertices1 + vertices2:
            if len(vertices1) % 2 != 0:
                best_vertex, best_position, _ = get_best_insertion(vertices1, vertices2, distance_matrix)
                vertices1.insert(best_position, best_vertex)
            else:
                best_vertex, best_position, _ = get_best_insertion(vertices2, vertices1, distance_matrix)
                vertices2.insert(best_position, best_vertex)

    return vertices1 + vertices1[:1], vertices2 + vertices2[:1]
