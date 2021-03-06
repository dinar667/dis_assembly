# coding: utf-8

from collections import deque
from itertools import combinations

inf = float("inf")

visited = deque()
s = dict()

V = {"1", "2", "3", "4", "5", "6"}

# Матрица последователей - P
followers = [
    [0, 0, "3", "4", "5", "6"],
    [0, 0, 0, 0, 0, "6"],
    [0, "2", 0, 0, 0, 0],
    [0, "2", 0, 0, 0, 0],
    [0, 0, "3", "4", 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# Матрица кратчайших расстояний - M
paths = [
    [0, inf, 5, 5, 2, 12],
    [inf, 0, inf, inf, inf, 2],
    [inf, 2, 0, inf, inf, inf],
    [inf, 2, inf, 0, inf, inf],
    [inf, inf, 1, 2, 0, inf],
    [inf, inf, inf, inf, inf, 0],
]


#
# V = {"1", "2", "3", "4"}
#
# # Матрица последователей - P
# followers = [
#     [0, "2", "3", 0],
#     [0, 0, 0, "4"],
#     [0, "2", 0, "4"],
#     [0, 0, 0, 0],
# ]
#
# # Матрица кратчайших расстояний - M
# paths = [
#     [  0,   5,   3,  inf],
#     [inf,   0, inf,    2],
#     [inf,   2,   0,    1],
#     [inf, inf, inf,    0]
# ]


def print_matrix(mx):
    for row in mx:
        # print(f"{:>3}".join(map(str, row))
        print(" ".join("{:>3}".format(i) for i in map(str, row)))
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
            if followers[i][j] != 0 and followers[i][j] in V:
                relations_count += 1

        for j in range(len(followers)):
            if i == j or str(j + 1) not in V:
                continue
            for k in range(len(followers[j])):
                if followers[j][k] == n:
                    relations_count += 1

        # print(
        #     f"Количество смежных с {i + 1} ({followers[i]}) = {relations_count}"
        # )

        if relations_count < min_count and relations_count != 0:
            min_node = i
            min_count = relations_count

    return min_node


def find_related_nodes(in_node):
    if len(V) == 2:
        return list(V)

    result = set()
    for i in range(len(followers)):
        if i == in_node:
            continue
        for j in range(len(followers[i])):
            if followers[i][j] == str(in_node + 1):
                result.add(str(i + 1))

    for node in followers[in_node]:
        if node != 0 and node in V:
            result.add(node)

    return list(result)


def get_orelated_nodes(in_node):
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

    k = list(
        map(lambda x: int(x) - 1, find_related_nodes(top_least_node))
    )
    s[top_least_node] = sorted(k)
    print(f"Смежные с {top_least_node + 1} вершины: {s[top_least_node]}")

    related_nodes = sorted(list(
        map(lambda x: int(x) - 1, get_orelated_nodes(top_least_node))
    ))
    print(f"Из {top_least_node + 1} можно попасть в вершины: {related_nodes}")

    pairs = combinations(related_nodes, r=2)
    for i1, i2 in pairs:
        distance = paths[i1][top_least_node] + paths[i2][top_least_node]
        print(f"{i1 + 1} <-> {i2 + 1} = {distance}")

        # Если пути не существует
        # Или старый путь длиннее нового
        if paths[i1][i2] > distance:
            print("Заменяем")
            followers[i1][i2] = str(top_least_node + 1)
            paths[i1][i2] = distance
        else:
            print("Ничего не меняем")

    print_matrix(followers)
    print_matrix(paths)

print("Разборка завершена")
print("----")
print()
#
# # ---- СБОРКА ГРАФА ----
print("----")
print("Сборка")
print()

while visited:
    new_node = visited.popleft()
    print(f"Добавляем вершину: {new_node + 1}")
    print(f"Смежные с ней: {s[new_node]}")

    # Идем по всем доступным вершинам
    # ИЗ ВЕРШИНЫ ЧЕРЕЗ СМЕЖНУЮ
    print("Прямой путь")
    for node in sorted(map(lambda x: int(x) - 1, V)):
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
            print(
                f"Меняем на {min_dist_2} с вершиной \"{min_node_2 + 1}\" "
                f"({new_node + 1} -> {node + 1} = {min_dist_2})"
            )
            paths[new_node][node] = min_dist_2
            followers[new_node][node] = str(min_node_2 + 1)

    print("Обратный путь")
    # ИЗ СМЕЖНОЙ ЧЕРЕЗ ВЕРШИНУ
    for node in sorted(map(lambda x: int(x) - 1, V)):
        old_distance = paths[node][new_node]

        print(f"{node + 1} <-> {new_node + 1}: {old_distance}")

        # А вот тут уже идем по смежным
        min_dist_2 = inf
        min_node_2 = None
        for related in s[new_node]:
            if related == node:
                continue
            distance_2 = paths[node][related] + paths[related][new_node]
            print(f"({node + 1} <-> {related + 1}) + "
                  f"({related + 1} <-> {new_node + 1}): {distance_2}")

            if distance_2 < min_dist_2:
                min_dist_2 = distance_2
                min_node_2 = related

        if min_dist_2 < old_distance:
            print(
                f"Меняем на {min_dist_2} с вершиной \"{min_node_2 + 1}\" "
                f"({node + 1} -> {new_node + 1} = {min_dist_2})"
            )
            paths[node][new_node] = min_dist_2
            followers[node][new_node] = followers[node][
                min_node_2]  # str(min_node_2 + 1)

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

    follower = followers[start][end]

    result = [_from, ]
    while follower:
        result.append(follower)
        new_start = int(follower) - 1
        follower = followers[new_start][end]

    return result


print("Пример: кратчайшие пути от первой вершины до всех остальных")
v0 = 0
for i in range(len(paths[v0])):
    if i == v0:
        continue

    path = paths[v0][i]

    route = " -> ".join(find_lower_path(str(v0 + 1), str(i + 1)))
    print(f"{v0 + 1} -> {i + 1}: {path:>2} ({route})")
