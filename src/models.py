from typing import Dict, Any
from pydantic import BaseModel, model_validator


class ParameterDefinition(BaseModel):
    type: str

    @model_validator(mode="after")
    def verify_len(self) -> "ParameterDefinition":
        res = self.type.strip()
        if not res:
            raise ValueError("empty parameter type")
        self.type = self.type.strip()
        return self


class ReturnDefinition(BaseModel):
    type: str


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, ParameterDefinition]
    returns: ReturnDefinition

    @model_validator(mode="after")
    def verify_len(self) -> "FunctionDefinition":
        if not self.name.strip():
            raise ValueError("empty function name")
        if not self.description.strip():
            raise ValueError("empty function description")
        for p in self.parameters:
            if not p.strip():
                raise ValueError("empty parameter name")
        return self


class FunctionCall(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Any]


class Prompt(BaseModel):
    prompt: str

    @model_validator(mode="after")
    def verify_len(self) -> "Prompt":
        if not self.prompt.strip():
            raise ValueError("empty prompt")
        return self
