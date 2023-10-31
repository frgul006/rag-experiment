import jsonlines
import openai
import pinecone
from tqdm.auto import tqdm

from regent_rag.core.logging import logger
from regent_rag.core.settings import get_settings


def load_data(file_path: str) -> list[dict[str, str]]:
    with jsonlines.open(file_path) as f:
        data = [item for item in f]
    return data


def init_openai(api_key: str) -> str:
    openai.api_key = api_key
    return "text-embedding-ada-002"


def init_pinecone(api_key: str, index_name: str, environment: str, dimension: int) -> pinecone.Index:
    pinecone.init(api_key, environment=environment)
    if index_name not in pinecone.list_indexes():
        metadata_config = {"indexed": ["source"]}
        pinecone.create_index(index_name, dimension=dimension, metadata_config=metadata_config)
    return pinecone.Index(index_name)


def create_and_index_embeddings(data: list[dict[str, str]], model: str, index: pinecone.Index) -> None:
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
    res = openai.Embedding.create(input=text_batch, engine=model)
    embeds = [record["embedding"] for record in res["data"]]
    metadata_batch = [{"text": text, "source": source} for text, source in zip(text_batch, source_batch)]
    return embeds, metadata_batch


def main() -> None:
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
