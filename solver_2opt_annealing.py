#!/usr/bin/env python3

import sys
import math
import random
import time

from common import print_tour, read_input, write_tour

TIMES = 10000

def get_total_distance(tour, dist):
  total = 0
  for i in range(len(tour) - 1):
    total += dist[tour[i]][tour[i+1]]
  return total


def swap(tour, N):
  i, j = random.sample(range(1, N), 2)
  start = min(i, j)
  end = max(i, j)
  reversed_tour = list(reversed(tour[start: end + 1]))
  tour = tour[: start] + reversed_tour + tour[end + 1:]

  return tour

def annealing(tour, dist, p, N):
  current_tour = tour
  swapped_tour = swap(tour, N)
  current_dist = get_total_distance(current_tour, dist)
  swapped_dist = get_total_distance(swapped_tour, dist)

  if current_dist > swapped_dist:
    return swapped_tour
  elif random.random() < p:
    return swapped_tour
  else:
    return current_tour

def greedy(dist, start_city, N):
  current_city = start_city
  unvisited_cities = {i for i in range(N) if i != 0}
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

  return tour

def solve(cities):
    N = len(cities)

    # すべての都市同士の距離を測る
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    # start_cityを変えてベストスコアを出してみる
    # best_tourとshortest_distanceに0からスタートした場合の値を入れる
    for i in range(0, N):
      tour = greedy(dist, i, N)

      # opt2では二つのペアの点にもし結び目があれば点をswapして解いてより短い距離になるというアルゴリズムを使うが、
      # 結び目がない場合だと、swapすると逆に長くなってしまう
      # opt2でより長い経路を選ぶ確率をpとすると、100回のうち、最初の方はpが高く、後の方につれpが減っていき、
      # より短い経路を選ぶようになるようにする。
      start_time = time.time()
      time_limit = 20 * 60  # 20分 = 1200秒

      j = 0  # ステップカウント
      p_first = 1.0
      p_end = 0.0

      shortest_distance = float('inf')
      best_tour = tour.copy()

      while True:
          elapsed = time.time() - start_time
          if elapsed > time_limit:
              break

          # 時間に基づく温度（確率p）更新
          t = elapsed / time_limit  # 0.0 ~ 1.0 に正規化
          p = math.exp(-5 * t)

          # 焼きなましステップ
          tour = annealing(tour, dist, p, N)

          # 結果が良ければ保存
          total_dist = get_total_distance(tour, dist)
          if total_dist < shortest_distance:
              print(f"Step {j}, p={p:.5f}, dist={total_dist:.2f}")
              shortest_distance = total_dist
              best_tour = tour.copy()

          j += 1

      print(f"\nBest distance after 20 minutes: {get_total_distance(best_tour, dist)}")
      return best_tour

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

if __name__ == '__main__':
    assert len(sys.argv) > 2
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    write_tour(tour, sys.argv[2])
