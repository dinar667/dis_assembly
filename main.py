# coding: utf-8

from dis_assembly import DisAssemblyAlgo

inf = float("inf")


def main():
    v = {"1", "2", "3", "4", "5", "6"}

    # Матрица последователей - P
    followers = [
        [0, "2", "3", "4", 0, "6"],
        ["1", 0, "3", "4", 0, 0],
        ["1", "2", 0, "4", 0, "6"],
        ["1", "2", "3", 0, "5", 0],
        [0, 0, 0, "4", 0, "6"],
        ["1", 0, "3", 0, "5", 0]
    ]

    # Матрица кратчайших расстояний - M
    paths = [
        [0, 7, 9, 21, inf, 2],
        [7, 0, 10, 15, inf, inf],
        [9, 10, 0, 11, inf, 14],
        [21, 15, 11, 0, 6, inf],
        [inf, inf, inf, 6, 0, 9],
        [2, inf, 14, inf, 9, 0]
    ]

    da = DisAssemblyAlgo(v=v, followers=followers, paths=paths)
    da.find_lower_paths()

    da.print_lower_path()


if __name__ == '__main__':
    main()
