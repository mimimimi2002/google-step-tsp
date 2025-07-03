#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, write_tour

def get_total_distance(tour, dist):
  total = 0
  for i in range(len(tour) - 1):
    total += dist[tour[i]][tour[i+1]]
  return total

def or_1_opt(tour: list[int], dist: list[list[float]]) -> bool:
  improved = False
  for i in range(len(tour) - 3):
    for j in range(i + 3, len(tour) - 1):
      a, b, c = tour[i], tour[i + 1], tour[i + 2]
      d, e = tour[j], tour[j + 1]

      # もしbがac間ではなくde間にある場合の方が短いとき
      if dist[a][b] + dist[b][c] +  dist[d][e] >  dist[a][c] + dist[d][b] + dist[b][e]:
        improved = True
        tour = tour[: i + 1] + tour[i + 2: j + 1] + [b] + tour[j + 1: ]

  return improved, tour

def or_2_opt(tour: list[int], dist: list[list[float]]) -> bool:
  improved = False
  for i in range(len(tour) - 4):
    for j in range(i + 4, len(tour) - 1):
      a, b, c, d = tour[i], tour[i + 1], tour[i + 2], tour[i + 3]
      e, f = tour[j], tour[j + 1]

      # もしbがac間ではなくde間にある場合の方が短いとき
      if dist[a][b] + dist[c][d] + dist[e][f] >  dist[a][d] + dist[e][b] + dist[c][f]:
        improved = True
        tour = tour[: i + 1] + tour[i + 3: j + 1] + [b, c] + tour[j + 1: ]

  return improved, tour

def opt2(tour: list[int], dist: list[list[float]]) -> bool:
  improved = False
  for i in range(len(tour) - 2):
    for j in range(i + 2, len(tour) - 1):
      a, b = tour[i], tour[i + 1]
      c, d = tour[j], tour[j + 1]

      # 結び目を発見した場合
      if dist[a][b] + dist[c][d] > dist[a][c] + dist[b][d]:
        reversed_tour = list(reversed(tour[i + 1: j + 1]))
        tour = tour[: i + 1] + reversed_tour + tour[j + 1:]
        improved = True

  return improved, tour

def greedy_and_opt2_or_1_opt_or_2_opt(cities, dist, start_city):
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

    # すべての結び目を解く(2opt)
    improved = True
    while improved:
      improved, tour = opt2(tour, dist)

    # or_1_opt, もしある点が別の二つの点の間にある場合に経路が短くなるならそっちにする
    improved = True
    while improved:
      improved, tour = or_1_opt(tour, dist)

    # or_2_opt, もしある隣同士の二つの点が別の二つの点に間にある場合に経路が短くなったらそっちにする
    improved = True
    while improved:
      improved, tour = or_2_opt(tour, dist)
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

    # start_cityを1からN-1まで変え、一番良いものをとってくる
    shortest_distance = float('inf')
    best_tour = [0, 0]

    for i in range(0, N):
      start_city = i
      tour = greedy_and_opt2_or_1_opt_or_2_opt(cities, dist, start_city)
      total_dist = get_total_distance(tour, dist)
      print(i, total_dist)
      if total_dist < shortest_distance:
        shortest_distance = total_dist
        best_tour = tour.copy()

    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 2
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    write_tour(tour, sys.argv[2])
