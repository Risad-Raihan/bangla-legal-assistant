import os
import json
import pickle
import numpy as np
import faiss
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalVectorDatabase:
    """
    FAISS-based vector database for Bengali legal documents
    """
    
    def __init__(self, embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", 
                 db_path: str = "./vector_db"):
        self.embedding_model_name = embedding_model_name
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        # Initialize the embedding model
        logger.info(f"Loading embedding model: {embedding_model_name}")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # FAISS index
        self.index = None
        self.document_metadata = []  # Store document info for each embedding
        self.chunks = []  # Store original text chunks
        
        # File paths for persistence
        self.index_file = self.db_path / "faiss_index.bin"
        self.metadata_file = self.db_path / "metadata.json"
        self.chunks_file = self.db_path / "chunks.pkl"
        
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of texts
        """
        logger.info(f"Creating embeddings for {len(texts)} texts")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings.astype('float32')
    
    def build_index(self, document_chunks: Dict[str, List[str]]) -> None:
        """
        Build FAISS index from document chunks
        """
        logger.info("Building FAISS index...")
        
        # Prepare all chunks and metadata
        all_chunks = []
        all_metadata = []
        
        for doc_name, chunks in document_chunks.items():
            for chunk_idx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    'document': doc_name,
                    'chunk_index': chunk_idx,
                    'total_chunks': len(chunks)
                })
        
        if not all_chunks:
            logger.error("No chunks provided for indexing")
            return
        
        # Create embeddings
        embeddings = self.create_embeddings(all_chunks)
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        self.index.add(embeddings)
        
        # Store metadata and chunks
        self.document_metadata = all_metadata
        self.chunks = all_chunks
        
        logger.info(f"Index built with {len(all_chunks)} chunks from {len(document_chunks)} documents")
        
    def save_index(self) -> None:
        """
        Save the FAISS index and metadata to disk
        """
        if self.index is None:
            logger.error("No index to save")
            return
            
        logger.info("Saving FAISS index and metadata...")
        
        # Save FAISS index
        faiss.write_index(self.index, str(self.index_file))
        
        # Save metadata
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.document_metadata, f, ensure_ascii=False, indent=2)
        
        # Save chunks
        with open(self.chunks_file, 'wb') as f:
            pickle.dump(self.chunks, f)
            
        logger.info(f"Index saved to {self.db_path}")
    
    def load_index(self) -> bool:
        """
        Load the FAISS index and metadata from disk
        """
        try:
            if not all([self.index_file.exists(), self.metadata_file.exists(), self.chunks_file.exists()]):
                logger.warning("Index files not found")
                return False
            
            logger.info("Loading FAISS index and metadata...")
            
            # Load FAISS index
            self.index = faiss.read_index(str(self.index_file))
            
            # Load metadata
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.document_metadata = json.load(f)
            
            # Load chunks
            with open(self.chunks_file, 'rb') as f:
                self.chunks = pickle.load(f)
            
            logger.info(f"Loaded index with {len(self.chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant chunks based on query
        """
        if self.index is None:
            logger.error("Index not loaded")
            return []
        
        # Create query embedding
        query_embedding = self.create_embeddings([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx >= 0:  # Valid index
                result = {
                    'rank': i + 1,
                    'score': float(score),
                    'text': self.chunks[idx],
                    'metadata': self.document_metadata[idx],
                    'document': self.document_metadata[idx]['document'],
                    'chunk_index': self.document_metadata[idx]['chunk_index']
                }
                results.append(result)
        
        return results
    
    def get_document_info(self) -> Dict[str, int]:
        """
        Get information about indexed documents
        """
        if not self.document_metadata:
            return {}
        
        doc_counts = {}
        for metadata in self.document_metadata:
            doc_name = metadata['document']
            doc_counts[doc_name] = doc_counts.get(doc_name, 0) + 1
        
        return doc_counts
    
    def search_by_document(self, document_name: str, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search within a specific document
        """
        all_results = self.search(query, top_k * 3)  # Get more results to filter
        
        # Filter by document
        filtered_results = [
            result for result in all_results 
            if result['document'] == document_name
        ]
        
        return filtered_results[:top_k]
    
    def get_context_for_query(self, query: str, top_k: int = 5) -> str:
        """
        Get formatted context string for RAG
        """
        results = self.search(query, top_k)
        
        if not results:
            return "কোনো প্রাসঙ্গিক তথ্য পাওয়া যায়নি।"
        
        context_parts = []
        for result in results:
            doc_name = result['document']
            chunk_idx = result['chunk_index']
            text = result['text']
            score = result['score']
            
            context_part = f"""
=== {doc_name} (অংশ {chunk_idx + 1}) [সম্পর্ক: {score:.3f}] ===
{text}
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)

def test_vector_database():
    """
    Test function for the vector database
    """
    # Sample Bengali legal text for testing
    sample_chunks = {
        "সংবিধান": [
            "বাংলাদেশের সংবিধানের ২৭ ধারা অনুযায়ী আইনের দৃষ্টিতে সকল নাগরিক সমান।",
            "সংবিধানের ৩১ ধারায় আইনের আশ্রয় লাভের অধিকারের কথা বলা হয়েছে।"
        ],
        "দণ্ডবিধি": [
            "দণ্ডবিধির ৪২০ ধারায় প্রতারণার শাস্তির বিধান রয়েছে।",
            "অবৈধ দখলের ক্ষেত্রে দণ্ডবিধির ৪৪৭ ধারা প্রযোজ্য।"
        ]
    }
    
    # Initialize database
    db = LegalVectorDatabase()
    
    # Build index
    db.build_index(sample_chunks)
    
    # Test search
    results = db.search("নাগরিকদের সমান অধিকার", top_k=2)
    
    print("Search Results:")
    for result in results:
        print(f"Score: {result['score']:.3f}")
        print(f"Document: {result['document']}")
        print(f"Text: {result['text'][:100]}...")
        print("-" * 50)
    
    return db

if __name__ == "__main__":
    test_vector_database() 