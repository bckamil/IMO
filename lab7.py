import copy
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import time  
from statistics import mean

S=30 #Population passing selection
M=4 #Mutation probability
A=100 #Epochs
T=20 #Elite
P=50 #Population

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


def get_second_vertex(first_vertex, distance_matrix):
    max_distance = max(distance_matrix[first_vertex])
    return distance_matrix[first_vertex].index(max_distance)



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


def selection(population):
    return np.random.choice(population, size=S, replace=False)

def mutation(solution):
    vs1 = solution.v1[0]
    vs2 = solution.v2[0]
    vertices1 = []
    vertices2 = []
    for i in range(random.randint(20, 70))
        vertices1.appendsolution.v1[i]
        vertices2.appendsolution.v2[i]
    for i in range(99-len(vertices1)):
        v1,v2 = insert(vertices1,vertices2,distance_matrix)
        vertices1.append(v1)
        vertices2.append(v2)
    vertices1.append(vs1)
    vertices2.append(vs2)
    score = calculate_score(vertices1, distance_matrix, cycle=True) + calculate_score(vertices2, distance_matrix, cycle=True)
    #print(vertices1)
    #print(vertices2)
    #print(score)
    #plot(ins,vertices1,vertices2)
    return vertices1,vertices2,score

def get_best_insertion_cross(vertices, vertices2, distance_matrix, position=True, cycle=False):
    best_vertex = None
    best_score = None
    best_position = None

    for i in vertices2:
        for position in range(len(vertices) + 1):
            temp_vertices = copy.copy(vertices)
            temp_vertices.insert(position, i)
            score = calculate_score(temp_vertices, distance_matrix, cycle=True)
            if best_score is None or score < best_score:
                best_score = score
                best_vertex = i
                best_position = position

    return best_vertex, best_position, best_score

def cross(parent1,p2,distance_matrix):
    parent2 = copy.deepcopy(p2)
    deleted_1 = []
    deleted_2 = []
    for v in parent1.v1:
        if v not in parent2.v1 and v != parent2.v1[0] and v != parent1.v1[0] and v != parent2.v2[0] and v != parent1.v2[0]:
            parent2.v1.remove(v)
            deleted_1.append(v)
    for v in parent1.v2:
        if v not in parent2.v2 and v != parent2.v2[0] and v != parent1.v2[0] and v != parent2.v1[0] and v != parent1.v1[0]:
            parent2.v2.remove(v)
            deleted_2.append(v)
    for k in deleted_1:
        best_vertex, best_position, _ = get_best_insertion_cross(parent2.v1, [k], distance_matrix)
        if best_position==0:
            best_position+=1
        parent2.v1.insert(best_position, best_vertex)
    for k in deleted_2:
        best_vertex, best_position, _ = get_best_insertion_cross(parent2.v2, [k], distance_matrix)
        if best_position==0:
            best_position+=1
        parent2.v2.insert(best_position, best_vertex)
    parent2.score = calculate_score(parent2.v1,distance_matrix) + calculate_score(parent2.v2,distance_matrix)
    return parent2    


class Solution:
    def __init__(self, v1, v2, score):
        self.v1 = v1
        self.v2 = v2
        self.score = score
