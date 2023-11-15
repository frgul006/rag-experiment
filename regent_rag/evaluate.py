import json
from pprint import pformat

from ragas.langchain.evalchain import RagasEvaluatorChain
from ragas.metrics import answer_relevancy  # , context_precision, context_recall, faithfulness

from datasets import Dataset
from regent_rag.core.logging import logger
from regent_rag.core.settings import get_settings
from regent_rag.retrieval import get_chain, get_llm, get_retriever


def main() -> None:
    logger.info("Loading dataset...")
    # The list to store each JSON object
    data_list = []

    # Open the .jsonl file and read each line
    with open("./datasets/dataset.jsonl", "r", encoding="utf-8") as file:
        for line in file:
            # Parse the JSON line and add the dictionary to the list
            json_obj = json.loads(line.strip())
            data_list.append(json_obj)
    dataset = Dataset.from_list(data_list)
    logger.info(pformat(dataset))

    settings = get_settings()
    llm = get_llm(settings)
    multi_query_retriever = get_retriever(settings, llm)
    chain = get_chain(llm, multi_query_retriever)
    # question = "What is the lease time of a staff car?"
    # result = chain(question)
    # logger.info(result["answer"])

    # create evaluation chains
    # faithfulness_chain = RagasEvaluatorChain(metric=faithfulness)
    answer_rel_chain = RagasEvaluatorChain(metric=answer_relevancy)
    # context_rel_chain = RagasEvaluatorChain(metric=context_precision)
    # context_recall_chain = RagasEvaluatorChain(metric=context_recall)

    predictions = chain.batch(dataset)
    logger.info(pformat(predictions))

    # faithfulness_result = faithfulness_chain.evaluate(
    #     dataset,
    #     predictions,
    #     question_key="question",
    #     prediction_key="answer",
    #     context_key="sources",
    #     ground_truths_key="answer",
    # )
    # logger.info(faithfulness_result)

    # context_recall_result = context_recall_chain.evaluate(
    #     dataset,
    #     predictions,
    #     question_key="question",
    #     prediction_key="answer",
    #     context_key="sources",
    #     ground_truths_key="answer",
    # )
    # logger.info(context_recall_result)

    # context_precision_result = context_rel_chain.evaluate(
    #     dataset,
    #     predictions,
    #     question_key="question",
    #     prediction_key="answer",
    #     context_key="sources",
    #     ground_truths_key="answer",
    # )
    # logger.info(context_precision_result)

    answer_relevancy_result = answer_rel_chain.evaluate(
        dataset,
        predictions,
        question_key="question",
        prediction_key="answer",
        context_key="sources",
        ground_truths_key="answer",
    )
    logger.info(answer_relevancy_result)


if __name__ == "__main__":
    main()
