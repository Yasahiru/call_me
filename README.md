*This project has been created as part of the 42 curriculum by hloutman.*

# Function Calling with Constrained Decoding

## Description

This project implements a small language-model pipeline for function-calling tasks. The goal is to take a natural-language user request, select the most relevant function from a list of available tools, and output a valid JSON object that matches the expected schema.

The system is built around a constrained decoding strategy: rather than letting the model produce any text, the decoder narrows generation to a valid function name and parameter structure. This makes the output both safer and easier to validate.

The project is organized around a lightweight CLI that:

- loads available function definitions from JSON,
- builds a prompt describing the callable functions,
- runs a local LLM,
- constrains decoding so the final output matches the expected JSON format,
- writes the result to an output JSON file.

A separate moulinette sub-project is also included to generate exercise files and grade student submissions against a public or private dataset.

## Instructions

### Prerequisites

- Python 3.10+
- `uv` package manager
- Internet access to download the chosen Hugging Face model on first run

### Installation

From the repository root:

```bash
uv sync
```

This installs the project dependencies and the workspace package for the local LLM SDK.

### Running the main project

The main program is executed from the repository root:

```bash
uv run python3 -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json \
  --model Qwen/Qwen3-0.6B
```

You can also use a different model, for example:

```bash
uv run python3 -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

### Running the moulinette

The moulinette lives in the `moulinette/` directory:

```bash
cd moulinette
uv run python -m moulinette prepare_exercises --set public
uv run python -m moulinette grade_student_answers data/output/function_calls.json --set public
```

To generate a private dataset instead:

```bash
cd moulinette
uv run python -m moulinette prepare_exercises --set private
uv run python -m moulinette grade_student_answers data/output/function_calls.json --set private
```

### Common development commands

```bash
make run
make run-large
make test
```

## Algorithm explanation

The central idea is constrained decoding.

### 1. Function metadata loading

The parser reads a JSON list of function declarations, each containing:

- the function name,
- a description,
- parameter names and types,
- return type.

These entries are converted into typed Pydantic models so they can be validated before use.

### 2. Prompt construction

The `PromptBuilder` builds a textual prompt containing:

- the list of callable functions,
- their descriptions,
- parameter names and expected types,
- the user request.

The prompt ends with a clear instruction: select the best function and emit only a valid JSON function call.

### 3. Function name decoding

The decoder first forces a JSON-like prefix into the model input, then begins generating the function name. To avoid arbitrary tokens, the implementation:

- encodes candidate function names,
- keeps only tokens that match the current generation prefix,
- applies a logit filter to choose the most likely valid next token,
- continues until the closing quote is reached.

This prevents the model from producing names that are not in the available function set.

### 4. Parameter decoding

Once the function name is known, parameter generation is performed in a type-aware way:

- numbers are decoded while restricting the model to numeric digits and valid separators,
- strings are built in a controlled way to keep them syntactically valid JSON strings,
- booleans are mapped to JSON booleans,
- each parameter is inserted in the correct JSON object layout.

The result is a structured object equivalent to:

```json
{
  "name": "function_name",
  "parameters": {
    "arg1": "value",
    "arg2": 42
  }
}
```

### 5. Validation and output

After generation, the result is written to a JSON file. The system also validates the object structure, so invalid or malformed responses are either corrected or rejected before saving.

## Design decisions

Several design choices were made to keep the implementation simple and robust:

- Type-driven validation: Pydantic models validate function definitions and prompts before runtime use.
- Cached logits: repeated token decisions use a memoized cache to reduce redundant model calls.
- Modular architecture: parsing, prompt building, model access, and decoding are separated into distinct components.
- Deterministic structure: generation is constrained to valid JSON fields, which reduces the risk of malformed function calls.
- Fallback handling: a fallback `unknown` function is added when no candidate function clearly matches the prompt.
- Small-model-first setup: the project is designed to work with small local models, making it practical for rapid iteration and experimentation.

## Performance analysis

This solution trades raw free-form generation speed for reliability. Constrained decoding usually improves validity and reduces the number of malformed outputs, but it also adds overhead because the decoder must continuously check candidate tokens and filter logits.

### Accuracy

Accuracy depends mostly on the model size and the quality of the function definitions. Small models can perform the task reasonably well when the function list is short and descriptions are clear, but accuracy drops when:

- the function descriptions are vague,
- multiple functions are semantically close,
- the request requires subtle reasoning.

### Speed

The runtime is strongly influenced by model size and the number of prompts being processed. The decoder introduces extra token filtering operations, which adds latency compared to unconstrained generation. However, the cache helps reduce repeated work for repeated token prefixes.

### Reliability

The main reliability gain is structural correctness. By restricting generation to valid function names and JSON-compatible parameter values, the solution avoids many common failure modes such as:

- invalid JSON,
- wrong function names,
- missing required fields,
- type mismatches.

In practice, reliability is good for small controlled task sets, while larger and noisier tool catalogs need more careful prompt design.

## Challenges faced

The main difficulties encountered were technical and algorithmic:

1. Matching the model output to a real function name without producing unsupported tokens.
2. Building valid JSON while keeping generation constrained and stable.
3. Handling different parameter types consistently, especially numbers and strings.
4. Managing model latency with repeated inference passes.
5. Ensuring the project remained modular enough to work with different model backends.

These were addressed by:

- restricting generated tokens to candidate prefixes,
- validating function schemas before decoding,
- implementing dedicated number and string generation routines,
- using a cache for repeated logit lookups,
- separating parsing, prompting, and decoding logic into independent modules.

## Testing strategy

Validation was performed through a combination of lightweight automated and manual checks:

- Pydantic model validation to catch malformed function definitions and prompts.
- JSON parsing checks for input files and generated outputs.
- CLI execution against the provided function definitions and prompt datasets.
- Output inspection to confirm the structure is valid and matches the expected schema.
- Regression-style validation by re-running with different models and checking the JSON output remains well-formed.

The project also includes a moulinette grader that can compare generated outputs to expected corrections for function-calling tasks.

## Example usage

### Example 1: Run with a small model

```bash
uv run python3 -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json \
  --model Qwen/Qwen3-0.6B
```

### Example 2: Generate and grade exercise data

```bash
cd moulinette
uv run python -m moulinette prepare_exercises --set public
uv run python -m moulinette grade_student_answers ../data/output/function_calling_results.json --set public
```

### Example 3: Run with a larger model

```bash
uv run python3 -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json \
  --model Qwen/Qwen3-1.7B
```

## Resources

### Documentation and references

- Hugging Face Transformers documentation: https://huggingface.co/docs/transformers
- PyTorch documentation: https://pytorch.org/docs/
- Pydantic documentation: https://docs.pydantic.dev/
- JSON Schema and structured output principles: https://json-schema.org/
- Function-calling and tool-use patterns in modern LLM systems: https://platform.openai.com/docs/guides/function-calling

### AI usage

AI was used during the development of this project for:

- drafting and refining the constrained decoding logic,
- proposing prompt structures for tool selection, 
- helping validate the design of the JSON output format,
- accelerating the writing of the project documentation and README.

The AI assistance was used as a support tool to improve implementation quality and documentation clarity, while the final validation and code decisions remained under human control.

## Summary

This project explores a practical approach to function calling with local models: keep the model constrained to a valid tool schema, enforce JSON output structure, and validate results before writing them. The result is a lightweight but effective pattern for tool-use tasks in constrained environments.
