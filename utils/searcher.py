import os
import faiss
import numpy as np
import torch
import pickle  # For saving/loading additional data like paragraphs
from transformers import AutoTokenizer, AutoModel

from dotenv import load_dotenv
load_dotenv()

class EntitySearcher:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", index_path="faiss_index"):
        self.__tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.__model = AutoModel.from_pretrained(model_name)
        self.__index_path = os.path.join(os.environ["INDEX_DIR"], index_path)
        self.__paragraphs = []
        self.__embeddings = []
        self.__index = None

    def __embed_text(self, text: str):
        """
        Generate embeddings for a given text.
        """
        inputs = self.__tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding="max_length")
        with torch.no_grad():
            outputs = self.__model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).squeeze(0).cpu().numpy()

    def __save_index(self):
        """
        Save the FAISS index and paragraphs to disk.
        """
        faiss.write_index(self.__index, f"{self.__index_path}.faiss")
        with open(f"{self.__index_path}_paragraphs.pkl", "wb") as f:
            pickle.dump(self.__paragraphs, f)
        print("Index and paragraphs saved.")

    def __load_index(self) -> bool:
        """
        Load the FAISS index and paragraphs from disk.
        """
        if os.path.exists(f"{self.__index_path}.faiss") and os.path.exists(f"{self.__index_path}_paragraphs.pkl"):
            self.__index = faiss.read_index(f"{self.__index_path}.faiss")
            with open(f"{self.__index_path}_paragraphs.pkl", "rb") as f:
                self.__paragraphs = pickle.load(f)
            print("Index and paragraphs loaded.")
            return True
        return False

    def __process_document(self, document: str) -> None:
        """
        Split the document into paragraphs and create embeddings.
        """
        self.__paragraphs = [p.strip() for p in document.split("\n") if p.strip()]
        self.__embeddings = np.array([self.__embed_text(p) for p in self.__paragraphs]).astype("float32")

    def __build_index(self) -> None:
        """
        Build a FAISS index from paragraph embeddings.
        """
        self.__index = faiss.IndexFlatL2(self.__embeddings.shape[1])
        self.__index.add(self.__embeddings)

    def prepare_index(self, document: str) -> None:
        """
        Prepare the FAISS index by loading it or creating it if necessary.
        """
        if not self.__load_index():
            print("No existing index found. Creating a new one...")
            self.__process_document(document)
            self.__build_index()
            self.__save_index()

    def search_entity(self, query: str, top_k: int = 3) -> list:
        """
        Search for the top matching paragraph(s) for a given query.
        """
        query_embedding = self.__embed_text(query).reshape(1, -1).astype("float32")
        distances, indices = self.__index.search(query_embedding, top_k)
        results = [(self.__paragraphs[idx], distances[0, i]) for i, idx in enumerate(indices[0]) if idx < len(self.__paragraphs)]
        return results

# Example Usage
if __name__ == "__main__":
    document = """
    Elon Musk is the CEO of SpaceX. The company focuses on space exploration.
    
    SpaceX was founded in 2002 and has revolutionized the space industry.
    
    Tesla is another company led by Elon Musk, focusing on electric vehicles and renewable energy.
    
    The Boring Company, Neuralink, and OpenAI are also among Elon Musk's ventures.
    """
    query = "SpaceX"

    # Initialize searcher
    searcher = EntitySearcher(index_path="space_index")

    # Prepare the index (load existing or create new)
    searcher.prepare_index(document)

    # Search for the entity
    results = searcher.search_entity(query)

    # Output results
    print("Top Matching Paragraph(s):")
    for text, distance in results:
        print(f"\nParagraph: {text}\nDistance: {distance}")