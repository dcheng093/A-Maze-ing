# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    parser.py                                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dcheng <dcheng@student.42kl.edu.my>        +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/04/28 12:22:10 by dcheng            #+#    #+#             #
#    Updated: 2026/04/28 12:22:10 by dcheng           ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from dataclasses import dataclass


@dataclass
class Config:
    """
    store maze generation configuration values

    attributes:
        width: maze width
        height: maze height
        entry: starting coordinates
        exit: ending coordinates
        output_file: path for generated maze output file
        perfect: whether to generate a perfect maze
        seed: optional random seed
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_config(filepath: str) -> Config:
    """parse and validate config file"""
    data = {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Invalid line: {line}")

                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()

    except FileNotFoundError:
        raise ValueError(f"Config file not found: {filepath}")

    # requirements
    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

    # parsing
    try:
        width = int(data["WIDTH"])
        height = int(data["HEIGHT"])

        parts = data["ENTRY"].split(",")
        if len(parts) != 2:
            raise ValueError("Invalid ENTRY format")
        ex, ey = map(int, parts)
        entry = (ex, ey)

        parts = data["EXIT"].split(",")
        if len(parts) != 2:
            raise ValueError("Invalid EXIT format")
        tx, ty = map(int, parts)
        exit_ = (tx, ty)

        output_file = data["OUTPUT_FILE"]

        perfect = data["PERFECT"].lower() == "true"

        if not perfect:
            entry = (width // 2, height // 2)

        seed_value = data.get("SEED")
        seed = int(seed_value) if seed_value is not None else None

    except Exception as e:
        raise ValueError(f"Invalid config values: {e}")

    # validation
    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive")

    if not perfect and (width < 3 or height < 3):
        raise ValueError(
            "PERFECT = False requires a maze of at least 3x3"
        )

    if entry == exit_:
        if perfect:
            raise ValueError("ENTRY and EXIT cannot be the same")
        raise ValueError(
            "In PERFECT = False mode, the player starts at the maze center"
            ". Choose an EXIT that is not the center cell"
            )

    for x, y in [entry, exit_]:
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"Point {(x, y)} is out of bounds")

    return Config(width, height, entry, exit_, output_file, perfect, seed)
