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
from mazegen.renderer import render_ascii, apply_42, lock_42_walls
from mazegen.solver import solve, path_to_coords
from mazegen.parser import parse_config, Config
from mazegen.output_writer import write_maze
import sys
import os

def clear_terminal():
    # "nt" for windows, others like "posix" are for mac/linux
    os.system('cls' if os.name == 'nt' else 'clear')

def build_maze(config: Config) -> tuple[
            list[list[int]],
            str,
            list[tuple[int, int]],
            set[tuple[int, int]]
        ]:
    """generates maze && solves it"""
    width = config.width
    height = config.height

    def in_bounds(p):
        x, y = p
        return 0 <= x < width and 0 <= y < height

    if not in_bounds(config.entry):
        raise ValueError(f"Entry {config.entry} is out of bounds")

    if not in_bounds(config.exit):
        raise ValueError(f"Exit {config.exit} is out of bounds")
    while True:
        gen = MazeGenerator(
            width,
            height,
            seed=None,
            perfect=config.perfect,
        )
        grid = gen.generate()
        special_cells = apply_42(grid)
        lock_42_walls(grid, special_cells)
        # entry || exit not inside 42
        if config.entry in special_cells or config.exit in special_cells:
            continue  # regenerate
        try:
            path = solve(grid, config.entry, config.exit)
        except KeyError:
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

        show_path = True
        color_mode = 0

        while True:
            # render current state
            render_ascii(
                        grid,
                        coords if show_path else None,
                        color_mode,
                        special
                        )

            print("\nSolution (N/E/S/W):")
            print(path)

            print("\n[r] regenerate  [p] toggle path  [c] colour  [q] quit")
            cmd = input("> ").strip().lower()

            if cmd == "q":
                break

            elif cmd == "r":
                grid, path, coords, special = build_maze(config)
                clear_terminal()

            elif cmd == "p":
                show_path = not show_path

            elif cmd == "c":
                color_mode = (color_mode + 1) % 4
                print(f"Colour mode: {color_mode}")

            else:
                print("Unknown command")

        # write final maze output only upon clean exit
        write_maze(
            config.output_file,
            grid,
            config.entry,
            config.exit,
            path,
        )

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
