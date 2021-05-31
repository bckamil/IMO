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
P=100 #Population

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
    rand = random.randint(0, 100)
    if(rand<50):
        x_id = random.randint(1, len(solution.v1)-1)
        y_id = random.randint(1, len(solution.v1)-1)
        temp = solution.v1[x_id]
        solution.v1[x_id] = solution.v1[y_id]
        solution.v1[y_id] = temp
    else:
        x_id = random.randint(1, len(solution.v2)-1)
        y_id = random.randint(1, len(solution.v2)-1)
        temp = solution.v2[x_id]
        solution.v2[x_id] = solution.v2[y_id]
        solution.v2[y_id] = temp
    return solution

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
        if v in parent2.v1 and v != parent2.v1[0] and v != parent1.v1[0] and v != parent2.v2[0] and v != parent1.v2[0]:
            parent2.v1.remove(v)
            deleted_1.append(v)
    for v in parent1.v2:
        if v in parent2.v2 and v != parent2.v2[0] and v != parent1.v2[0] and v != parent2.v1[0] and v != parent1.v1[0]:
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


def myFunc(solution):
    return solution.score


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


def main():
    instance = load_instance("kroA100.tsp")
    distance_matrix = create_distance_matrix(instance)
    answer = []
    population = []
    for i in range(100):
        x,y = greedy_cycle(distance_matrix, i)
        score = calculate_score(x,distance_matrix) + calculate_score(y,distance_matrix)
        s = Solution(x,y,score)
        population.append(copy.deepcopy(s))
    population.sort(key=myFunc)
    cross(population[0],population[1],distance_matrix)
    for i in range(A):
        population.sort(key=myFunc)
        new_population = []
        for i in range(T):
            new_population.append(copy.deepcopy(population[i]))
        for i in range(T):
            population.remove(population[0])
        selected = selection(population)
        for i in range(len(selected)):
            new_population.append(selected[i])
        while(len(new_population)!=P):
            p1= random.randint(0, 49)
            p2 = random.randint(0, 49)
            while(p2==p1):
                p2 = random.randint(0, 49)
            child = cross(new_population[p1],new_population[p2],distance_matrix)
            new_population.append(child)
        for i in range(20,P):
            rand = random.randint(0, 100)
            if(rand<M):
                new = mutation(new_population[i])
                new.score = calculate_score(new.v1,distance_matrix) + calculate_score(new.v2,distance_matrix)
                new_population[i] = copy.deepcopy(new)
        population = new_population
    population.sort(key=myFunc)
    answer.sort(key=myFunc)
    plot(instance,population[0].v1,population[0].v2)

    
if __name__ == "__main__":
    main()
