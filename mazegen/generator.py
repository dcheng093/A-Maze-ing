# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    generator.py                                       :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: dcheng <dcheng@student.42kl.edu.my>        +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/04/28 12:21:34 by dcheng            #+#    #+#             #
#    Updated: 2026/04/28 12:21:34 by dcheng           ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from typing import List, Optional, Tuple
from .maze_generator import MazeGenerator


class Generator:
    """
    public wrapper for maze generation

    this is the class exposed by the mazegen package
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        self._engine = MazeGenerator(width, height, seed, perfect)

    def generate(self) -> List[List[int]]:
        """
        generate a maze grid
        returns:
            2D grid of integer bitmasks
        """
        return self._engine.generate()

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        """
        optional convenience wrapper if you want
        (you can also keep solver separate)
        """
        from .solver import solve
        grid = self._engine.grid
        return solve(grid, start, end)
