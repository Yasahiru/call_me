from .validator import Validator
from .vocabulary import Vocabulary
from llm_sdk import Small_LLM_Model


if __name__ == "__main__":
    try:
        #  validator tests:
        # v = Validator()
        # v.load_functions("data/input/functions_definition.json")
        # v.load_prompts("data/input/function_calling_tests.json")
        # for el in v.functions_obj:
        #     print(el.name, el.description, sep=": ")
        # print()
        # for p in v.prompts:
        #     print(p.prompt)

        llm = Small_LLM_Model()

        # vocab tests:
        llm = Small_LLM_Model()
        voc = Vocabulary(llm)
        voc.load()

    except Exception as e:
        print(e)
