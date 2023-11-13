# Building a RAG Application: Leveraging LLMs for Internal Knowledge Queries

## Introduction to Large Language Models (LLMs)

### What are LLMs?

Large Language Models (LLMs), like the widely recognized GPT (Generative Pre-trained Transformer), represent the forefront of natural language processing technology. They are sophisticated algorithms designed to understand, interpret, and generate human-like text.

GPT, a prominent example, has revolutionized how we interact with machine intelligence, offering capabilities that range from simple Q&A formats to generating complex, contextually relevant content.

### But how?

#### **Some** **WORDS** are **more IMPORTANT** than **OTHERS**.

The Transformer Architecture was introduced in the paper ["Attention is All You Need"](https://arxiv.org/abs/1706.03762) in 2017. Transformers use a mechanism called self-attention to process words in relation to all other words in a sentence, enabling the model to capture context more effectively.

#### Attention is All You Need.

In traditional models, the significance of a word was often determined by its position in a sentence or its relation to a few neighboring words. The transformer architecture's self-attention mechanism allows the model to weigh the significance of each word in the context of every other word in a sentence. This means that the model can determine more nuanced meanings and relationships, making it better at understanding context and less reliant on the sequential position of words.

#### Data, data and more data. And then some more data.

GPT models are notable for their large scale in terms of both model size (number of parameters) and training data. Each successive version of GPT has dramatically increased the number of parameters (GPT-3 and GPT-4, for example, both have around 175 billion parameters), allowing the model to capture more nuances of language.

## Understanding Tokens in LLMs

### Defining Tokens in LLM Context

In the realm of Large Language Models like GPT, a 'token' is essentially the smallest unit of text processed independently by the model. While tokens are commonly whole words, they can also be fragments of words, punctuation marks, or other textual elements, varying based on the language and the specific tokenization technique used.

### Tokenization Techniques

Standard tokenization might simply break down text into its constituent words. However, the more advanced methods employed by LLMs, such as GPT, delve deeper, dividing words into smaller segments known as subwords or wordpieces. For instance, the word "unbelievable" could be segmented into "un," "believ," and "able."

### Implications for Cost and Resource Allocation

In the context of LLM usage, it's essential to note that operational costs and resource allocation are often calculated based on the number of tokens processed. This underscores the significance of understanding tokenization for effective budget management.

## The Concept of Chunks in NLP

LLMs can only process a certain amount of text at a time, so we split longer texts into smaller "chunks" that fit within this limit.

- In short, chunks in NLP are segments of text grouped for easier processing, whether that's based on their meaning, structure, or the limitations of the LLM.

## Demystifying Embeddings in NLP

Embeddings are numerical representations of objects in a lower-dimensional space. They are used to transform high-dimensional data (hey, remember chunks?) like text or images into a form that machine learning models can work with.

This process is called "Dimensionality Reduction".

![A 3D object casting a 2D shadow unto a plane.](./images/dimensionality_reduction.png "A 3D object casting a 2D shadow unto a plane.")

### Visualizing Embeddings

An embedding is a type of vector that represents a complex object. When we say an embedding, we are generally referring to the vector representation of an object that is designed for use in a machine learning model.

They allow machines to 'understand' and operate on human language.

- In NLP (Natural Language Processing) embeddings capture semantic meaning by placing semantically similar words closer to each other in a vector space

![Word embeddings map](./images/embeddings_and_vectors.png "Word embeddings map")

Image Source: [David Rozado, "Wide range screening of algorithmic bias in word embedding models using large sentiment lexicons reveals underreported bias types"](https://www.researchgate.net/figure/Word-embeddings-map-words-in-a-corpus-of-text-to-vector-space-Linear-combinations-of_fig6_340825443). Licensed under [CC BY](https://creativecommons.org/licenses/by/4.0/). ResearchGate, April 2020.

### Vector Databases and Their Role

A type of database designed for efficiently storing and querying high-dimensional vectors, which are often used in machine learning models, particularly for similarity search in the context of tasks like recommendation systems, image recognition, and natural language processing.

Imagine you have a big library of books, but instead of words, each book is filled with numbers that describe the content. This library is like a vector database, where each book represents an item, like an image or a piece of text, that's been turned into a list of numbers called a vector. These numbers capture the essence of the item in a way that computers can understand and compare.

#### The Vector Index Explained

Now, to find a book in our library quickly, we need a system. A vector index is like a super-efficient librarian who can quickly point you to the books most similar to the one you like. It organizes the vectors in a way that speeds up the search for similar items. So, when you ask for a book on a topic, the librarian (vector index) quickly finds books with numbers that match up closest to what you're looking for.

In a computer system, when you perform a search, the vector index allows you to quickly find the most similar vectors — finding the items that are most like what you're searching for, even among millions or billions of items.

## Beyond ChatGPT: Harnessing Business Knowledge

### Limitations of Public Internet Models

While ChatGPT showcases impressive capabilities in understanding and generating language, its knowledge is inherently limited to what is available publicly on the internet. This means it lacks access to the wealth of information stored in private intranets or confidential internal company documents.

### The RAG Advantage

Enter the RAG (Retrieval-Augmented Generation) approach. RAG stands as a solution designed to bridge this gap. It extends beyond the realm of public internet knowledge, enabling the incorporation of specialized, company-specific information stored in private databases and intranets.

## Unveiling RAG: A New Era of Customized Knowledge Applications

### What is a RAG Application?

A RAG (Retrieval-Augmented Generation) application is an advanced AI system that combines the power of two key components: a retrieval mechanism and a generative language model. This dual approach allows the system to pull in relevant information from a specific dataset (like an intranet database) and then generate responses or content based on that information.

### Customized Knowledge at Your Fingertips

The real power of RAG lies in its ability to tailor its responses to include specific, internal knowledge that a standard model like ChatGPT wouldn't have access to. This makes RAG applications incredibly valuable for businesses looking to leverage their unique data repositories for more informed, accurate, and context-specific interactions.
