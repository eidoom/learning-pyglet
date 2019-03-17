from functools import reduce
from math import sqrt, cos, sin, acos
from operator import mul


def rotation_matrix(angle):
    return ((cos(angle), -sin(angle)),
            (sin(angle), cos(angle)))


def product(numbers):
    return reduce(mul, numbers)


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the Euclidean distance between two points"""
    return sqrt(sum((point_1[i] - point_2[i]) ** 2 for i in range(len(point_1))))


def vector_magnitude(vector):
    return sqrt(sum(x ** 2 for x in vector))


def cos_angle_between_vectors(*vectors):
    return sum(x1 * x2 for x1, x2 in zip(*vectors)) / product([vector_magnitude(vector) for vector in vectors])


def angle_between_vectors(*vectors):
    return acos(cos_angle_between_vectors(*vectors))


def add_vectors(*vectors):
    return tuple(x1 + x2 for x1, x2 in zip(*vectors))


def matrix_times_vector(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(vector)))


def rotate_vector_by_angle(vector, angle):
    return matrix_times_vector(rotation_matrix(angle), vector)
