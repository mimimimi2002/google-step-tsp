# googleSTEP

## File Descriptions

| File name             | Usage                                            | Command |
|-----------------------|--------------------------------------------------|---------|
| solver_2opt_original.py            | TSP using original 2 opt                        |python solver_2opt_original.py input_file output_file|
| solver_2opt.py                     | TSP using 2 opt                                 |python solver_2opt.py input_file output_file|
| solver_greedy_2_opt_or_1_opt.py    | TSP using greedy and 2 opt and or_1_opt         |python solver_greedy_2_opt_or_1_opt.py input_file output_file|
| solver_greedy_2_opt_or_1_opt_or_2_opt.py | TSP using greedy and 2 opt and or_1opt and or_2_opt                             |python solver_greedy_2_opt_or_1_opt_or_2_opt.py input_file output_file|
| solver_annealing.py               | TSP using annealing and 2 opt and or_1opt and or_2_opt                             |python solver_annealing.py input_file output_file|


# Homework
## Overview
Find the shorter path that visit all the cities and return to the first city.

## Algorithm
### Origianl opt2
Utilize opt-2 algorithm to detect the intersection in the path and untie it to make the path shorter.

1. Add new city to the current path.

2. If the new path has an intersection with any previous path, untie it.

3. Iterate it until the end, and considering that the path still has intersections, untie it until it has no circle in the path.

#### Structure
To make the code more easy to read, we utilized several class object to assign different role for each class.

1. City class

Represents the city and has attributes of x coordinate and y coordinate of the position and its name.

2. Intersection class

Responsible to judge whether two lines that are made of four City classes have an intersection.

3. Path class

Represents the current path and responsible to update the path and untie it if necessary.

### opt2
The opt2 I provided in previous sectino had a complicated structure, so after the coding review with the team member, I found that there is a simple algorithm that can achieve opt2

#### Structure
After getting the list of cities in a greedy way(get the next city that is the nearest from the current city), get the different 2 edges (a->b and c->d) and it swap the path between a and d
( ex: a->b->e->f->c->d => a->c->f->e->b->d) which basically means to **un tie the knot**.

So what we need to do in the algorithm is that `if dist[a][b] + dist[c][d] > dist[a][c] + dist[b][d]`
then un tie the knot.

We will continue this process until all the knots in the path has been un tied.

Then we change the start city and see which has the bset score.

### opt2 + or_1_opt
After using opt2 to optimize the path, we used or_1_opt algorithm to make it even more optimized.

Or_1_opt algothim means that to get a certain city and insert it between the differnt edge.
For example, a->b->c d->e => a->c d->b->e. In this way, we will optimize the situation where if b is closer to the other edge and can be optimized.

So what we need to do in the algorithm is that `if dist[a][b] + dist[b][c] +  dist[d][e] >  dist[a][c] + dist[d][b] + dist[b][e]`
then insert b to the middle of d and e.

Then we change the start city and see which has the bset score.

### opt2 + or_1_opt + or_2_opt
After using opt2 and or_1_opt to optimize the path, we used or_2_opt algorithm to make it even more optimized.

Or_2_opt algothim means that to get a pair of cities that is next to each other and insert them between the differnt edge. It is similar to or_1_opt idea, but this time we will move two cities at the same time.

For example, a->b->c->d e->f => a->d e->b->c->f. In this way, we will optimize the situation where if b is closer to the other edge and can be optimized.

So what we need to do in the algorithm is that `dist[a][b] + dist[c][d] + dist[e][f] >  dist[a][d] + dist[e][b] + dist[c][f]:`
then insert b and c to the middle of e and f.

Then we change the start city and see which has the bset score.

### Annealing
The algorithms that we provided has a week point in that, the optimized path can be stuck in the local optimal solution which means there might be better optmized path but because it started from a certain path and it never reaches to the better one.

Here is the graph that shows there are other global minimum answer but if you are caught in local answer.


This graph comes from https://www.researchgate.net/figure/Example-of-local-and-global-solutions-in-an-optimization-problem_fig3_322270023

To avoid this, we need to choose the worse path in a certain posibility so that it can reach to the global minimum answer.

To achieve this, we need to consider how to define p here. We first define how much time we spend to find one solution and based on the total time, we define p as it goes from 1 to closer to 0 using exponential function.

```
t = time_pased / time_limit  # 0.0 ~ 1.0 に正規化
p = math.exp(-5 * t)
```

In this way, we cannot guaranteed that we can find better answer, but it helps us not to be stuck in the local optimal answer.

#### Structure
1. Initialize the path in a random way

2. Swap random edges and if it is better than previous one, but if it is worse than previous one, return the worse one with the p possibility.

3. Do this until p gets lower than 0.1, if so, shuffle the tour again go back to 2.


## Results
| Algorithm         | N = 5 | N = 8     | N = 64 | N = 128   | N = 512    | N = 2048   | N = 8192|
|-------------------|-------|-------    |--------|---------  |---------   |----------  |---------|
2opt                |3291.62|3832.29    |4494.42 |8256.55    |10885.95    |20932.86    |41437.85|
2opt+or_1_opt       |3291.62|**3778.72**|4494.42 |8256.55    |10836.61    |**20822.26**|         |
2opt+or_1_opt_2_opt |3291.62|**3778.72**|4494.42 |8256.55    |10802.37    |**20822.26**|
annealing           |3291.62|**3778.72**|4494.42 |**8118.40**|**10530.55**|21102.054   |42773.13 |

## Conclusion
TSP is a NP problem which cannot be solved in algorithm with N^x order, but we have several algorithms to try to find optimized answers. Based on the results, I expect that annealing has the best score with all kinds of N, but it looks like depending on N, the algorithm that finds the shorter path varies.