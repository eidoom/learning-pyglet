from functools import reduce
from math import sqrt
from operator import mul


def product(numbers):
    return reduce(mul, numbers)


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def vector_magnitude(vector):
    return sqrt(sum([x ** 2 for x in vector]))


def angle_between_vectors(*vectors):
    return sum([x1 * x2 for x1, x2 in zip(*vectors)]) / product([vector_magnitude(vector) for vector in vectors])


def add_vectors(*vectors):
    return [x1 + x2 for x1, x2 in zip(*vectors)]
