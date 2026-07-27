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

run:
	@python3 $(NAME) $(CONFIG_FILE)

custom:
	@python3 $(NAME) $(CUSTOM_CONFIG)

install:
	pip install flake8 mypy

debug:
	@python3 -m pdb $(NAME) $(CONFIG_FILE)

lint:
	flake8 a_maze_ing.py mazegen/.
	mypy a_maze_ing.py mazegen/. --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 a_maze_ing.py mazegen/.
	mypy a_maze_ing.py mazegen/. --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info

fclean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info
	rm -rf maze_*.txt

.PHONY: install run debug lint lint-strict clean fclean custom