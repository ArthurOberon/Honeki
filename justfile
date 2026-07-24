venv := ".venv"
python := venv + "/bin/python"
maturin := venv + "/bin/maturin"

default: run

run:	
	{{ python }} gui/main.py

# use maturin develop when rust src/ has change
# or when you need to build rust src
build:
	{{ maturin }} develop

dev: build run

setup:
	python3 -m venv {{ venv }}
	{{ venv }}/bin/pip install maturin pyside6
	{{ maturin }} develop

clean:
	cargo clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete


fclean: clean
	rm -rf {{ venv }}
