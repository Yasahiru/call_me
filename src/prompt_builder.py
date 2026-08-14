from .models import FunctionDefinition
from typing import List


class PromptBuilder:

    def build(
        self,
        user_prompt: str,
        functions: List[FunctionDefinition]
    ) -> None:
        prompt = "Available functions:\n"

        for fn in functions:
            prompt += f"Function: {fn.name}\n"
            prompt += f"Description: {fn.description}\n"
            prompt += "Parameters:\n"

            for name, parameter in fn.parameters.items():
                prompt += f"- {name}: {parameter.type}\n"

            prompt += f"Returns: {fn.returns.type}\n"

        prompt += "User request:\n"
        prompt += user_prompt
        prompt += "\n"
        prompt += (
            "Select the best function for the user and generate ONLY "
            "a valid JSON function call."
        )

        return prompt
