import hashlib
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any

import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm

from utils.logging import logger

OUTPUT_FOLDER = "./out"
SCRAPE_FOLDER = f"{OUTPUT_FOLDER}/scrape"

tokenizer = tiktoken.get_encoding("cl100k_base")


def tiktoken_len(text: str) -> int:
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""],
)


def process_file(file_path: str) -> list[Any]:
    documents = []

    try:
        # Load the JSON content
        with open(file_path, "r") as f:
            content = json.load(f)

        # Generate a unique ID based on the file path
        m = hashlib.md5()
        m.update(file_path.encode("utf-8"))
        uid = m.hexdigest()[:12]

        # Split the content into chunks
        chunks = text_splitter.split_text(content["content"])

        # Create document data
        for i, chunk in enumerate(chunks):
            documents.append(
                {"id": f"{uid}-{i}", "text": chunk, "source": content["url"]}
            )

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")

    return documents


def process_json_files(folder_path: str, output_folder_path: str) -> list[Any]:
    # Get all files in the folder
    all_files = os.listdir(folder_path)

    # Filter out JSON files
    json_files = [file for file in all_files if file.endswith(".json")]

    documents = []

    with ProcessPoolExecutor(max_workers=4) as executor:
        future_to_file = {
            executor.submit(process_file, os.path.join(folder_path, file)): file
            for file in json_files
        }
        for future in tqdm(as_completed(future_to_file), total=len(json_files)):
            documents.extend(future.result())

    # Save the documents to a JSONL file
    with open(f"{output_folder_path}/train.jsonl", "w") as f:
        for doc in documents:
            f.write(json.dumps(doc) + "\n")

    return documents


def main() -> None:
    process_json_files(SCRAPE_FOLDER, OUTPUT_FOLDER)


if __name__ == "__main__":
    main()
