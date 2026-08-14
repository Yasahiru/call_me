from functools import lru_cache
from typing import List, Tuple, Set
from llm_sdk import Small_LLM_Model  # type: ignore
from .prompt_builder import PromptBuilder
from .models import FunctionDefinition, FunctionCall


class ConstrainedDecoder:
    def __init__(self, model: Small_LLM_Model):
        self.model = model
        self.builder = PromptBuilder()

    @lru_cache(maxsize=512)
    def _cached_logits(
        self,
        inp_ids_tup: Tuple[int, any]
    ) -> List[float]:
        return self.model.get_logits_from_input_ids(
            list(inp_ids_tup)
        )

    def filter_logits(
        self,
        input_ids: List[int],
        allowed_tokens: Set[int]
    ) -> int:

        if not allowed_tokens:
            raise ValueError("No allowed tokens available")

        logits = self._cached_logits(tuple(input_ids))
        return max(
            allowed_tokens,
            key=lambda token_id: logits[token_id]
        )

    def force_token(
        self,
        text: str,
        input_ids: List[int]
    ) -> None:
        token_ids = self.model.encode(text).tolist[0]
        input_ids.extend(token_ids)

    def generate_function_names(
        self,
        input_ids: List[int],
        func_names: List[str]
    ) -> None:

        func_ids = List[List[int]] = []
        for name in func_names:
            token = self.model.encode(name + '"')
            func_ids.append(token.tolist()[0])

    def decode(
        self,
        prompt: str,
        functions: List[FunctionDefinition]
    ) -> FunctionCall:

        general_prompt = self.builder.build(
            prompt,
            functions
        )
        input_ids = self.model.encode(general_prompt).tolist()[0]
        logits = self._cached_logits(tuple(input_ids))
