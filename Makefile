VENV = .venv
PYTHON = $(VENV)/bin/python
MATURIN = $(VENV)/bin/maturin


all: run

run:
	$(PYTHON) gui/main.py

# use maturin develop when rust src/ has change
# or when you need to build rust src
build:
	$(MATURIN) develop

dev: build run

setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install maturin pyside6
	$(MATURIN) develop

clean:
	cargo clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	rm -rf $(VENV)

.PHONY: run build dev setup clean fclean