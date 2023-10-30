import pinecone
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from regent_rag.utils.logging import logger
from regent_rag.utils.settings import get_settings


def main() -> None:
    settings = get_settings()
    openai_api_key = settings.openai_api_key
    pinecone_api_key = settings.pinecone_api_key
    pinecone_index_name = settings.pinecone_index_name
    pinecone_environment = settings.pinecone_environment

    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
    index = pinecone.Index(pinecone_index_name)

    logger.debug(f'Pinecone stats for index "{pinecone_index_name}\n{index.describe_index_stats()}"')

    model_name = "text-embedding-ada-002"
    logger.info(f"Setting up embedding using {model_name}")
    embed = OpenAIEmbeddings(model=model_name, openai_api_key=openai_api_key)  # ignore call-arg

    text_field = "text"
    # vectorstore = Pinecone(index, embed.embed_query, text_field)
    vectorstore = Pinecone.from_existing_index(pinecone_index_name, embed, text_field)

    # query = "Where can I download the font that Regent uses?"
    query = "How long is the lease time for a staff car?"
    # query = "Can you get me the link to the excel sheet to estimate cost for a staff car?"

    # completion llm
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.0)  # type: ignore

    qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
    )

    logger.info(qa_with_sources(query))


if __name__ == "__main__":
    main()
