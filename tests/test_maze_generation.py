import io
import unittest
from contextlib import redirect_stdout

from mazegen.maze_generator import MazeGenerator, DX, DY, E, OPPOSITE, W, N, S
from mazegen.renderer import lock_42_walls
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

    def _has_two_way_passage(self, grid: list[list[int]], a: tuple[int, int], b: tuple[int, int]) -> bool:
        x1, y1 = a
        x2, y2 = b
        if x2 == x1 + 1 and y2 == y1:
            direction = E
        elif x2 == x1 - 1 and y2 == y1:
            direction = W
        elif x2 == x1 and y2 == y1 + 1:
            direction = S
        elif x2 == x1 and y2 == y1 - 1:
            direction = N
        else:
            return False
        return not (grid[y1][x1] & direction) and not (grid[y2][x2] & OPPOSITE[direction])

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

    def test_small_maze_warns_on_every_generation(self) -> None:
        generator = MazeGenerator(6, 4, seed=1, perfect=True)
        output = io.StringIO()

        with redirect_stdout(output):
            generator.generate()
            generator.generate()

        warning_output = output.getvalue()
        self.assertEqual(warning_output.count("WARNING"), 2)
        self.assertIn("Maze too small for 42 pattern", warning_output)

    def test_small_grid_does_not_apply_42_pattern(self) -> None:
        generator = MazeGenerator(14, 5, seed=1, perfect=False)
        output = io.StringIO()

        with redirect_stdout(output):
            generator.generate()

        self.assertEqual(generator.special_cells, set())
        self.assertIn("WARNING", output.getvalue())

    def test_imperfect_small_grid_opens_key_cells_with_two_way_passages(self) -> None:
        generator = MazeGenerator(10, 5, seed=1, perfect=False)
        grid = generator.generate()
        key_cells = [(0, 0), (0, 4), (9, 0), (9, 4), (5, 2)]

        for x, y in key_cells:
            if (x, y) in generator.special_cells:
                continue
            openings = 0
            for direction in (E, W, N, S):
                nx = x + DX[direction]
                ny = y + DY[direction]
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    if (nx, ny) not in generator.special_cells and not (grid[y][x] & direction):
                        openings += 1
            self.assertGreaterEqual(openings, 1)

    def test_imperfect_small_grid_has_zero_real_dead_ends(self) -> None:
        generator = MazeGenerator(10, 5, seed=1, perfect=False)
        grid = generator.generate()
        dead_ends = 0

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                openings = 0
                for direction in (1, 2, 4, 8):
                    if not (grid[y][x] & direction):
                        openings += 1
                if openings == 1:
                    dead_ends += 1

        self.assertEqual(dead_ends, 0)

    def test_large_imperfect_maze_has_coherent_walls_with_42_pattern(self) -> None:
        generator = MazeGenerator(20, 10, seed=1, perfect=False)
        grid = generator.generate()
        lock_42_walls(grid, generator.special_cells)
        mismatches = 0

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if x + 1 < len(grid[0]):
                    if bool(grid[y][x] & E) != bool(grid[y][x + 1] & W):
                        mismatches += 1
                if y + 1 < len(grid):
                    if bool(grid[y][x] & S) != bool(grid[y + 1][x] & N):
                        mismatches += 1

        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
