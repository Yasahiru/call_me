from llm_sdk import Small_LLM_Model
from .prompt_builder import PromptBuilder


class ConstrainedDecoder:
     def __init__(self, model: Small_LLM_Model):
        self.model = model
        self.builder = PromptBuilder()
