import pinecone
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from utils.config import load_config
from utils.logging import logger


def main() -> None:
    (
        OPENAI_API_KEY,
        PINECONE_API_KEY,
        PINECONE_INDEX_NAME,
        PINECONE_ENVIRONMENT,
    ) = load_config()

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    index = pinecone.Index(PINECONE_INDEX_NAME)

    logger.debug(
        f'Pinecone stats for index "{PINECONE_INDEX_NAME}\n{index.describe_index_stats()}"'
    )

    model_name = "text-embedding-ada-002"
    logger.info(f"Setting up embedding using {model_name}")
    embed = OpenAIEmbeddings(  # type: ignore[call-arg]
        model=model_name, openai_api_key=OPENAI_API_KEY
    )  # ignore call-arg

    text_field = "text"
    # vectorstore = Pinecone(index, embed.embed_query, text_field)
    vectorstore = Pinecone.from_existing_index(PINECONE_INDEX_NAME, embed, text_field)

    # query = "Where can I download the font that Regent uses?"
    query = "How long is the lease time for a staff car?"
    # query = "Can you get me the link to the excel sheet to estimate cost for a staff car?"

    # completion llm
    llm = ChatOpenAI(  # type: ignore
        openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.0
    )

    qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
    )

    logger.info(qa_with_sources(query))


if __name__ == "__main__":
    main()
