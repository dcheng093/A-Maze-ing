*This project has been created as part of the 42 curriculum by dcheng, asyeo.*

<p align="center">
  <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcW1kdjZwM2h2YXQzZHQ2NGZ1ZDl5aDRncms4d2Rla2UzdHF1dGFrZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O8dCwBMsKWwtfrcgQs/giphy.gif" alt="cute gif" width="300"/>
</p>

---

Table of contents
- [Description](#description)
- [Instructions](#instructions)
  - [Requirements](#requirements)
  - [Compilation](#compilation)
  - [Other Commands](#other-commands)
- [Configuration File](#configuration-file)
- [Maze Generation (DFS Backtracking)](#maze-generation-dfs-backtracking)
  - [Implementation Details](#implementation-details)
  - [42 Logo Constraint](#42-logo-constraint)
  - [Perfect vs Imperfect Mazes](#perfect-vs-imperfect-mazes)
  - [Why DFS specifically?](#why-dfs-specifically)
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
- [Use of AI](#use-of-ai)


## Description
A-Maze-ing is a terminal-based maze generator and solver written in Python 3.10+. The program reads a configuration file to set up maze parameters, generates a maze using either a Depth-First Search (DFS), embeds the 42 logo in the center of the maze, solves it using Breadth-FIrst-Search (BFS), and renders it in the terminal with ANSI colors and block characters.
The project also provides a reusable Python package `mazegen` that exposes the `MazeGenerator` class for use in any Python project.

**Key features:**
- Maze generation with DFS (recursive backtracker)
- Embedded 42 in the maze's center
- BFS pathfinding to find the shortest solution
- Perfect or imperfect maze modes
- Reproducible mazes via seed
- Interactive menu to regenerate, change colors, and toggle the path for the shortest solution
- Reusable `mazegen` package installable via pip

## Instructions

### Requirements
- Python 3.10+
- pip
- venv (`python3.10+ -m venv "name"`)

### Compilation

Compile the project using `make`:

```bash
make run
```

yeah that's it

### Other Commands

```bash
make install      # installs flake8 && mypy
make debug        # Run in debug mode with pdb
make lint         # Run flake8 and mypy checks
make lint-strict  # Run mypy with --strict flag
make clean        # Remove __pycache__, .mypy_cache, build artifacts

```

---

### Configuration File

The program requires a configuration file as its only argument:

```bash
python3 a_maze_ing.py config.txt
```

**Config file format** (key=value, case-insensitive):

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

| Key         | Type    | Required | Description                                      |
|-------------|---------|----------|--------------------------------------------------|
| WIDTH       | int     | Yes      | Number of columns in the maze (> 0)             |
| HEIGHT      | int     | Yes      | Number of rows in the maze (> 0)                |
| ENTRY       | x,y     | Yes      | Entry cell coordinates                          |
| EXIT        | x,y     | Yes      | Exit cell coordinates                           |
| OUTPUT_FILE | string  | Yes      | Path to the output file                         |
| PERFECT     | bool    | Yes      | True = no loops, False = imperfect maze         |

Lines starting with `#` are treated as comments and ignored.

--- 

## Maze Generation (DFS Backtracking)

The maze is generated using a **Depth-First Search (DFS)** algorithm, also known as the *recursive backtracker*. This approach creates long, winding paths and ensures full connectivity across the maze.

The algorithm proceeds as follows:

1. Start from a random cell
2. Mark the current cell as visited
3. Randomly shuffle the four possible directions (N, E, S, W)
4. For each direction:
   - Compute the neighboring cell `(nx, ny)`
   - Skip if:
     - It is out of bounds
     - It has already been visited
     - It belongs to the **forbidden set** (used for the 42 logo)
   - Otherwise:
     - Remove the wall between the current cell and the neighbor
     - Recursively continue DFS from the neighbor

This process continues until all reachable cells have been visited.

---

### Implementation Details

```python
def dfs(self, x, y, visited):
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
```

### 42 Logo Constraint

Before generation begins, a set of cells forming the **"42" logo** is computed:

```python
self.forbidden = apply_42(self.grid)
```

These cells are treated as blocked during DFS:
- The algorithm will never carve into them
- This preserves the logo shape inside the maze

### Perfect vs Imperfect Mazes
Perfect maze (`PERFECT=True`)
- No loops
- Exactly one path between any two points
- Guaranteed by DFS

Imperfect maze (`PERFECT=False`)
- Additional walls may be removed (optional extension)
- Creates loops and multiple valid paths

### Why DFS specifically?
DFS is used because:
- It is simple and efficient
- Produces visually interesting mazes (long corridors, fewer short branches)
- Guarantees a fully connected maze without isolated sections

## Reusability

The project is structured as a reusable Python package named `mazegen`.

### Reusable Components

- **MazeGenerator**
  - Encapsulates maze generation logic using DFS
  - Can be reused independently in other projects

- **Solver**
  - BFS-based pathfinding (`solve`)
  - Works on any compatible grid representation

- **Renderer**
  - ASCII rendering with optional colors and overlays
  - Can display paths and special patterns

- **Parser**
  - Config file parsing into a structured `Config` object

### How to reuse

The package can be imported into any Python project:

```python
from mazegen.maze_generator import MazeGenerator
```

### Example Usage
```python
gen = MazeGenerator(20, 10)
grid = gen.generate()
```
This modular design allows each component (generation, solving, rendering) to be reused independently.

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

- Recursive DFS may hit recursion limits on large mazes
- Imperfect maze generation could be expanded further
- Rendering performance could be optimized for larger grids

---

### Tools Used

- Python 3.10+
- `mypy` for static type checking
- `flake8` for linting
- `make` for task automation
- Git for version control

## Use of AI

AI was used to help debug my code and adjust it to comply with mypy's restrictions as well as helping me find extra edge cases
