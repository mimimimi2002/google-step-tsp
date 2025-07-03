#!/usr/bin/env python3

import sys
import math
import random
import time

from common import print_tour, read_input, write_tour

TIMES = 10000

# 都市番号のリストが与えられたときにそれらを最初から繋ぎ合わせた時の総合距離を返す
# |tour|: list[int] 都市番号ののリスト
# |dist|: list[list[float]]　都市同士の距離が入った二次元リスト
def get_total_distance(tour: list[int], dist: list[list[float]]) -> float:
  total = 0
  for i in range(len(tour) - 1):
    total += dist[tour[i]][tour[i+1]]
  return total

# 現在の都市番号リストから適当に二つの都市を選んで順番を交換し、そのリストを返す
# |tour|: list[int] 都市番号ののリスト
# N: 都市の数
def swap(tour: list[int], N: int) -> list[int]:
  i, j = random.sample(range(1, N), 2)
  start = min(i, j)
  end = max(i, j)

  reversed_tour = list(reversed(tour[start: end + 1]))
  if start == 0:
    tour = reversed_tour + tour[end + 1: -1] + [reversed_tour[0]]
  else:
    tour = tour[: start] + reversed_tour + tour[end + 1:]
  return tour

# 焼きなまし法、swap関数を呼び出したときに元の都市リストの総合距離より小さければ、swapされたリストを返す
# swapした後総合距離が長くなったらpの確率でswapしたリストを返す、それ以外はswapしてないリストが返される
# |tour|: list[int] 都市番号ののリスト
# |dist|: list[list[float]]　都市同士の距離が入った二次元リスト
# |p|: float swapしたリストの方が距離が長くなった場合にswapリストを返す確率
# |N|: 都市の数
def annealing(tour: list[int], dist: list[list[float]], p: float, N: int) -> list[int]:
  current_tour = tour
  swapped_tour = swap(tour, N)
  current_dist = get_total_distance(current_tour, dist)
  swapped_dist = get_total_distance(swapped_tour, dist)

  # もしswapの結果が必ず良ければswapしたものを返し
  if current_dist > swapped_dist:
    return swapped_tour

  # そうでなければpの確率でswapしたものを返す
  elif random.random() < p:
    return swapped_tour
  else:
    return current_tour

# 貪欲法で訪問したことない年の中で一番近い都市を次に訪問し、そのリストを返す
# |dist|: list[list[float]]　都市同士の距離が入った二次元リスト
# |start_city|: int 最初に訪問する都市番号
# |N|: 都市の数
def greedy(dist: list[list[float]], start_city: int, N: int) -> list[int]:
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

# ランダムな都市のリストを返す
# |N|: 都市の数
def random_tour(N: int) -> list[int]:
  tour = [i for i in range(N)]
  random.shuffle(tour)
  tour.append(tour[0])
  return tour

# opt2のアルゴリズムで受け取った都市リストを最適化し、もし結び目があったらTrueと都市リストを返す
# なかったらFlaseと都市リストを返す
# 二組の辺が交差していたら解くアルゴリズム
# |tour|: list[int] 都市番号ののリスト
# |dist|: list[list[float]]　都市同士の距離が入った二次元リスト
def opt2(tour: list[int], dist: list[list[float]]) -> tuple[bool, list[int]]:
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

# or_1_optのアルゴリズムで受け取った都市リストを最適化し、もし効率よくできたらTrueと都市リストを返す
# できなかったらFalseと都市リストを返す
# a->b->c d->e => a->c d->b->eの方が効率的であるなら入れ替えるアルゴリズム
# |tour|: list[int] 都市番号ののリスト
# |dist|: list[list[float]]　都市同士の距離が入った二次元リスト
def or_1_opt(tour: list[int], dist: list[list[float]]) -> tuple[bool, list[int]]:
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

# or_2_optのアルゴリズムで受け取った都市リストを最適化し、もし効率よくできたらTrueと都市リストを返す
# できなかったらFalseと都市リストを返す
# a->b->c->d e->f => a->d e->b->c->fの方が効率的であるなら入れ替えるアルゴリズム
# |tour|: list[int] 都市番号ののリスト
# |dist|: list[list[float]]　都市同士の距離が入った二次元リスト
def or_2_opt(tour: list[int], dist: list[list[float]]) -> tuple[bool, list[int]]:
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

# 1番良い都市リストを返す関数
# |cities|: list[list[float]]: それぞれの都市番号のリストにx座標とy座標を入れたリスト
def solve(cities: list[list[float]]) -> list[int]:
    N = len(cities)

    # すべての都市同士の距離を測る
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    # start_cityを変えてベストスコアを出してみる
    # best_tourとshortest_distanceに0からスタートした場合の値を入れる
    # tour = greedy(dist, i, N)
    tour = random_tour(N)

    # opt2では二つのペアの点にもし結び目があれば点をswapして解いてより短い距離になるというアルゴリズムを使うが、
    # 結び目がない場合だと、swapすると逆に長くなってしまう
    # opt2でより長い経路を選ぶ確率をpとすると、100回のうち、最初の方はpが高く、後の方につれpが減っていき、
    # より短い経路を選ぶようになるようにする。
    true_start_time = time.time()
    start_time = time.time()
    time_limit = 60 * 60  # 60分

    j = 0  # ステップカウント

    shortest_distance_after_opt = float('inf')
    best_tour = tour.copy()

    while True:
        elapsed = time.time() - start_time

        # ここでbreakさせないので、無限ループになります
        # if (time.time() - true_start_time) > time_limit:
        #     break

        # 時間に基づく温度（確率p）更新
        t = elapsed / time_limit  # 0.0 ~ 1.0 に正規化
        p = math.exp(-5 * t)

        # 焼きなましステップ
        tour = annealing(tour, dist, p, N)

        # 結果
        total_dist = get_total_distance(tour, dist)

        # 出てきたtourをopt2とor_1_optとor_2_optしてみる
        opt_tour = tour.copy()

        # opt2
        improved = True
        while improved:
          improved, opt_tour = opt2(opt_tour, dist)

        # or_1_opt
        improved = True
        while improved:
          improved, opt_tour = or_1_opt(opt_tour, dist)

        # or_2_opt
        improved = True
        while improved:
          improved, opt_tour = or_2_opt(opt_tour, dist)
        total_dist_after_opt = get_total_distance(opt_tour, dist)

        # もしpが0.1を下回ったらもう一度tourをシャッフルし、pも1からスタートします
        if p < 0.1:
          print("shuffle")
          start_time = time.time()
          tour = random_tour(N)
          shortest_distance_after_opt = float('inf')

        # もしより良いpathが見つかったら、記録
        if total_dist_after_opt < shortest_distance_after_opt:
          shortest_distance_after_opt = total_dist_after_opt
          print(j, p, total_dist_after_opt)
          best_tour = opt_tour.copy()
          write_tour(best_tour, sys.argv[2])

        j += 1

    print(f"\nBest distance after 20 minutes: {get_total_distance(best_tour, dist)}")
    return best_tour

# 二つの都市間の距離を返す関数
# |city1| :int 都市番号
# |city2| :int 都市番号
def distance(city1: int, city2: int) -> float:
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

if __name__ == '__main__':
    assert len(sys.argv) > 2
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    write_tour(tour, sys.argv[2])
