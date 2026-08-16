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

    # returns the max score from the allowed tokens
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

    # force a token into the prompt
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

        candidates = {
            name: self.model.encode(name + '"').tolist()[0]
            for name in func_names
        }

        generated: List[int] = []
        while True:
            allowed_tokens = set()

            """
                loops over candidates by index
                and adds that token to the allowed tokens
                if the token has a large length
            """
            for token in candidates.values():
                if len(generated) < len(token):
                    allowed_tokens.add(
                        token[len(generated)]
                    )

            """ we add the allowed tokens back to the prompt """
            next_token = self.filter_logits(
                input_ids,
                allowed_tokens,
            )

            """ 
                we add the token that the llm gave us
                to the prompt also to the generated var
                and we create a new candidates dict
            """
            input_ids.append(next_token)
            generated.append(next_token)
            new_candidates = {}

            for name, tokens in candidates.items():
                """ 
                    first we verify that the candidate has a lenght
                    less or equal to what we've generated
                    
                    in the sencond condition we check if the condidate
                    have the same prefix as the generated one 
                """
                if (
                    len(generated) <= len(tokens)
                    and tokens[:len(generated)] == generated
                ):
                    new_candidates[name] = tokens

            candidates = new_candidates
            if self.model.decode([next_token]) == '"':
                return self.model.decode(generated[:-1])

    def generate_number(self, input_ids: list[int]) -> str:

        #  encode the allowed tokens
        digits = self.model.encode("0123456789").tolist()[0]
        stop = self.model.encode(",}").tolist()[0]
        negative = self.model.encode(" -").tolist()[0]
        positive = self.model.encode("+").tolist()[0]
        point = self.model.encode(".").tolist()[0]

        result: list[int] = []
        allowed = digits + stop + negative + point + positive

        while True:
            next_token = self.filter_logits(input_ids + result, allowed)
            decoded = self.model.decode(next_token)

            if ',' in decoded or '}' in decoded:
                if not result:
                    raise ValueError("numbers not found")

                input_ids.extend(result)
                value: str = self.model.decode(result)
                return (value)
            else:
                result.append(next_token)

    def generate_string(self, input_ids: list[int]) -> str:

        result: list[int] = []

        while (True):

            logits = self._cached_logits(tuple(input_ids + result))
            next_token = logits.index(max(logits))
            decoded = self.model.decode([next_token])

            if '"' in decoded and ' "' != decoded:
                if len(decoded) == 1:
                    input_ids.extend(result)
                    return str(result)

                else:
                    i = decoded.index('"')
                    result.extend(self.model.encode(decoded[:i]).tolist()[0])
                return str(self.model.decode(result))

            else:
                result.append(next_token)

    def generate_parameters(
        self,
        fn_name: str,
        functions: list[FunctionDefinition],
        input_ids: list[int],
    ) -> dict[str, Any] | None:
        ...

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
