# coding: utf-8

from collections import deque
from itertools import combinations

inf = float("inf")

visited = deque()
s = dict()

# V = {"1", "2", "3", "4", "5", "6"}
#
# # Матрица последователей - P
# followers = [
#     [0, "2", "3", "4", 0, "6"],
#     ["1", 0, "3", "4", 0, 0],
#     ["1", "2", 0, "4", 0, "6"],
#     ["1", "2", "3", 0, "5", 0],
#     [0, 0, 0, "4", 0, "6"],
#     ["1", 0, "3", 0, "5", 0]
# ]
#
# # Матрица кратчайших расстояний - M
# paths = [
#     [0, 7, 9, 21, inf, 2],
#     [7, 0, 10, 15, inf, inf],
#     [9, 10, 0, 11, inf, 14],
#     [21, 15, 11, 0, 6, inf],
#     [inf, inf, inf, 6, 0, 9],
#     [2, inf, 14, inf, 9, 0]
# ]

# V = {"1", "2", "3", "4"}
# followers = [
#     [0, "2", "3", 0],
#     ["1", 0, "3", "4"],
#     ["1", "2", 0, "4"],
#     [0, "2", "3", 0]
# ]
#
# paths = [
#     [0, 2, 2, inf],
#     [2, 0, 3, 8],
#     [2, 3, 0, 4],
#     [inf, 8, 4, 0]
# ]

# V = {"1", "2", "3", "4", "5"}
# followers = [
#     [0, "2", 0, "4", "5"],
#     ["1", 0, "3", 0, 0],
#     [0, "2", 0, "4", "5"],
#     ["1", 0, "3", 0, 0],
#     ["1", 0, "3", 0, 0]
# ]
#
# paths = [
#     [  0,   3, inf,  10,   2],
#     [  3,   0,   4, inf, inf],
#     [inf,   4,   0,   2, 3],
#     [ 10, inf,   2, 0, inf],
#     [  2, inf,   3, inf, 0]
# ]
# Матрица вершин
V = {"0", "1", "2", "3", "4"}

# Матрица весов
paths = [
    [0, 1, inf, inf, 4],
    [1, 0, 5, 1, inf],
    [inf, 5, 0, 2, inf],
    [inf, 1, 2, 0, 1],
    [4, inf, inf, 1, 0]
]

# Матрица последователей
followers = [
    [0, "2", 0, 0, "5"],
    ["1", 0, "3", "4", 0],
    [0, "2", 0, "4", 0],
    [0, "2", "3", 0, "5"],
    ["1", 0, 0, "4", 0],
]


def print_matrix(mx):
    for row in mx:
        print(row)
    print()


def find_top_least():
    min_node = inf
    min_count = inf

    for i in range(len(followers)):
        n = str(i + 1)

        if n not in V:
            continue

        relations_count = 0
        for j in range(len(followers[i])):
            if j not in visited and followers[i][j] != 0:
                relations_count += 1

        print(
            f"Количество смежных с {i + 1} ({followers[i]}) = {relations_count}"
        )

        if relations_count < min_count:
            min_node = i
            min_count = relations_count

    return min_node


def find_related_nodes(in_node):
    if len(V) == 2:
        return list(V)

    return (
        node for node in followers[in_node]
        if node != 0 and node in V
    )


# ---- РАЗБОРКА ГРАФА ----

while len(V) > 2:
    top_least_node = find_top_least()
    visited.appendleft(top_least_node)

    V ^= {str(top_least_node + 1)}
    print(f"Удаляем вершину {top_least_node + 1}")
    print("V:", sorted(V))

    related_nodes = list(
        map(lambda x: int(x) - 1, find_related_nodes(top_least_node))
    )
    s[top_least_node] = related_nodes

    pairs = combinations(related_nodes, r=2)
    for i1, i2 in pairs:
        distance = paths[i1][top_least_node] + paths[i2][top_least_node]
        print(f"{i1 + 1} <-> {i2 + 1} = {distance}")

        # Если пути не существует
        # Или старый путь длиннее нового
        if paths[i1][i2] == inf or paths[i1][i2] > distance:
            print("Заменяем")

            followers[i1][i2] = str(top_least_node + 1)
            followers[i2][i1] = followers[i2][top_least_node]

            # followers[i2][i1] = str(top_least_node + 1)

            paths[i1][i2] = distance
            paths[i2][i1] = distance
        else:
            print("Ничего не меняем")

    print_matrix(followers)
    print_matrix(paths)

print("Разборка завершена")
print("----")
print()

# ---- СБОРКА ГРАФА ----
print("----")
print("Сборка")
print()

while visited:
    new_node = visited.popleft()
    print(f"Добавляем вершину: {new_node + 1}")
    print(f"Смежные с ней: {s[new_node]}")

    # Идем по всем доступным вершинам
    for node in map(lambda x: int(x) - 1, V):
        old_distance = paths[new_node][node]

        print(f"{new_node + 1} <-> {node + 1}: {old_distance}")

        # А вот тут уже идем по смежным
        min_dist_2 = inf
        min_node_2 = None
        for related in s[new_node]:
            if related == node:
                continue

            distance_2 = paths[new_node][related] + paths[related][node]
            print(f"({new_node + 1} <-> {related + 1}) + "
                  f"({related + 1} <-> {node + 1}): {distance_2}")

            if distance_2 < min_dist_2:
                min_dist_2 = distance_2
                min_node_2 = related

        if min_dist_2 < old_distance:
            print(f"Меняем на {min_dist_2} с вершиной {min_node_2 + 1}")
            paths[new_node][node] = min_dist_2
            paths[node][new_node] = min_dist_2

            followers[new_node][node] = str(min_node_2 + 1)
            followers[node][new_node] = followers[node][min_node_2]

    print()
    print_matrix(followers)
    print_matrix(paths)

    V.add(str(new_node + 1))

    # input()

print("Сборка завершена")
print()


# ----
# ИТОГ

def find_lower_path(_from: str, _to: str):
    start = int(_from) - 1
    end = int(_to) - 1
    follower = followers[end][start]

    result = [_to, ]
    while follower:
        result.append(follower)
        new_end = int(follower) - 1
        follower = followers[new_end][start]
        # print(new_end)

    return result[::-1]


print("Пример: кратчайшие пути от первой вершины до всех остальных")
v0 = 1
for i in range(len(paths[v0])):
    if i == v0:
        continue

    path = paths[v0][i]

    route = " -> ".join(find_lower_path(str(v0 + 1), str(i + 1)))
    print(f"{v0 + 1} -> {i + 1}: {path:>2} ({route})")
