import logging
from typing import Any, Dict

import pinecone
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.vectorstores import Pinecone

from regent_rag.core.logging import logger
from regent_rag.core.settings import Settings, get_settings


def get_retriever(settings: Settings, llm: Any) -> MultiQueryRetriever:
    logger.info("Getting retriever...")
    log_level = settings.log_level
    if log_level == logging.DEBUG:
        index = pinecone.Index(settings.pinecone_index_name)
        logger.debug(f'Pinecone stats for index "{settings.pinecone_index_name}\n{index.describe_index_stats()}"')

    embeddings = get_embeddings(settings)
    vectordb = get_vectordb(settings, embeddings)

    # You can return the db itself as a basic retriever
    # return vectordb.as_retriever()

    return MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(), llm=llm)


def get_llm(settings: Settings) -> Any:
    logger.info("Setting up LLM...")
    llm = ChatOpenAI(
        openai_api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
    )
    return llm


def get_embeddings(settings: Settings) -> OpenAIEmbeddings:
    logger.info("Setting up embeddings...")
    embeddings = OpenAIEmbeddings(model=settings.embeddings_model, openai_api_key=settings.openai_api_key)
    return embeddings


def get_vectordb(settings: Settings, embeddings: OpenAIEmbeddings) -> Pinecone:
    logger.info("Initializing Pinecone...")
    pinecone_index_name = settings.pinecone_index_name
    pinecone_api_key = settings.pinecone_api_key
    pinecone_environment = settings.pinecone_environment
    pinecone_text_field = settings.pinecone_text_field

    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
    vectordb = Pinecone.from_existing_index(pinecone_index_name, embeddings, pinecone_text_field)
    return vectordb


def get_chain(llm: Any, retriever: MultiQueryRetriever) -> Any:
    logger.info("Setting up chain...")
    chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return chain


def retrieve_answer(query: str) -> Dict[str, Any]:
    settings = get_settings()
    llm = get_llm(settings)
    multi_query_retriever = get_retriever(settings, llm)
    chain = get_chain(llm, multi_query_retriever)
    # You can get the unique docs that are retrieved in query
    # unique_docs = multi_query_retriever.get_relevant_documents(query)
    # logger.info(unique_docs)

    logger.info("Making query...")
    return chain(query)


def main() -> None:
    # query = "What colors are the Regent logo?""
    # query = "What ISO certifications do Regent have?""
    # query = "Where can I download the font that Regent uses?"
    # query = "How long is the lease time for a staff car?"
    # query = "What's the lease time on a company car?""
    # query = "Can you get me the link to the excel sheet to estimate cost for a staff car?"
    # query = "Which fonts should I use?"

    query = input("Please enter your question: ")
    result = retrieve_answer(query)
    logger.info(result)
    print(result["answer"])


if __name__ == "__main__":
    main()
