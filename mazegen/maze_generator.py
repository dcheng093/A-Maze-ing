# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    maze_generator.py                                  :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dcheng <dcheng@student.42kl.edu.my>        +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/04/28 12:21:48 by dcheng            #+#    #+#             #
#    Updated: 2026/04/28 12:21:48 by dcheng           ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

import random
from .renderer import apply_42, lock_42_walls

N, E, S, W = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPPOSITE = {N: S, S: N, E: W, W: E}
DIRECTIONS = [N, E, S, W]


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        perfect: bool = False,
    ) -> None:
        """
        generate maze layouts using randomized backtracking

        the generator supports perfect mazes and Pac-Man style
        mazes with loops
        """
        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive")

        self.width = width
        self.height = height
        self.random = random.Random(seed)
        self.perfect = perfect
        self.special_cells: set[tuple[int, int]] = set()
        # initializes grid with all cells fully walled off
        self.grid: list[list[int]] = [
            [N | E | S | W for _ in range(width)]
            for _ in range(height)
        ]

    def generate(self) -> list[list[int]]:
        """generate (optionally braid it) and return the maze grid"""
        visited = [[False] * self.width for _ in range(self.height)]

        if self.width > 12 and self.height > 7:
            self.special_cells = apply_42(self.grid)
        else:
            self.special_cells = set()

        start_x = self.random.randrange(self.width)
        start_y = self.random.randrange(self.height)

        while (start_x, start_y) in self.special_cells:
            start_x = self.random.randrange(self.width)
            start_y = self.random.randrange(self.height)

        self._carve_with_stack(start_x, start_y, visited)

        if not self.perfect:
            self._ensure_pacman_cells()
            self.add_loops()

        self._apply_special_cells()

        return self.grid

    def _ensure_pacman_cells(self) -> None:
        """ensure corners and centre are open in Pac-Man mode"""

        required_cells = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
            (self.width // 2, self.height // 2),
        ]

        for x, y in required_cells:
            if (x, y) in self.special_cells:
                continue

            # already reachable
            if self._cell_openings(x, y) > 0:
                continue

            # open a random wall
            walls = self._dead_end_walls(x, y)

            if walls:
                self._open_passage(
                    x,
                    y,
                    self.random.choice(walls)
                )

    def _carve_with_stack(self, start_x: int, start_y: int,
                          visited: list[list[bool]]) -> None:
        """carve the maze using an explicit stack (recursion depth issues)"""
        stack: list[tuple[int, int, int]] = [(start_x, start_y, -1)]
        visited[start_y][start_x] = True

        while stack:
            x, y, last_direction = stack[-1]
            directions = DIRECTIONS.copy()
            self.random.shuffle(directions)
            next_cell = None

            for direction in directions:
                if direction == last_direction:
                    continue
                nx = x + DX[direction]
                ny = y + DY[direction]
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) in self.special_cells:
                        continue
                    if not visited[ny][nx]:
                        next_cell = (nx, ny, direction)
                        break

            if next_cell is None:
                stack.pop()
                continue

            nx, ny, direction = next_cell
            self.grid[y][x] &= ~direction
            self.grid[ny][nx] &= ~OPPOSITE[direction]
            visited[ny][nx] = True
            stack.append((nx, ny, OPPOSITE[direction]))

    def _find_dead_ends(self) -> list[tuple[int, int]]:
        """return a list of cells that have exactly one open passage"""
        result = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.special_cells:
                    continue

                if self._cell_openings(x, y) == 1:
                    result.append((x, y))

        return result

    def _dead_end_walls(self, x: int, y: int) -> list[int]:
        """return the closed walls that can be opened from the given cell"""
        walls = []

        for direction in DIRECTIONS:
            nx = x + DX[direction]
            ny = y + DY[direction]

            if not self._in_bounds(nx, ny):
                continue

            if (nx, ny) in self.special_cells:
                continue

            # only consider closed walls
            if self.grid[y][x] & direction:
                walls.append(direction)

        return walls

    def add_loops(self) -> None:
        """remove dead ends by braiding the maze"""
        dead_ends = self._find_dead_ends()

        for x, y in dead_ends:
            edges = self._dead_end_walls(x, y)

            if edges:
                edge = self.random.choice(edges)
                self._open_passage(x, y, edge)

    def _cell_openings(self, x: int, y: int) -> int:
        """return the number of open passages connected to a cell"""
        openings = 0
        for direction in DIRECTIONS:
            if not (self.grid[y][x] & direction):
                openings += 1
        return openings

    def _open_passage(self, x: int, y: int, direction: int) -> None:
        """remove the wall between a cell and its neighboring cell"""
        nx = x + DX[direction]
        ny = y + DY[direction]
        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~OPPOSITE[direction]

    def _apply_special_cells(self) -> None:
        """lock the walls surrounding the reserved 42 pattern cells"""
        if self.special_cells:
            lock_42_walls(self.grid, self.special_cells)

    def _in_bounds(self, x: int, y: int) -> bool:
        """returns true if the coordinates lie within the maze boundaries"""
        return 0 <= x < self.width and 0 <= y < self.height
