from mazegen.maze_generator import MazeGenerator


def count_loops(grid):
    width = len(grid[0])
    height = len(grid)
    visited = [[False] * width for _ in range(height)]
    nodes = 0
    edges = 0
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        x, y = stack.pop()
        nodes += 1
        if y > 0 and not (grid[y][x] & 1) and not (grid[y - 1][x] & 4):
            edges += 1
        if x + 1 < width and not (grid[y][x] & 2) and not (grid[y][x + 1] & 8):
            edges += 1
        if y + 1 < height and not (
              grid[y][x] & 4) and not (grid[y + 1][x] & 1):
            edges += 1
        if x > 0 and not (grid[y][x] & 8) and not (grid[y][x - 1] & 2):
            edges += 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                visited[ny][nx] = True
                stack.append((nx, ny))
    return edges - nodes + 1

perfect = MazeGenerator(12, 8, seed=42, perfect=True).generate()
imperfect = MazeGenerator(12, 8, seed=42, perfect=False).generate()
print('perfect_loops', count_loops(perfect))
print('imperfect_loops', count_loops(imperfect))
assert count_loops(perfect) == 0
assert count_loops(imperfect) >= 2
print('verification=passed')
