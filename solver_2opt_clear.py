#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_tour

def get_total_distance(tour, dist):
  total = 0
  for i in range(len(tour) - 1):
    total += dist[tour[i]][tour[i+1]]
  return total

def opt2(tour: list[int], dist: list[list[float]]) -> bool:
  improved = False
  for i in range(len(tour) - 2):
    for j in range(i + 2, len(tour) - 1):
      a, b = tour[i], tour[i + 1]
      c, d = tour[j], tour[j + 1]

      # 結び目を発見した場合、解く(2opt)
      if dist[a][b] + dist[c][d] > dist[a][c] + dist[b][d]:
        reversed_tour = list(reversed(tour[i + 1: j + 1]))
        tour = tour[: i + 1] + reversed_tour + tour[j + 1:]
        improved = True

  return improved, tour

def greedy_and_opt2(cities, dist, start_city):
    N = len(cities)

    # greedyで訪問したことない年の中で一番近い都市を次に持ってくる
    # current_cityに最初の出発都市を追加し、まだ訪問していない都市を全てに設定する
    current_city = start_city
    unvisited_cities = {i for i in range(N) if i != start_city}
    tour = [current_city]

    # まだ訪問されていない都市を訪問する
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)

        # tourにnext_cityを追加する
        tour.append(next_city)
        current_city = next_city

    # 最初のcityを追加
    tour.append(start_city)

    # すべての結び目を解く
    improved = True
    while improved:
      improved, tour = opt2(tour, dist)

    return tour

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def solve(cities):
    N = len(cities)

    # すべての都市同士の距離を測る
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    # start_cityを変えてベストスコアを出してみる
    # best_tourとshortest_distanceに0からスタートした場合の値を入れる
    tour_start_from_0 = greedy_and_opt2(cities, dist, 0)
    shortest_distance = get_total_distance(tour_start_from_0, dist)
    best_tour = tour_start_from_0.copy()

    # start_cityを1からN-1まで変え、一番良いものをとってくる
    for i in range(1, N):
      print(i)
      start_city = i
      tour = greedy_and_opt2(cities, dist, start_city)
      total_dist = get_total_distance(tour, dist)
      if total_dist < shortest_distance:
        shortest_distance = total_dist
        best_tour = tour.copy()

    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 2
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    write_tour(tour, sys.argv[2])
