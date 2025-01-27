from sys import argv
from llama_index.core import Response, Document
from llama_index.core.evaluation import BaseEvaluator, FaithfulnessEvaluator
from llama_index.core.schema import NodeWithScore

from processing import llm, iterate
from pagebypage import parse_arguments, ask_parameters


def evaluate(evaluator: BaseEvaluator, page_prompt: str):
    completion_response = llm.complete(page_prompt)

    response = Response(
        response=completion_response.text,
        source_nodes=[NodeWithScore(node=Document(text=page_prompt), score=1.0)],
    )

    print("Response:")
    print(response)

    eval_result = evaluator.evaluate_response(response=response, query=prompt)

    print(f"\nPassing: {eval_result.passing}\n")

    print("Reason:")
    print(eval_result.feedback)

    print("\n--------------------------------\n")


if __name__ == '__main__':
    document, prompt, pages, _ = parse_arguments() if len(argv) > 1 else ask_parameters(save_output=False)

    print('Processing...\n')

    evaluator = FaithfulnessEvaluator(llm=llm)

    iterate(lambda page_prompt, _: evaluate(evaluator, page_prompt), document, prompt, pages)
