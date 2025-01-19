import numpy as np
from collections import defaultdict
from typing import List, Tuple, Callable
from aimakerspace.openai_utils.embedding import EmbeddingModel
import asyncio


def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)

def jaccard_similarity(vec_1: np.ndarray, vec_2: np.ndarray) -> float:
    """
    Compute Jaccard similarity between two vectors.
    Converts vectors to binary (presence/absence) before comparison.
    Returns a value between 0 (completely different) and 1 (identical).
    """
    # Convert to binary vectors (presence/absence)
    binary_1 = vec_1 != 0
    binary_2 = vec_2 != 0
    
    # Calculate intersection and union
    intersection = np.logical_and(binary_1, binary_2).sum()
    union = np.logical_or(binary_1, binary_2).sum()
    
    # Return Jaccard similarity
    return intersection / union if union != 0 else 0.0

class VectorDatabase:
    def __init__(self, embedding_model: EmbeddingModel = None):
        self.vectors = defaultdict(np.array)
        self.metadata = {}  # New dictionary to store metadata separately
        self.embedding_model = embedding_model or EmbeddingModel()

    def insert(self, key: str, vector: np.array, metadata: dict = None) -> None:
        self.vectors[key] = vector
        if metadata:
            self.metadata[key] = metadata

    def search(
        self,
        query_vector: np.array,
        k: int,
        distance_measure: Callable = cosine_similarity,
    ) -> List[Tuple[str, float, dict]]:
        scores = []
        for key, vector in self.vectors.items():
            similarity = distance_measure(query_vector, vector)
            metadata = self.metadata.get(key, {})
            # Handle both string and dict cases
            if isinstance(key, str) and key not in self.metadata:
                metadata = {'text': key}
            scores.append((key, similarity, metadata))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:k]

    def search_by_text(
        self,
        query_text: str,
        k: int,
        distance_measure: Callable = cosine_similarity,
        return_as_text: bool = False,
    ) -> List[Tuple[str, float, dict]]:
        query_vector = self.embedding_model.get_embedding(query_text)
        results = self.search(query_vector, k, distance_measure)
        if return_as_text:
            # For each result, return the text from metadata if available, otherwise use the key
            return [(r[0], r[2].get('text', r[0]), r[2]) for r in results]
        return results

    def retrieve_from_key(self, key: str) -> np.array:
        return self.vectors.get(key, None)

    async def abuild_from_list(self, documents: List[str | dict]) -> "VectorDatabase":
        """Build database from list of documents (either strings or dicts with metadata)
        
        Args:
            documents: List of either strings or dicts containing 'text' and 'metadata' keys
        """
        # Handle both string and dict inputs
        if documents and isinstance(documents[0], dict):
            texts = [doc['text'] for doc in documents]
            embeddings = await self.embedding_model.async_get_embeddings(texts)
            for doc, embedding in zip(documents, embeddings):
                key = f"{doc['metadata']['source']}_{doc['metadata']['chunk_index']}"
                self.insert(key, np.array(embedding), metadata=doc['metadata'])
        else:
            # Original behavior for list of strings
            embeddings = await self.embedding_model.async_get_embeddings(documents)
            for text, embedding in zip(documents, embeddings):
                self.insert(text, np.array(embedding))
        
        return self


if __name__ == "__main__":
    list_of_text = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    vector_db = VectorDatabase()
    vector_db = asyncio.run(vector_db.abuild_from_list(list_of_text))
    k = 2

    searched_vector = vector_db.search_by_text("I think fruit is awesome!", k=k)
    print(f"Closest {k} vector(s):", searched_vector)

    retrieved_vector = vector_db.retrieve_from_key(
        "I like to eat broccoli and bananas."
    )
    print("Retrieved vector:", retrieved_vector)

    relevant_texts = vector_db.search_by_text(
        "I think fruit is awesome!", k=k, return_as_text=True
    )
    print(f"Closest {k} text(s):", relevant_texts)
