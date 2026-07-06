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
from .renderer import apply_42

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
        perfect: bool = True,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive")

        self.width = width
        self.height = height
        self.random = random.Random(seed)
        self.perfect = perfect
        self.special_cells: set[tuple[int, int]] = set()
        self.grid: list[list[int]] = [
            [N | E | S | W for _ in range(width)]
            for _ in range(height)
        ]

    def generate(self) -> list[list[int]]:
        """Generate and return the maze grid."""
        visited = [[False] * self.width for _ in range(self.height)]
        self.special_cells = apply_42(self.grid)
        start_x = self.random.randrange(self.width)
        start_y = self.random.randrange(self.height)

        while (start_x, start_y) in self.special_cells:
            start_x = self.random.randrange(self.width)
            start_y = self.random.randrange(self.height)

        self._carve_with_stack(start_x, start_y, visited)
        if not self.perfect:
            self.add_loops()
        return self.grid

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

    def add_loops(self) -> None:
        """add extra corridors while keeping the maze pac-man ready."""
        target_loops = max(2, min(8, (self.width * self.height) // 300))
        target_dead_ends = 2
        attempts = 0

        while attempts < 400:
            if self._loop_count() >= target_loops and \
                    self._dead_end_count() <= target_dead_ends:
                break

            edge = self._pick_best_edge()
            if edge is None:
                break

            x, y, direction = edge
            self._open_passage(x, y, direction)
            attempts += 1

    def _pick_best_edge(self) -> tuple[int, int, int] | None:
        candidates: list[tuple[int, int, int, int]] = []
        seen: set[tuple[tuple[int, int], tuple[int, int]]] = set()

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.special_cells:
                    continue
                for direction in DIRECTIONS:
                    nx = x + DX[direction]
                    ny = y + DY[direction]
                    if not self._in_bounds(nx, ny):
                        continue
                    if (nx, ny) in self.special_cells:
                        continue
                    if self.grid[y][x] & direction:
                        first = (x, y)
                        second = (nx, ny)
                        edge_key = (first, second) if first < second else (
                            second, first
                        )
                        if edge_key in seen:
                            continue
                        seen.add(edge_key)
                        score = self._edge_score(x, y, nx, ny)
                        candidates.append((score, x, y, direction))

        if not candidates:
            return None

        candidates.sort(key=lambda item: item[0], reverse=True)
        best_score = candidates[0][0]
        best_candidates = [
            item[1:] for item in candidates if item[0] == best_score
            ]
        self.random.shuffle(best_candidates)
        return best_candidates[0]

    def _edge_score(self, x: int, y: int, nx: int, ny: int) -> int:
        a_openings = self._cell_openings(x, y)
        b_openings = self._cell_openings(nx, ny)
        if a_openings == 1 and b_openings == 1:
            return 100
        if a_openings == 1 or b_openings == 1:
            return 50
        if a_openings <= 2 and b_openings <= 2:
            return 10
        return 0

    def _cell_openings(self, x: int, y: int) -> int:
        openings = 0
        for direction in DIRECTIONS:
            if not (self.grid[y][x] & direction):
                openings += 1
        return openings

    def _open_passage(self, x: int, y: int, direction: int) -> None:
        nx = x + DX[direction]
        ny = y + DY[direction]
        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~OPPOSITE[direction]

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _dead_end_count(self) -> int:
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.special_cells:
                    continue
                openings = 0
                for direction in DIRECTIONS:
                    if not (self.grid[y][x] & direction):
                        openings += 1
                if openings == 1:
                    count += 1
        return count

    def _loop_count(self) -> int:
        nodes = 0
        edges = 0
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.special_cells:
                    continue
                nodes += 1
                if x + 1 < self.width and not (self.grid[y][x] & E) and \
                        not (self.grid[y][x + 1] & W):
                    edges += 1
                if y + 1 < self.height and not (self.grid[y][x] & S) and \
                        not (self.grid[y + 1][x] & N):
                    edges += 1
        return edges - nodes + 1
