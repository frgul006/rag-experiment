import jsonlines
import openai
import pinecone
from tqdm.auto import tqdm

from regent_rag.core.logging import logger
from regent_rag.core.settings import get_settings


def load_data(file_path: str) -> list[dict[str, str]]:
    """
    Load data from a JSONL file.

    Args:
        file_path (str): The path to the JSONL file.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the data from the file.
    """
    with jsonlines.open(file_path) as f:
        data = [item for item in f]
    return data


def init_openai(api_key: str) -> str:
    """
    Initialize eOpenAI API.

    Args:
        api_key (str): The API key for OpenAI.

    Returns:
        str: The name of the OpenAI model to use.
    """
    openai.api_key = api_key
    return "text-embedding-ada-002"


def init_pinecone(api_key: str, index_name: str, environment: str, dimension: int) -> pinecone.Index:
    """
    Initialize the Pinecone index.

    Args:
        api_key (str): The API key for Pinecone.
        index_name (str): The name of the index to create.
        environment (str): The environment to use for the index.
        dimension (int): The dimension of the embeddings.

    Returns:
        pinecone.Index: The Pinecone index.
    """
    pinecone.init(api_key, environment=environment)
    if index_name not in pinecone.list_indexes():
        metadata_config = {"indexed": ["source"]}
        pinecone.create_index(index_name, dimension=dimension, metadata_config=metadata_config)
    return pinecone.Index(index_name)


def create_and_index_embeddings(data: list[dict[str, str]], model: str, index: pinecone.Index) -> None:
    """
    Create embeddings for the data and index them in Pinecone.

    Args:
        data (list[dict[str, str]]): The data to create embeddings for.
        model (str): The name of the OpenAI model to use.
        index (pinecone.Index): The Pinecone index to use.
    """
    batch_size = 32
    for i in tqdm(range(0, len(data), batch_size)):
        batch = data[i : i + batch_size]
        source_batch = [item["source"] for item in batch]
        text_batch = [item["text"] for item in batch]
        ids_batch = [str(n) for n in range(i, i + min(batch_size, len(data) - i))]
        embeds, metadata_batch = create_embeddings_and_metadata(text_batch, source_batch, model)
        to_upsert = zip(ids_batch, embeds, metadata_batch)
        index.upsert(vectors=list(to_upsert))


def create_embeddings_and_metadata(
    text_batch: list[str], source_batch: list[str], model: str
) -> tuple[list[str], list[dict[str, str]]]:
    """
    Create embeddings and metadata for a batch of text.

    Args:
        text_batch (list[str]): The text to create embeddings for.
        source_batch (list[str]): The source of the text.
        model (str): The name of the OpenAI model to use.

    Returns:
        tuple[list[str], list[dict[str, str]]]: A tuple containing the embeddings and metadata.
    """
    res = openai.Embedding.create(input=text_batch, engine=model)
    embeds = [record["embedding"] for record in res["data"]]
    metadata_batch = [{"text": text, "source": source} for text, source in zip(text_batch, source_batch)]
    return embeds, metadata_batch


def main() -> None:
    """
    Main function to create embeddings and index them in Pinecone.
    """
    settings = get_settings()
    openai_api_key = settings.openai_api_key
    pinecone_api_key = settings.pinecone_api_key
    pinecone_index_name = settings.pinecone_index_name
    pinecone_environment = settings.pinecone_environment
    output_folder = settings.output_folder
    training_file_path = f"{output_folder}/train.jsonl"

    logger.info("Loading training data...")
    training_data = load_data(training_file_path)
    logger.debug(f"Loaded {len(training_data)} training examples from {training_file_path}")

    logger.info("Initializing OpenAI model...")
    model = init_openai(openai_api_key)
    sample_embedding = openai.Embedding.create(input="Doesn't matter", engine=model)["data"][0]["embedding"]
    embedding_dimension = len(sample_embedding)

    logger.info("Initializing Pinecone index...")
    pinecone_index = init_pinecone(pinecone_api_key, pinecone_index_name, pinecone_environment, embedding_dimension)

    logger.info("Creating embeddings and populating index...")
    create_and_index_embeddings(training_data, model, pinecone_index)

    logger.info("All done!")


if __name__ == "__main__":
    main()
