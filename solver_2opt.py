#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_tour

class City:
    """
    The City class represents basic information about an animal.

    Attributes:
        x (int): The x-coordinate of the city's location.
        y (int): The y-coordinate of the city's location.
        name (string): The name of the city
    """
    def __init__(self, city, name):
        self.x = city[0]
        self.y = city[1]
        self.name = name

class Intersection:
    """
    The Intersection class determines whether two line segments intersect.
    Each point should be an instance of the City class, which contains:
        - x (int or float): x-coordinate
        - y (int or float): y-coordinate
        - name (str): name of the city
    """
    def __init__(self, p1: 'City', p2: 'City', p3: 'City', p4: 'City'):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def is_above_line(self, p1, p2, p3):
        """
        Helper function to determine the relative position of point p3
        related to directed line from p1 to p2.
        Returns:
            > 0 if p3 is to the left of the line (p1 → p2)
            < 0 if p3 is to the right of the line (p1 → p2)
            = 0 if p3 is on the line
        """
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

    def has_intersection(self):
        """
        Determines whether the two line (p1-p2 and p3-p4) has an intersection.
        Uses the cross product method (also known as the counter-clockwise test).
        Returns True if 4 points has an intersection, returns False if not.

        The idea:
        - t1 and t2 check whether p3 and p4 lie on opposite sides of the line p1 → p2
        - t3 and t4 check whether p1 and p2 lie on opposite sides of the line p3 → p4
        If both pairs of points are on opposite sides, the segments intersect.
        """
        t1 = self.is_above_line(self.p1, self.p2, self.p3)
        t2 = self.is_above_line(self.p1, self.p2, self.p4)
        t3 = self.is_above_line(self.p3, self.p4, self.p1)
        t4 = self.is_above_line(self.p3, self.p4, self.p2)
        return t1 * t2 < 0.0 and t3 * t4 < 0.0

class Path:
    """
    The Path class manages a tour (a sequence of city visits) and helps detect and resolve
    paths that has intersections in the tour using 2-opt heuristics.

    Attributes:
        tour (list[int]): List of city indices representing the visit order.
        cities (list[(float, float)]): List of tuples of x and y of the cities
        num_cities (int): Number of cities in the current tour.
        order_dict (dict): Maps city name to its position in the tour.
        lines (list[tuple[City, City]]): Line representing paths between cities next to each other.
    """

    def __init__(self, tour, cities):
        self.num_cities = len(tour)
        self.tour = tour
        self.cities = cities
        self.order_dict = self.update_order_dict()
        self.lines = self.update_lines()


    def add_new_city(self, city):
        """
        Adds a new city to the end of the current tour and updates order of the new city and the nums of city.
        """
        self.lines.append((City(self.cities[self.tour[-1]], self.tour[-1]), City(self.cities[city], city)))
        self.tour.append(city)
        self.order_dict[city] = len(self.tour) - 1
        self.num_cities += 1

    def untie(self):
        """
        Detects and resolves a single intersection between the last added line and any previous line.
        Uses Intersection class to check for crossing segments.
        Return true if it has an intersection, if not returns False
        """
        for i in range(len(self.lines) - 1):
            p1 = self.lines[i][0]
            p2 = self.lines[i][1]
            p3 = self.lines[-1][0]
            p4 = self.lines[-1][1]
            intersection = Intersection(p1, p2, p3, p4)

            # if this combination has an intersection, change the order of tour and update lines and order of the cities.
            if intersection.has_intersection():
                self.change_tour(p1, p2, p3, p4)
                self.lines = self.update_lines()
                self.order_dict = self.update_order_dict()
                self.show_lines()
                return True
        return False

    def whole_untie(self):
        """
        Checks for intersections between all pairs of line segments and resolves the first one found.
        Returns True if a change was made, otherwise False.
        """

        # check all the combination of paths and check whether they have intersections.
        # if so, untie it
        for i in range(len(self.lines) - 1):
            for j in range(i + 1, len(self.lines)):
                p1 = self.lines[i][0]
                p2 = self.lines[i][1]
                p3 = self.lines[j][0]
                p4 = self.lines[j][1]
                intersection = Intersection(p1, p2, p3, p4)
                if intersection.has_intersection():
                    self.change_tour(p1, p2, p3, p4)
                    self.lines = self.update_lines()
                    self.order_dict = self.update_order_dict()
                    self.show_lines()
                    return True
        return False

    def update_order_dict(self):
        """
        Update the order of the cities in the current tour.
        Returns the dictionary of order of them.
        """
        order_dict = {}
        for i in range(self.num_cities):
            order_dict[self.tour[i]] = i
        return order_dict

    def update_lines(self):
        """
        Update the lines.

        Returns:
            A list of tuples of two City object that represents the updated path.
        """
        lines = []
        for i in range(self.num_cities - 1):
            current_city = self.cities[self.tour[i]]
            next_city = self.cities[self.tour[i+1]]
            lines.append((City(current_city, self.tour[i]), City(next_city, self.tour[i + 1])))

        return lines

    def show_lines(self):
        """
        Print the current lines.
        """
        for i in range(len(self.lines)):
            print(self.lines[i][0].name, self.lines[i][1].name)

    def get_lines(self):
        """
        Get the current lines.
        A list of tuples of two City object that represents the updated path.
        """
        return self.lines

    def change_tour(self, p1, p2, p3, p4):
        """
        Reverses the sub-path between p2 and p3 to solve an intersection.
        This is similar to the 2-opt technique used in TSP solvers.

        Args:
            p1, p2: Endpoints of the first intersecting line segment.
            p3, p4: Endpoints of the second intersecting line segment.

        """
        order1 = self.order_dict[p1.name]
        order2 = self.order_dict[p2.name]
        order3 = self.order_dict[p3.name]
        order4 = self.order_dict[p4.name]

        for i in range(int((order3 - order2) / 2) + 1):
            temp = self.tour[order2 + i]
            self.tour[order2 + i] = self.tour[order3 - i]
            self.tour[order3 - i] = temp

    def get_tour(self):
        """
        Returns the tour without the last city (assuming it might be a return-to-start point).
        """
        return self.tour[:-1]



def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def solve(cities):
    N = len(cities)

    # すべての都市同士の距離を測る
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    # current_cityに最初の出発都市を追加し、まだ訪問していない都市を全てに設定する
    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    # pathのクラスを用意する
    path = Path(tour, cities)

    # まだ訪問されていない都市を訪問する
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)

        # pathクラスにnext_cityを追加する
        path.add_new_city(next_city)

        # 追加したnext_cityによって得られたパスに交点があったら解く
        path.untie()
        current_city = next_city

    # 最初のcityを追加して、最後のパスに交点があったら解く
    path.add_new_city(0)
    path.untie()

    #　最後にループで回して、すべての交点を解くようにする
    has_circle = True
    while True:
        has_circle = path.whole_untie()
        if has_circle == False:
            break

    return path.get_tour()


if __name__ == '__main__':
    assert len(sys.argv) > 2
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    write_tour(tour, sys.argv[2])
