from typing import List, Tuple


def write_maze(
        filename: str,
        grid: List[List[int]],
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        path: str,
        ) -> None:
    """write maze in required hex format"""

    try:
        with open(filename, "w", encoding="utf-8") as f:
            # grid
            for row in grid:
                line = "".join(format(cell, "X") for cell in row)
                f.write(line + "\n")
            f.write("\n")

            # entry / exit
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")

            # path
            f.write(path + "\n")

    except Exception as e:
        raise RuntimeError(f"Failed to write maze file: {e}") from e
