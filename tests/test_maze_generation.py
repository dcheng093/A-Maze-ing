import unittest

from mazegen.maze_generator import MazeGenerator
from mazegen.solver import solve


class MazeGenerationTests(unittest.TestCase):
    def _count_loops(self, grid: list[list[int]]) -> int:
        width = len(grid[0])
        height = len(grid)
        nodes = 0
        edges = 0

        for y in range(height):
            for x in range(width):
                nodes += 1
                if x + 1 < width and not (grid[y][x] & 2) and not (grid[y][x + 1] & 8):
                    edges += 1
                if y + 1 < height and not (grid[y][x] & 4) and not (grid[y + 1][x] & 1):
                    edges += 1

        return max(edges - nodes + 1, 0)

    def _count_dead_ends(self, grid: list[list[int]]) -> int:
        count = 0
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                openings = 0
                for direction in (1, 2, 4, 8):
                    if not (grid[y][x] & direction):
                        openings += 1
                if openings == 1:
                    count += 1
        return count - 3

    def test_perfect_maze_has_no_loops(self) -> None:
        generator = MazeGenerator(12, 8, seed=42, perfect=True)
        grid = generator.generate()
        self.assertEqual(self._count_loops(grid), 0)

    def test_imperfect_maze_adds_loops(self) -> None:
        generator = MazeGenerator(12, 8, seed=42, perfect=False)
        grid = generator.generate()
        self.assertGreaterEqual(self._count_loops(grid), 2)
        self.assertLessEqual(self._count_dead_ends(grid), 2)

    def test_large_maze_generation_does_not_recurse_too_deeply(self) -> None:
        generator = MazeGenerator(200, 200, seed=7, perfect=True)
        grid = generator.generate()
        self.assertEqual(len(grid), 200)
        self.assertEqual(len(grid[0]), 200)


if __name__ == "__main__":
    unittest.main()
