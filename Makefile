# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcheng <dcheng@student.42kl.edu.my>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/22 11:21:10 by dcheng            #+#    #+#              #
#    Updated: 2026/04/22 11:21:10 by dcheng           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = a_maze_ing.py
CONFIG_FILE = default_config.txt
CUSTOM_CONFIG = config.txt

install:
	pip install flake8 mypy

run:
	@python3 $(NAME) $(CONFIG_FILE)

custom:
	@python3 $(NAME) $(CUSTOM_CONFIG)

debug:
	@python3 -m pdb $(NAME) $(CONFIG_FILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info maze_*.txt output_*.txt

lint:
	flake8 a_maze_ing.py mazegen/.
	mypy a_maze_ing.py mazegen/. --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 a_maze_ing.py mazegen/.
	mypy a_maze_ing.py mazegen/. --strict

.PHONY: install run custom debug clean lint lint-strict