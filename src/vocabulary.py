import json
from typing import Dict


class Vocabulary:
    def __init__(self, llm) -> None:
        self.llm = llm
        self.token_to_text: Dict[int, str] = {}

    def load(self) -> None:
        path = self.llm.get_path_to_vocab_file()

        with open(path, mode="r") as f:
            data = json.load(f)

        for d in data:
            print(self.llm.decode(d))


