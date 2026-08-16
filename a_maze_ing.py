# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    a_maze_ing.py                                      :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dcheng <dcheng@student.42kl.edu.my>        +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/04/28 12:21:09 by dcheng            #+#    #+#             #
#    Updated: 2026/04/28 12:21:09 by dcheng           ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from mazegen.maze_generator import MazeGenerator
from mazegen.renderer import render_ascii, get_42_cells
from mazegen.solver import solve, path_to_coords
from mazegen.parser import parse_config, Config
from mazegen.output_writer import write_maze
import sys
import os
N, E, S, W = 1, 2, 4, 8


def clear_terminal() -> None:
    """clear terminal screen depending on operating system"""
    # nt for windows, others like "posix" are for mac/linux
    os.system('cls' if os.name == 'nt' else 'clear')


def _warn_small_maze() -> None:
    """emit a clear warning when the 42 pattern cannot be applied"""
    print("\033[31mWARNING: Maze too small for 42 pattern\033[0m")


def build_maze(config: Config) -> tuple[
            list[list[int]],
            str,
            list[tuple[int, int]],
            set[tuple[int, int]]
        ]:
    """generates maze && solves it"""
    width = config.width
    height = config.height

    def in_bounds(p: tuple[int, int]) -> bool:
        x, y = p
        return 0 <= x < width and 0 <= y < height

    if not in_bounds(config.entry):
        raise ValueError(f"Entry {config.entry} is out of bounds")

    if not in_bounds(config.exit):
        raise ValueError(f"Exit {config.exit} is out of bounds")

    # calculates where 42 logo should be (if grid big enough)
    if width > 12 and height > 7:
        temp_grid = [[0 for _ in range(width)]
                     for _ in range(height)
                     ]
        logo_cells = get_42_cells(temp_grid)
        if config.entry in logo_cells:
            raise ValueError("Entry cannot be inside 42 logo")
        if config.exit in logo_cells:
            raise ValueError("Exit cannot be inside 42 logo")

    while True:
        gen = MazeGenerator(
            width,
            height,
            seed=config.seed,
            perfect=config.perfect,
        )
        grid = gen.generate()
        special_cells = gen.special_cells
        try:
            path = solve(grid, config.entry, config.exit)
        except ValueError:
            continue  # unsolvable maze == regenerate
        coords = path_to_coords(config.entry, path)
        return grid, path, coords, special_cells


def main() -> None:
    try:
        if len(sys.argv) > 2:
            raise ValueError("Usage: python a_maze_ing.py [config_file]")

        config_file = (
            sys.argv[1]
            if len(sys.argv) == 2
            else "default_config.txt"
           )
        config = parse_config(config_file)

        grid, path, coords, special = build_maze(config)
        player = config.entry
        current_coords = coords.copy()

        try:
            write_maze(
                config.output_file,
                grid,
                config.entry,
                config.exit,
                path,
            )
        except RuntimeError as e:
            print(f"Error: {e}")
            return

        show_path = True
        color_mode = 0

        while True:
            # render current state
            clear_terminal()
            if config.width <= 12 and config.height <= 7:
                _warn_small_maze()
            render_ascii(
                        grid,
                        current_coords if show_path else None,
                        color_mode,
                        player,
                        special,
                        config.exit
                        )

            print("\nSolution (N/E/S/W):")
            print(path)

            print("\n[r] regenerate  [p] toggle path  "
                  "[c] colour  [q] quit")
            cmd = input("> ").strip().lower()

            if cmd == "q":
                break

            elif cmd == "r":
                grid, path, coords, special = build_maze(config)
                player = config.entry
                current_coords = coords.copy()

                try:
                    write_maze(
                        config.output_file,
                        grid,
                        config.entry,
                        config.exit,
                        path,
                    )
                except RuntimeError as e:
                    print(f"Error: {e}")
                    break

                clear_terminal()

            elif cmd == "p":
                show_path = not show_path

            elif cmd == "c":
                color_mode = (color_mode + 1) % 4
                print(f"Colour mode: {color_mode}")

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
