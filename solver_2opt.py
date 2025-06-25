#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_tour

class Point:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

class Intersection:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def f(self, p1, p2, p3):
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

    def has_intersection(self):
        print(self.p1.index, self.p2.index, self.p3.index, self.p4.index)
        t1 = self.f(self.p1, self.p2, self.p3)
        t2 = self.f(self.p1, self.p2, self.p4)
        t3 = self.f(self.p3, self.p4, self.p1)
        t4 = self.f(self.p3, self.p4, self.p2)
        return t1 * t2 < 0.0 and t3 * t4 < 0.0


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def change_order(order1, order2, order3, order4, tour):
    for i in range(int((order3 - order2) / 2) + 1):
        temp = tour[order2 + i]
        tour[order2 + i] = tour[order3 - i]
        tour[order3 - i] = temp
    print(tour)

def untie(tour, dist, point_sets, order_dict):

    # within the paths, get four points that have an intersection
    for i in range(len(point_sets) - 1):
        for j in range(i + 1, len(point_sets)):
            p1 = point_sets[i][0]
            p2 = point_sets[i][1]
            p3 = point_sets[j][0]
            p4 = point_sets[j][1]
            intersection = Intersection(p1, p2, p3, p4)
            if intersection.has_intersection():
                print("order")
                change_order(order_dict[p1.index], order_dict[p2.index], order_dict[p3.index], order_dict[p4.index], tour)

def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]
    order_dict = {}
    order_dict[current_city] = 0
    point_sets = []

    # visit the closes city that has not been visited
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        order_dict[next_city] = order_dict[current_city] + 1
        point_sets.append((Point(cities[current_city][0], cities[current_city][1], current_city), Point(cities[next_city][0], cities[next_city][1], next_city)))
        current_city = next_city

    print(order_dict)
    # add last set of two points
    point_sets.append((Point(cities[current_city][0], cities[current_city][1], current_city), Point(cities[0][0], cities[0][1], 0)))
    untie(tour, dist, point_sets, order_dict)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 2
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    write_tour(tour, sys.argv[2])
