import random
from typing import List
from .renderer import apply_42

N, E, S, W = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPPOSITE = {N: S, S: N, E: W, W: E}


class MazeGenerator:
    def __init__(self,
                 width: int,
                 height: int,
                 seed: int | None = None,
                 perfect: bool = True):
        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive")

        self.width = width
        self.height = height
        self.random = random.Random(seed)
        self.perfect = perfect
        self.forbidden: set[tuple[int, int]] = set()
        self.grid: List[List[int]] = [
            [N | E | S | W for _ in range(width)]
            for _ in range(height)
        ]

    def generate(self) -> List[List[int]]:
        """generate and return the maze grid"""
        visited = [[False] * self.width for _ in range(self.height)]
        self.forbidden = apply_42(self.grid)
        start_x = self.random.randrange(self.width)
        start_y = self.random.randrange(self.height)
        self.dfs(start_x, start_y, visited)
        return self.grid

    def dfs(self, x: int, y: int, visited: List[List[bool]]) -> None:
        """depth-first search maze carving"""
        visited[y][x] = True
        directions = [N, E, S, W]
        self.random.shuffle(directions)

        for direction in directions:
            nx = x + DX[direction]
            ny = y + DY[direction]
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) in self.forbidden:
                    continue
                if not visited[ny][nx]:
                    self.grid[y][x] &= ~direction
                    self.grid[ny][nx] &= ~OPPOSITE[direction]

                    self.dfs(nx, ny, visited)
