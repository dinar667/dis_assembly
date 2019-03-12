# coding: utf-8

from collections import deque
from itertools import combinations
from typing import List, Union, Set, Dict

inf = float("inf")


def print_matrix(mx):
    for row in mx:
        print(row)
    print()


class DisAssemblyAlgo:
    def __init__(self, v, followers, paths) -> None:

        self.v: Set[str] = v
        self.followers: List[List[Union[str, int]]] = followers
        self.paths: List[List[Union[int, float]]] = paths

        # Посещенные вершины
        self.visited: deque = deque()

        # Смежные вершины
        self.s: Dict[int, List[int]] = {}

    def find_top_least(self) -> Union[int, float]:
        """ Находит вершину наименьшей степени """

        min_node: Union[int, float] = inf
        min_count: Union[int, float] = inf

        for node in self.followers:

            n: str = str(self.followers.index(node) + 1)
            if n not in self.v:
                continue

            relations_count: int = len([
                follower for follower in node
                if follower != 0
            ])

            if relations_count < min_count:
                min_node = self.followers.index(node)
                min_count = relations_count

        return min_node

    def find_related_nodes(self, in_node: int):
        """ Находит смежные для вершины in_node вершины"""

        if len(self.v) == 2:
            return list(self.v)

        return (
            node for node in self.followers[in_node]
            if node != 0 and node in self.v
        )

    def disassembly(self) -> None:
        """ Разборка графа """

        while len(self.v) > 2:
            top_least_node = self.find_top_least()
            self.visited.appendleft(top_least_node)

            self.v ^= {str(top_least_node + 1)}
            print(f"Удаляем вершину {top_least_node + 1}")
            print("V:", sorted(self.v))

            related_nodes = list(
                map(
                    lambda x: int(x) - 1,
                    self.find_related_nodes(top_least_node)
                )
            )
            self.s[top_least_node] = related_nodes

            pairs = combinations(related_nodes, r=2)
            for i1, i2 in pairs:
                distance = self.paths[i1][top_least_node] \
                           + self.paths[i2][top_least_node]
                print(f"{i1 + 1} <-> {i2 + 1} = {distance}")

                # Если пути не существует
                # Или старый путь длиннее нового
                if self.paths[i1][i2] == inf or self.paths[i1][i2] > distance:
                    print("Заменяем")
                    self.followers[i1][i2] = str(top_least_node + 1)
                    self.followers[i2][i1] = str(top_least_node + 1)

                    self.paths[i1][i2] = distance
                    self.paths[i2][i1] = distance
                else:
                    print("Ничего не меняем")

            print_matrix(self.followers)
            print_matrix(self.paths)

    def assembly(self) -> None:
        """ Сборка графа """

        while self.visited:
            new_node = self.visited.popleft()
            print(f"Добавляем вершину: {new_node + 1}")
            print(f"Смежные с ней: {self.s[new_node]}")

            # Идем по всем доступным вершинам
            for node in map(lambda x: int(x) - 1, self.v):
                old_distance = self.paths[new_node][node]

                print(f"{new_node + 1} <-> {node + 1}: {old_distance}")

                # А вот тут уже идем по смежным
                min_dist_2 = inf
                min_node_2 = None
                for related in self.s[new_node]:
                    if related == node:
                        continue

                    distance_2 = \
                        self.paths[new_node][related] + \
                        self.paths[related][node]
                    print(f"({new_node + 1} <-> {related + 1}) + "
                          f"({related + 1} <-> {node + 1}): {distance_2}")

                    if distance_2 < min_dist_2:
                        min_dist_2 = distance_2
                        min_node_2 = related

                if min_dist_2 < old_distance:
                    print(f"Меняем на {min_dist_2} с вершиной {min_node_2 + 1}")
                    self.paths[new_node][node] = min_dist_2
                    self.paths[node][new_node] = min_dist_2

                    self.followers[new_node][node] = str(min_node_2 + 1)
                    self.followers[node][new_node] = str(min_node_2 + 1)

            print()
            print_matrix(self.followers)
            print_matrix(self.paths)

            self.v.add(str(new_node + 1))

    def get_lower_path(self, _from: str, _to: str) -> List[str]:
        """ Находит кратчайший путь между вершинами _from и _to """

        start = int(_from) - 1
        end = int(_to) - 1
        follower = self.followers[start][end]

        result: List[str] = [_from, follower]
        while follower != _to:
            new_from = follower
            start = int(new_from) - 1
            follower = self.followers[start][end]
            result.append(follower)

        return result

    def find_lower_paths(self) -> None:
        self.disassembly()
        self.assembly()

    def print_lower_path(self) -> None:
        print("Пример: кратчайшие пути от первой вершины до всех остальных")
        v0: int = 0
        for i in range(len(self.paths[v0])):
            if i == v0:
                continue

            path: Union[int, float] = self.paths[v0][i]

            route: str = " > ".join(self.get_lower_path(
                str(v0 + 1), str(i + 1))
            )
            print(f"{v0 + 1} -> {i + 1}: {path:>2} ({route})")
