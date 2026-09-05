# mazegen

`mazegen` is the reusable maze-generation component of the **A-Maze-ing** project.

It is designed to separate maze generation from the terminal application, allowing the generator to be imported and used independently in other Python programs.

---

## Overview

The package provides a `MazeGenerator` class responsible for creating the internal maze representation.

The generator does not handle:

- Terminal rendering
- Configuration file parsing
- User input
- Solution display
- Writing the final maze file

This separation allows the maze-generation logic to be reused without depending on the rest of the application.

---

## Installation

From the root of the project, the package can be installed with:

```bash
make build
```

After installation, the generator can be imported normally:
    from mazegen.maze_generator import MazeGenerator

---

## Basic Usage

Create a generator by providing the maze dimensions:
    from mazegen.maze_generator import MazeGenerator
    generator = MazeGenerator(20, 10)
    maze = generator.generate()
`generate()` returns the generated maze as a 2D grid.

The returned grid can then be passed to another component, such as a solver or renderer.

---

## API

### `MazeGenerator`

The main class exposed by the package.
    MazeGenerator(width, height, seed=None, perfect=True)

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns in the maze |
| `height` | `int` | Number of rows in the maze |
| `seed` | `int \| None` | Optional seed for reproducible generation |
| `perfect` | `bool` | Determines whether the maze is generated without additional loops |

### `generate()`

    maze = generator.generate()

Generates and returns the maze grid.

The generator starts with every cell containing four walls and progressively removes walls while traversing the grid.

---

## Maze Representation

The maze is stored as a two-dimensional list.

Each cell contains an integer representing its walls using a **bitmask**.

The four directions are represented by individual bits:

    N = 0001
    E = 0010
    S = 0100
    W = 1000

These values allow multiple walls to be represented by combining them with the bitwise OR operator:

    N | E | S | W

which represents a cell with all four walls.

The resulting value is:

    1111 = 15

### Checking a Wall

A wall can be checked using a bitwise AND:

    if maze[y][x] & N:
        # North wall exists

If the result is non-zero, that wall is present.

### Removing a Wall

A wall can be removed using a bitwise AND with the inverted direction bit:

    maze[y][x] &= ~N

The same operation is performed on the neighbouring cell using the opposite direction.

This ensures that a passage is represented consistently from both sides.

---

## Generation Algorithm

The generator uses randomized depth-first traversal with backtracking.

At each cell, the generator:

1. Marks the current cell as visited.
2. Randomizes the four possible directions.
3. Checks each neighbouring cell.
4. Ignores neighbours that are outside the maze.
5. Ignores neighbours that have already been visited.
6. Ignores cells reserved for the `42` logo.
7. Removes the wall between the current cell and a valid neighbour.
8. Continues from the new cell.
9. Backtracks when no unvisited neighbours remain.

An explicit stack is used to keep track of the traversal state rather than relying on Python's call stack.

This allows the generator to handle larger mazes without depending on recursive call depth.

---

## Perfect Mazes

When generating a perfect maze, a new passage is only carved when it leads to an unvisited cell.

This means every newly carved passage connects a new cell to the existing maze.

As a result, the generated maze forms a connected structure without cycles.

For a perfect maze containing `N` cells, the generated structure contains exactly `N - 1` passages.

Therefore, there is exactly one path between any two cells.

---

## Imperfect Mazes

When `perfect` is disabled, the generator can remove additional walls after the initial maze has been created.

These additional passages introduce cycles into the maze.

This allows multiple routes between cells while maintaining the connectivity established during the initial generation.

The imperfect mode is used by the main A-Maze-ing application to provide a more open, Pac-Man-like maze layout.

---

## Randomness and Seeds

Maze generation uses a random number generator to determine the order in which directions are explored.

A seed can be supplied to make generation reproducible:

    generator = MazeGenerator(
        20,
        10,
        seed=42
    )

    maze = generator.generate()

Using the same dimensions and seed produces the same sequence of random choices, which makes generated mazes easier to reproduce during testing and debugging.

---

## 42 Logo Support

The generator supports reserving cells for the `42` logo.

These cells are represented internally as a set of coordinates.

During generation, the DFS traversal checks whether a neighbouring cell belongs to this reserved set.

If it does, the cell is skipped:

    if (nx, ny) in self.forbidden:
        continue

This prevents the maze-generation algorithm from carving passages through the cells occupied by the logo.

The logo constraint is therefore applied during generation rather than modifying an already-generated maze afterwards.

---

## Reusing the Generated Grid

The generator is intentionally independent from the other parts of the project.

For example, the returned grid can be used by a solver:

    from mazegen.maze_generator import MazeGenerator

    generator = MazeGenerator(20, 10)
    maze = generator.generate()

    # Pass maze to another component
    solution = solve(maze)

Or it can be passed to a renderer:

    render_ascii(maze)

This allows the same generated maze representation to be consumed by multiple components.

---

## Example

A minimal standalone program using `mazegen`:

    from mazegen.maze_generator import MazeGenerator


    def main():
        generator = MazeGenerator(
            width=20,
            height=10,
            seed=42
        )

        maze = generator.generate()

        for row in maze:
            print(row)


    if __name__ == "__main__":
        main()

The package itself does not decide how the generated grid should be displayed. The application using the package is responsible for interpreting the grid.

---

## Design Goals

The package follows a few simple design principles:

- **Separation of concerns** — generation is independent from rendering and input handling.
- **Reusability** — the generator can be imported without running the main application.
- **Deterministic testing** — optional seeds make random generation reproducible.
- **Simple data representation** — walls are stored efficiently using integer bitmasks.
- **Independent components** — the generated grid can be passed to other parts of the application.

---

## Project Structure

    mazegen/
    ├── __init__.py
    └── maze_generator.py

The package is intentionally small. Its purpose is to provide the core maze-generation functionality while leaving application-specific behaviour to the main A-Maze-ing project.

---

## Relationship to A-Maze-ing

`mazegen` is the reusable library component of the A-Maze-ing project.

The main application is responsible for:

    Configuration
         |
         v
    Maze generation
         |
         v
    Solving
         |
         v
    Rendering
         |
         v
    User interaction

`mazegen` focuses specifically on:

    Maze dimensions / options
              |
              v
         MazeGenerator
              |
              v
           Maze grid

This makes it possible to reuse the generator independently of the terminal application.