install:
	uv sync

run:
	uv run python3 -m src \
	--functions_definition data/input/functions_definition.json \
	--input data/input/function_calling_tests.json \
	--output data/output/function_calling_results.json \
	--model Qwen/Qwen3-0.6B

run-large:
	uv run python3 -m src \
	--functions_definition data/input/functions_definition.json \
	--input data/input/function_calling_tests.json \
	--output data/output/function_calls.json \
	--model Qwen/Qwen3-1.7B

run-large2:
	uv run python3 -m src \
	--functions_definition data/input/functions_definition.json \
	--input data/input/function_calling_tests.json \
	--output data/output/function_calls.json \
	--model facebook/opt-125m

run-large3:
	uv run python3 -m src \
	--functions_definition data/input/functions_definition.json \
	--input data/input/function_calling_tests.json \
	--output data/output/function_calls.json \
	--model TinyLlama/TinyLlama-1.1B-Chat-v1.0

run-large4:
	uv run python3 -m src \
	--functions_definition data/input/functions_definition.json \
	--input data/input/function_calling_tests.json \
	--output data/output/function_calls.json \
	--model Qwen/Qwen2-0.5B

test:
	uv run pytest tests/ -v

lint:
	uv run mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	uv run flake8 src/

lint-strict:
	uv run mypy src/ --strict
	uv run flake8 src/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +