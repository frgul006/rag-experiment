# Workshop notes

## TO DOs

- Evaluation

  - MDD (Metrics-Driven Development)

    - Using Ragas, we can evaluate and monitor essential metrics over time such as

      - **Faithfulness**: This feature assists in identifying and quantifying instances of hallucinations.
      - **Bad retrieval**: This feature helps identify and quantify poor context retrievals.
      - **Bad response**: This feature helps in recognizing and quantifying evasive, harmful, or toxic responses.
      - **Bad format**: This feature helps in detecting and quantifying responses with incorrect formatting.

- Frontend
- Conversation
- Agent with actions

## Thoughts

- Break out into multiple branches or versions to walk through
- Facit on one screen/env and then live code on another?
- Setup, Pinecone and OpenAPI keys, local Python dev env

  - How to setup local env
  - How to setup Pinecone index (1536 dimensions cosine)

- How to scrape websites
  - Cookies
  - Robots
  - Ethics
  - Clean it
- Split it
- Create embeddings
- Index

## Terminology to go through

- LLM (Large Language Model)
  - Such as GPT (Generative Pre-trained Transformer)
- Tokens
  - In the context of Large Language Models (LLMs) like GPT (Generative Pre-trained Transformer), a "token" refers to the smallest unit of text that is individually processed by the model. Tokens are often words, but they can also be parts of words, punctuation, or other elements depending on the language and tokenization method. Here's a simplified explanation:
    - Often, simple tokenization methods split the text into words where each word is considered a token. LLMs like GPT use more complex tokenization methods that can split words into smaller parts, known as subwords or wordpieces. For example, "unbelievable" might be split into "un," "believ," and "able."
    - It's common for cost and budgets to be calculated by token.
- Chunks
  - LLMs can only process a certain amount of text at a time, so we split longer texts into smaller "chunks" that fit within this limit.
  - In short, chunks in NLP are segments of text grouped for easier processing, whether that's based on their meaning, structure, or the limitations of the LLM.
- Embeddings
  - Numerical representations of objects in a lower-dimensional space
  - Transform high-dimensional data like text or images into a form that machine learning models can work with
  - They allow machines to 'understand' and operate on human language.
  - VISUALS: A 3D to 2D analogy graphic where objects from a 3D space are being projected onto a 2D plane
  - In NLP (Natural Language Processing) embeddings capture semantic meaning by placing semantically similar words closer to each other in a vector space
  - Visual Suggestion: Show a 2D scatter plot with words like "king", "queen", "man", and "woman" positioned close to each other based on their relationships.
  - An embedding is a type of vector that represents a complex object
  - When we say an embedding, we are generally referring to the vector representation of an object that is designed for use in a machine learning model
- Vector database and indexes
  Vector Databases:

Imagine you have a big library of books, but instead of words, each book is filled with numbers that describe the content. This library is like a vector database, where each book represents an item, like an image or a piece of text, that's been turned into a list of numbers called a vector. These numbers capture the essence of the item in a way that computers can understand and compare.

Now, to find a book in our library quickly, we need a system. A vector index is like a super-efficient librarian who can quickly point you to the books most similar to the one you like. It organizes the vectors in a way that speeds up the search for similar items. So, when you ask for a book on a topic, the librarian (vector index) quickly finds books with numbers that match up closest to what you're looking for.

In a computer system, when you perform a search, the vector index allows you to quickly find the most similar vectors — finding the items that are most like what you're searching for, even among millions or billions of items.

## Considerations

- Data Laws (Pinecone in US)
- Localization (the intranet is in Swedish and English, how to make it bilingual?)

## Prerequisites

- OpenAI Account
- Pinecone Account
- Python-ready (3.9+) development environment
