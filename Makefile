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

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3
NAME = a_maze_ing.py
CONFIG_FILE = default_config.txt
CUSTOM_CONFIG = config.txt

install:
	@python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install mypy flake8 build

build:
	$(PYTHON) -m build --outdir .

reinstall: build
	$(PIP) install --force-reinstall mazegen-1.0.0-py3-none-any.whl

run:
	@python3 $(NAME) $(CONFIG_FILE)

custom:
	@python3 $(NAME) $(CUSTOM_CONFIG)

debug:
	@python3 -m pdb $(NAME) $(CONFIG_FILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info maze.txt output_*.txt

fclean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info maze.txt output_*.txt venv mazegen-1.0.0-py3-none-any.whl mazegen-1.0.0.tar.gz mazegen-1.0.0

lint:
	flake8 a_maze_ing.py mazegen/.
	mypy a_maze_ing.py mazegen/. --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 a_maze_ing.py mazegen/.
	mypy a_maze_ing.py mazegen/. --strict

.PHONY: install build reinstall run custom debug clean fclean lint lint-strict