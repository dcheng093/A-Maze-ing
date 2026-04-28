# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    solver.py                                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dcheng <dcheng@student.42kl.edu.my>        +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/04/28 12:22:35 by dcheng            #+#    #+#             #
#    Updated: 2026/04/28 12:22:35 by dcheng           ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from collections import deque
from typing import List, Tuple, Dict

N, E, S, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
DX_CHAR = {"E": 1, "W": -1, "N": 0, "S": 0}
DY_CHAR = {"E": 0, "W": 0, "N": -1, "S": 1}
DIR_CHAR = {N: "N", E: "E", S: "S", W: "W"}


def path_to_coords(
        start: Tuple[int, int],
        path: str) -> List[Tuple[int, int]]:
    x, y = start
    coords = [(x, y)]

    for move in path:
        x += DX_CHAR[move]
        y += DY_CHAR[move]
        coords.append((x, y))

    return coords


def solve(
        grid: List[List[int]],
        start: Tuple[int, int],
        end: Tuple[int, int]
        ) -> str:
    """solves maze using bfs"""
    width = len(grid[0])
    height = len(grid)

    queue = deque([start])
    visited = set([start])
    parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], int]] = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            break

        for direction in [N, E, S, W]:
            if not (grid[y][x] & direction):  # for no wall type shi
                nx = x + DX[direction]
                ny = y + DY[direction]

                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        parent[(nx, ny)] = ((x, y), direction)

    # reconstruct
    path = []
    current = end

    while current != start:
        prev, direction = parent[current]
        path.append(DIR_CHAR[direction])
        current = prev

    return "".join(reversed(path))
