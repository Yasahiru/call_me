from .models import FunctionDefinition, ParameterDefinition
from .models import ReturnDefinition, Prompt
import json
# import sys


class Validator:
    def __init__(self):
        self.functions_obj = []
        self.prompts = []

    def load_functions(self, file: str) -> None:
        with open(file, mode="r") as f:
            data = json.load(f)

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

    def load_prompts(self, file: str) -> None:
        with open(file, mode="r") as f:
            data = json.load(f)

        for line in data:
            self.prompts.append(
                Prompt(prompt=line["prompt"])
            )
