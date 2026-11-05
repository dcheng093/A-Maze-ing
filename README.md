*This project has been created as part of the 42 curriculum by dcheng, asyeo.*

<p align="center">
  <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcW1kdjZwM2h2YXQzZHQ2NGZ1ZDl5aDRncms4d2Rla2UzdHF1dGFrZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O8dCwBMsKWwtfrcgQs/giphy.gif" alt="cute gif" width="300"/>
</p>

---

Table of contents
- [Description](#description)
- [Instructions](#instructions)
  - [Requirements](#requirements)
  - [Running](#running)
  - [Interactive controls](#interactive-controls)
  - [Other Commands](#other-commands)
  - [Building and installing the package](#building-and-installing-the-package)
- [Configuration File](#configuration-file)
- [Output File](#output-file)
- [Maze Representation](#maze-representation)
- [Maze Generation (DFS Backtracking)](#maze-generation-dfs-backtracking)
  - [Implementation Details](#implementation-details)
  - [42 Logo Constraint](#42-logo-constraint)
  - [Perfect vs Imperfect Mazes](#perfect-vs-imperfect-mazes)
  - [Why DFS specifically?](#why-dfs-specifically)
- [Solving (BFS)](#solving-bfs)
- [Randomness and Seeds](#randomness-and-seeds)
- [Error Handling](#error-handling)
- [Reusability](#reusability)
  - [Reusable Components](#reusable-components)
  - [How to reuse](#how-to-reuse)
  - [Example Usage](#example-usage)
- [Team & Project Management](#team--project-management)
  - [Team Members](#team-members)
  - [Planning & Evolution](#planning--evolution)
  - [What Worked Well](#what-worked-well)
  - [What Could Be Improved](#what-could-be-improved)
  - [Tools Used](#tools-used)
- [Resources](#resources)
  - [References](#references)
  - [Use of AI](#use-of-ai)


## Description
A-Maze-ing is a terminal-based maze generator and solver written in Python 3.10+. The program reads a configuration file, generates a random (but seed-reproducible) maze using an iterative Depth-First Search (DFS), embeds the "42" logo in the centre of the maze, finds the shortest path from entry to exit using Breadth-First Search (BFS), writes the maze to a file using a hexadecimal wall encoding, and renders it in the terminal with ANSI colours.

The project also provides a reusable Python package, `mazegen`, which exposes the `MazeGenerator` class (and a solver) for use in any Python project.

**Key features:**
- Maze generation with DFS (iterative, explicit stack: no recursion limit issues)
- Embedded "42" pattern made of fully closed cells in the maze's centre
- BFS pathfinding to find the shortest solution
- Perfect mode (exactly one path) or Pac-Man mode (braided board with loops and no real dead ends)
- Reproducible mazes via an optional `SEED`
- Interactive menu to regenerate, toggle the shortest path and change wall colours
- Reusable `mazegen` package installable via pip

## Instructions

### Requirements
- Python 3.10+
- pip
- venv (`python3 -m venv <name>`)

### Running

```bash
make run
```

`make run` (or `python3 a_maze_ing.py` with no argument) uses the default `default_config.txt`. To run with another config, pass it as the only argument:

```bash
python3 a_maze_ing.py my_config.txt
```

### Interactive controls

| Key | Action |
|-----|--------|
| `r` | Re-generate a new maze (also rewrites the output file) |
| `p` | Show / hide the shortest path |
| `c` | Cycle the wall colour (white, blue, green, red) |
| `q` | Quit (Ctrl+C and Ctrl+D also quit cleanly) |

On screen, `P` is the entry (player), `X` is the exit, `.` marks the shortest path and `███` the "42" cells.

### Other Commands

```bash
make install      # create ./venv and install flake8, mypy and build
make debug        # run in debug mode with pdb
make lint         # flake8 + mypy with the subject's flags
make lint-strict  # flake8 + mypy --strict
make clean        # remove __pycache__, .mypy_cache, build artifacts and maze.txt
make fclean       # clean + remove the venv and the built package
```

### Building and installing the package

```bash
make install      # venv with the build tools
make build        # creates mazegen-1.0.0-py3-none-any.whl and mazegen-1.0.0.tar.gz at the root

# in another virtual environment:
python3 -m venv other_env
other_env/bin/pip install mazegen-1.0.0-py3-none-any.whl
```

---

## Configuration File

The program takes a configuration file as its only argument:

```bash
python3 a_maze_ing.py default_config.txt
```

**Format:**
- one `KEY=VALUE` pair per line, with no spaces around `=`
- keys are case-insensitive (`width=20` is accepted)
- lines starting with `#` are comments; empty lines are ignored
- the file name must end in `.txt`

Default `default_config.txt`:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

| Key         | Type    | Required | Description |
|-------------|---------|----------|-------------|
| WIDTH       | int     | Yes      | Number of columns, from 1 to 1000 |
| HEIGHT      | int     | Yes      | Number of rows, from 1 to 1000 |
| ENTRY       | x,y     | Yes      | Entry cell coordinates (x = column, y = row, starting at 0) |
| EXIT        | x,y     | Yes      | Exit cell coordinates; must differ from the entry |
| OUTPUT_FILE | string  | Yes      | Output file path; must end in `.txt` |
| PERFECT     | bool    | Yes      | `True` = perfect maze (one path, no loops), `False` = Pac-Man board (loops, no real dead ends) |
| SEED        | int     | No       | Seed for reproducible generation; random if absent |

Validation rules:
- the entry and exit must be inside the maze, different from each other, and not inside the "42" pattern
- `PERFECT=False` requires at least a 3x3 maze, and the player (entry) is placed at the **centre** of the maze, so `ENTRY` must still be valid but is replaced by `(WIDTH // 2, HEIGHT // 2)`; the exit must then not be the centre cell
- the "42" pattern is only drawn when the maze is larger than 12x7; for smaller mazes a warning is printed

## Output File

The first displayed maze (and each regenerated one) is written to `OUTPUT_FILE`:

```
b917        <- HEIGHT lines of WIDTH hexadecimal digits, one per cell
86c3
c7d6
            <- empty line
0,0         <- entry (x,y)
3,2         <- exit (x,y)
SENESES     <- shortest path from entry to exit, using N, E, S, W
```

Each line ends with `\n`. The output can be checked with `python3 maze_analyzer.py <output_file>`.

## Maze Representation

Each cell is an integer whose 4 lowest bits encode its walls (bit set to 1 = wall closed):

| Bit | Value | Direction |
|-----|-------|-----------|
| 0 (LSB) | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

```python
N, E, S, W = 1, 2, 4, 8

cell = N | E | S | W     # 15 (0b1111): all walls closed, how every cell starts
if cell & E:             # test: is the east wall closed?
    ...
cell &= ~E               # remove the east wall -> 13 (0b1101)
```

Every wall is shared by two cells, so whenever a wall is removed it is removed from **both** cells (`direction` on one side, `OPPOSITE[direction]` on the other). This keeps the encoding coherent.

---

## Maze Generation (DFS Backtracking)

The maze is generated with a randomized **Depth-First Search**, also known as the *recursive backtracker*, implemented **iteratively with an explicit stack**:

1. Start with every cell fully walled, and push a random starting cell onto the stack
2. Look at the cell on top of the stack
3. Shuffle the four directions (N, E, S, W)
4. Take the first neighbour that is:
   - inside the maze
   - not part of the "42" pattern
   - not visited yet
5. If one exists: remove the wall between the two cells (on both sides), mark the neighbour visited and push it
6. If none exists: the cell is a dead end, so pop it (backtrack)
7. Repeat until the stack is empty

---

### Implementation Details

From `mazegen/maze_generator.py`:

```python
def _carve_with_stack(self, start_x, start_y, visited):
    stack = [(start_x, start_y, -1)]      # (x, y, direction back to the parent)
    visited[start_y][start_x] = True

    while stack:
        x, y, last_direction = stack[-1]  # peek at the top of the stack
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
            stack.pop()                   # dead end -> backtrack
            continue

        nx, ny, direction = next_cell
        self.grid[y][x] &= ~direction            # remove my wall
        self.grid[ny][nx] &= ~OPPOSITE[direction] # remove the neighbour's wall
        visited[ny][nx] = True
        stack.append((nx, ny, OPPOSITE[direction]))
```

A stack is used instead of recursion because Python's default recursion limit (1000) would be exceeded on large mazes, where the DFS depth can reach WIDTH x HEIGHT.

### 42 Logo Constraint

Before generation, the cells forming the "42" (a 7x5 pattern centred in the maze) are computed:

```python
self.special_cells = get_42_cells(self.grid)
```

These cells:
- are never carved into by the DFS (`if (nx, ny) in self.special_cells: continue`)
- are never opened when adding loops
- are forced to `15` (all walls closed) at the end of generation

They therefore appear as a visible, fully closed "42". The pattern never isolates any other cell, and the centre cell always falls in the gap between the "4" and the "2". If the maze is 12x7 or smaller, the pattern is skipped and a warning is printed.

### Perfect vs Imperfect Mazes

**Perfect maze (`PERFECT=True`)**
- DFS only carves into *unvisited* cells, so each carve adds exactly one new cell to the maze: N cells, N - 1 passages
- the result is a spanning tree: fully connected, with no loops
- there is exactly one path between any two cells (including entry and exit)

**Imperfect maze (`PERFECT=False`, Pac-Man board)**
- the perfect maze is generated first, then **braided**: every dead end (a cell with exactly one opening) gets one extra wall opened toward a normal neighbour (never the outer border, never the "42")
- every extra opening creates a loop, so there are many independent routes and no real dead ends
- the four corners and the centre are guaranteed to be open corridors, and the player starts in the centre
- the provided analyzer reports it as `Pac-Man-USABLE` (and bonus-grade with `--max-dead-ends 0`)

Large open areas are avoided by construction: a perfect maze has no cycles, so it cannot contain even a 2x2 open area, and braiding only opens one wall per dead end.

### Why DFS specifically?
- It is simple and efficient: O(WIDTH x HEIGHT) time
- It produces visually interesting mazes (long winding corridors, fewer short branches)
- It visits every reachable cell, so the maze is always fully connected, without isolated sections
- It directly produces a perfect maze (a spanning tree), which is what `PERFECT=True` requires, and is easy to braid for the Pac-Man mode

## Solving (BFS)

The shortest path is found with **Breadth-First Search** (`mazegen/solver.py`) using a FIFO queue (`collections.deque`):
- cells are explored in order of distance from the entry, so the first time the exit is reached it is via a shortest path
- each discovered cell stores its parent and the direction used, so the path is rebuilt backwards from the exit and then reversed into a string such as `SENESES`

BFS is required because in the Pac-Man mode several paths exist and only BFS guarantees the shortest one.

## Randomness and Seeds

Randomness comes from Python's `random` module, using **dedicated `random.Random` instances** rather than the global functions:
- `a_maze_ing.py` creates one generator seeded with `SEED` (or a random seed if absent)
- for each maze (the first one and every regeneration), it draws a new 32-bit seed from it and gives it to `MazeGenerator`, which creates its own `random.Random(seed)`

With the same `SEED`, the first maze is always the same, and so is the sequence of mazes obtained by pressing `r`.

## Error Handling

The program never crashes with a traceback. Every problem results in a clear `Error: ...` message:
- missing configuration file, unreadable file or directory, wrong extension
- lines without `=`, spaces around `=`, missing mandatory keys
- non-numeric values, bad `PERFECT` value, malformed `x,y` coordinates
- non-positive or too large sizes, entry/exit out of bounds, identical, or inside the "42"
- output file that cannot be written

Ctrl+C and Ctrl+D (end of input) exit the program cleanly.

## Reusability

The project is structured as a reusable Python package named `mazegen`.

### Reusable Components

- **MazeGenerator** (`mazegen/maze_generator.py`)
  - Encapsulates maze generation (DFS + optional braiding + "42" reservation)
  - No terminal output, no file access: it only returns the grid

- **Solver** (`mazegen/solver.py`)
  - `solve(grid, start, end)`: BFS shortest path as a string of `N/E/S/W`
  - `path_to_coords(start, path)`: the same path as a list of `(x, y)` cells

- **Renderer** (`mazegen/renderer.py`)
  - ASCII rendering with optional colours, path, entry/exit and special cells

- **Parser** (`mazegen/parser.py`)
  - Config file parsing and validation into a `Config` dataclass

### How to reuse

Install the package (see [Building and installing the package](#building-and-installing-the-package)), then import it:

```python
from mazegen import MazeGenerator, solve, path_to_coords, render_ascii
```

`MazeGenerator(width, height, seed=None, perfect=False)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | number of columns (> 0) |
| `height` | `int` | number of rows (> 0) |
| `seed` | `int \| None` | seed for reproducible generation (`None` = random) |
| `perfect` | `bool` | `True` = perfect maze, `False` = braided Pac-Man board |

`generate()` returns the maze as a `list[list[int]]`: `grid[y][x]` is the wall bitmask of the cell at column `x`, row `y` (see [Maze Representation](#maze-representation)). After `generate()`, `special_cells` contains the coordinates of the "42" cells.

### Example Usage

```python
from mazegen import MazeGenerator, solve, path_to_coords, render_ascii

gen = MazeGenerator(20, 15, seed=42, perfect=True)   # custom size and seed
grid = gen.generate()                                # access the structure

print(grid[0][0])                     # wall bitmask of the top-left cell
print(gen.special_cells)              # cells of the "42" pattern

path = solve(grid, (0, 0), (19, 14))  # access a solution: e.g. "SSEENE..."
coords = path_to_coords((0, 0), path)
render_ascii(grid, coords, player=(0, 0), exit_pos=(19, 14))
```

Each component (generation, solving, rendering) can be used independently.

---

## Team & Project Management

### Team Members

- **dcheng**
  - Core implementation (maze generation, solver, rendering)
  - Project structure and architecture

- **asyeo**
  - Testing, debugging, and validation
  - Feedback and feature suggestions

---

### Planning & Evolution

Initial plan:
- Implement basic DFS maze generation
- Add BFS solver
- Render maze in terminal using ASCII characters

During development:
- Added configuration file support
- Introduced modular package structure (`mazegen`)
- Implemented 42 logo constraint inside the maze
- Added interactive controls (regenerate, toggle path, colors)
- Replaced the recursive DFS with an iterative stack to support large mazes
- Added the Pac-Man (braided) mode for `PERFECT=False`

Final result:
- Fully modular and reusable project
- Clean separation between generation, solving, and rendering
- Interactive and configurable system

---

### What Worked Well

- DFS algorithm produced consistent and visually pleasing mazes
- Modular design made debugging and extension easier
- Configuration system improved flexibility

---

### What Could Be Improved

- Formatting and structure could be better
- Imperfect maze generation could be expanded further
- Rendering performance could be optimized for larger grids

---

### Tools Used

- Python 3.10+
- `mypy` for static type checking
- `flake8` for linting
- `make` for task automation
- `build` / `setuptools` for packaging
- `pdb` for debugging
- Git for version control

## Resources

### References

- [Maze generation algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm): overview of DFS / recursive backtracker, Prim, Kruskal
- [Jamis Buck: Maze Generation, Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking): step-by-step explanation of the algorithm we use
- Jamis Buck, *Mazes for Programmers* (Pragmatic Bookshelf, 2015): braid mazes and dead-end removal
- [Think Labyrinth: Maze Algorithms (Walter D. Pullen)](https://www.astrolog.org/labyrnth/algrithm.htm): perfect vs braid mazes
- [Depth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Depth-first_search) and [Breadth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python `random` module](https://docs.python.org/3/library/random.html) and [Mersenne Twister (Wikipedia)](https://en.wikipedia.org/wiki/Mersenne_Twister)
- [Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) and [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [Python Wiki: Bitwise Operators](https://wiki.python.org/moin/BitwiseOperators)
- [ANSI escape codes (Wikipedia)](https://en.wikipedia.org/wiki/ANSI_escape_code): terminal colours
- [Python Packaging User Guide: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

### Use of AI

AI was used as an assistant, and all AI-suggested changes were reviewed, tested and understood by the team:
- **Debugging**: helping locate bugs in the generator and solver
- **Type checking**: adjusting the code to comply with mypy's restrictions (`make lint` / `make lint-strict`)
- **Edge cases**: suggesting invalid configurations to test the parser and error handling
- **Robustness**: reviewing the project against the evaluation sheet; this led to the clean handling of Ctrl+C / Ctrl+D in the interactive menu (`a_maze_ing.py`) and of unreadable configuration files (`mazegen/parser.py`)
- **Documentation**: help restructuring and completing this README
