from .models import (
    FunctionDefinition,
    ParameterDefinition,
    ReturnDefinition,
    Prompt,
)
from typing import List
import json
import sys


class Parser:
    def __init__(self) -> None:
        self.functions_obj: List[FunctionDefinition] = []
        self.prompts: List[Prompt] = []

    def load_functions(self, file: str) -> None:
        try:
            with open(file, mode="r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("Error: JSON root must be a list")
                sys.exit(1)
            data.append(
                    {
                        "name": "unkown",
                        "description": (
                            "Fallback function to use just when no other "
                            "function matches the user's prompt."
                        ),
                        "parameters": {},
                        "returns": {
                            "type": "string"
                        },
                    }
                )
            for fun in data:
                params = {}
                for k, v in fun["parameters"].items():
                    params[k] = ParameterDefinition(type=v["type"])
                ret = ReturnDefinition(type=fun["returns"]["type"])
                function = FunctionDefinition(
                    name=fun["name"],
                    description=fun["description"],
                    parameters=dict(params),
                    returns=ret
                )
                self.functions_obj.append(function)

        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
            sys.exit(1)

        except json.JSONDecodeError:
            print(f"Error: '{file}' is not a valid JSON file.")
            sys.exit(1)

        except ValueError as e:
            print(f"Validation error:\n{e}")
            sys.exit(1)

        except PermissionError:
            print(f"Error: Permission denied for '{file}'.")
            sys.exit(1)

    def load_prompts(self, file: str) -> None:
        try:
            with open(file, mode="r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("Error: JSON root must be a list")
                sys.exit(1)
            for line in data:
                self.prompts.append(
                    Prompt(prompt=line["prompt"])
                )

        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
            sys.exit(1)

        except json.JSONDecodeError:
            print(f"Error: '{file}' is not a valid JSON file.")
            sys.exit(1)

        except ValueError as e:
            print(f"Validation error:\n{e}")
            sys.exit(1)

        except PermissionError:
            print(f"Error: Permission denied for '{file}'.")
            sys.exit(1)
