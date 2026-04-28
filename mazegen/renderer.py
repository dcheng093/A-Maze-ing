# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    renderer.py                                        :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dcheng <dcheng@student.42kl.edu.my>        +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/04/28 12:22:22 by dcheng            #+#    #+#             #
#    Updated: 2026/04/28 12:22:22 by dcheng           ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from typing import List, Optional, Tuple
COLORS = [
    "\033[0m",   # white
    "\033[94m",  # blue
    "\033[92m",  # green
    "\033[91m",  # red
    "\033[33m",  # yellow
]
N, E, S, W = 1, 2, 4, 8
FOUR_TWO_PATTERN = [
    # 4
    (0, 0), (0, 1), (0, 2),
    (1, 2),
    (2, 0), (2, 1), (2, 2), (2, 3),
    (2, 4),

    # 2
    (4, 0), (5, 0), (6, 0),
    (6, 1),
    (5, 2),
    (4, 3),
    (4, 4), (5, 4), (6, 4),
]


def apply_42(grid: List[List[int]]) -> set[tuple[int, int]]:
    height = len(grid)
    width = len(grid[0])

    if width < 12 or height < 7:
        raise ValueError("Maze too small for 42 pattern")

    cx = width // 2 - 4
    cy = height // 2 - 2

    cells = set()

    for dx, dy in FOUR_TWO_PATTERN:
        x, y = cx + dx, cy + dy
        if 0 <= x < width and 0 <= y < height:
            cells.add((x, y))

    return cells


def lock_42_walls(grid, cells: set[tuple[int, int]]) -> None:
    N, E, S, W = 1, 2, 4, 8

    for x, y in cells:
        grid[y][x] = N | E | S | W


def render_ascii(
                grid: List[List[int]],
                path_coords: Optional[List[Tuple[int, int]]] = None,
                color_mode: int = 0,
                special: Optional[set[tuple[int, int]]] = None
                ) -> None:
    """renders maze using ascii characters"""
    height = len(grid)
    width = len(grid[0])
    color = COLORS[color_mode]
    reset = "\033[0m"
    print(color + "+" + "---+" * width + reset)

    for y in range(height):
        line1 = "|"
        line2 = "+"

        for x in range(width):
            is_42 = special and (x, y) in special
            if is_42:
                line1 += f"{COLORS[3]}███{reset}"
            elif path_coords and (x, y) in path_coords:
                line1 += f"{COLORS[4]} . {reset}"
            else:
                line1 += "   "
            cell = grid[y][x]

            if cell & E:
                line1 += f"{color}|{reset}"
            else:
                line1 += " "

            if cell & S:
                line2 += f"{color}---+{reset}"
            else:
                line2 += f"{color}   +{reset}"

        print(color + line1)
        print(color + line2)
