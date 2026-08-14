import os
import time
import json
import argparse
from .parser import Parser
from llm_sdk import Small_LLM_Model
from .decoder import ConstrainedDecoder
from typing import Any


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Constrained function calling"
    )
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the functions definition file",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the prompts file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to the output file",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen3-0.6B",
        help="Model to use",
    )

    args = parser.parse_args()
    # try:
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    # except Exception as e:
    #     raise ValueError(f"error {e}")
    return args


def main() -> None:
    start = time.time
    args = parse_arguments()
    p = Parser()
    p.load_functions(args.functions_definition)
    p.load_prompts(args.input)

    functions = p.functions_obj
    prompts = p.prompts

    model = Small_LLM_Model(model_name=args.model)
    constrained_decoder = ConstrainedDecoder(model)

    result: list[dict[str, Any]] = []
    for prompt in prompts:
        try:
            output = constrained_decoder.decode(prompt.prompt, functions)
            # result.append(output.model_dump())
            print()
        except ValueError as e:
            print(f"Error: {e}")

    # try:
    # with open(args.output, 'w') as f:
    #     json.dump(result, f, indent=4)
    # except OSError as e:
    #     raise ValueError(f"Error: could not write output {e}")
    # except TypeError as e:
    #     raise ValueError(f"Error: output data is not JSON-serializable: {e}")
    # except KeyboardInterrupt:
    #     print("stop")
    #     exit(130)
