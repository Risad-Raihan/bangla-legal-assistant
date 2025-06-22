from pdf_processor import BengaliPDFProcessor
from vector_database import LegalVectorDatabase
from gemini_client import GeminiLegalAssistant
from config import Config
import logging
from typing import Dict, List, Optional
import os
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BangladeshLegalRAGSystem:
    """
    Complete RAG system for Bangladesh legal assistance
    """
    
    def __init__(self, api_key: Optional[str] = None, force_rebuild: bool = False):
        self.api_key = api_key
        self.force_rebuild = force_rebuild
        
        # Initialize components
        self.pdf_processor = BengaliPDFProcessor(Config.PDF_DATA_PATH)
        self.vector_db = LegalVectorDatabase(
            embedding_model_name=Config.EMBEDDING_MODEL,
            db_path=Config.VECTOR_DB_PATH
        )
        
        # Initialize Gemini client (will be done when needed to avoid API key issues)
        self.gemini_client = None
        self._initialized = False
        
    def initialize_system(self) -> bool:
        """
        Initialize the complete RAG system
        """
        try:
            logger.info("Initializing Bangladesh Legal RAG System...")
            
            # Try to load existing index first
            if not self.force_rebuild and self.vector_db.load_index():
                logger.info("Loaded existing vector database")
                self._initialized = True
                return True
            
            # If no existing index or force rebuild, process PDFs and build index
            logger.info("Building new vector database from PDF documents...")
            
            # Process all PDFs
            document_chunks = self.pdf_processor.process_all_pdfs(
                chunk_size=Config.CHUNK_SIZE,
                overlap=Config.CHUNK_OVERLAP
            )
            
            if not document_chunks:
                logger.error("No documents were processed successfully")
                return False
            
            # Build vector index
            self.vector_db.build_index(document_chunks)
            
            # Save the index for future use
            self.vector_db.save_index()
            
            logger.info("System initialization completed successfully")
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Error initializing system: {e}")
            return False
    
    def _ensure_gemini_client(self) -> bool:
        """
        Ensure Gemini client is initialized
        """
        if self.gemini_client is None:
            try:
                self.gemini_client = GeminiLegalAssistant(self.api_key)
                return True
            except Exception as e:
                logger.error(f"Error initializing Gemini client: {e}")
                return False
        return True
    
    def get_legal_advice(self, query: str, use_context: bool = True) -> Dict[str, any]:
        """
        Get comprehensive legal advice with context
        """
        if not self._initialized:
            return {
                "success": False,
                "error": "সিস্টেম এখনো প্রস্তুত নয়। অনুগ্রহ করে প্রথমে সিস্টেম ইনিশিয়ালাইজ করুন।"
            }
        
        if not self._ensure_gemini_client():
            return {
                "success": False,
                "error": "Gemini AI সেবা ব্যবহার করতে সমস্যা হচ্ছে। API key যাচাই করুন।"
            }
        
        try:
            # Get relevant context from vector database
            context = ""
            relevant_docs = []
            
            if use_context:
                search_results = self.vector_db.search(query, top_k=Config.TOP_K_RETRIEVAL)
                relevant_docs = search_results
                context = self.vector_db.get_context_for_query(query, top_k=Config.TOP_K_RETRIEVAL)
            
            # Generate legal advice using Gemini
            advice = self.gemini_client.generate_legal_advice(query, context)
            
            return {
                "success": True,
                "query": query,
                "advice": advice,
                "relevant_documents": relevant_docs,
                "context_used": context if use_context else "প্রসঙ্গ ব্যবহার করা হয়নি",
                "sources": [doc['document'] for doc in relevant_docs] if relevant_docs else []
            }
            
        except Exception as e:
            logger.error(f"Error getting legal advice: {e}")
            return {
                "success": False,
                "error": f"পরামর্শ তৈরি করতে সমস্যা হয়েছে: {str(e)}"
            }
    
    def search_documents(self, query: str, document_name: Optional[str] = None) -> List[Dict]:
        """
        Search specific documents or all documents
        """
        if not self._initialized:
            return []
        
        try:
            if document_name:
                return self.vector_db.search_by_document(document_name, query, top_k=5)
            else:
                return self.vector_db.search(query, top_k=10)
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def get_available_documents(self) -> Dict[str, int]:
        """
        Get list of available documents and their chunk counts
        """
        if not self._initialized:
            return {}
        
        return self.vector_db.get_document_info()
    
    def generate_legal_document(self, document_type: str, details: Dict[str, str]) -> Dict[str, any]:
        """
        Generate legal documents like notices, petitions etc.
        """
        if not self._ensure_gemini_client():
            return {
                "success": False,
                "error": "Gemini AI সেবা ব্যবহার করতে সমস্যা হচ্ছে।"
            }
        
        try:
            document = self.gemini_client.generate_legal_document_draft(document_type, details)
            
            return {
                "success": True,
                "document_type": document_type,
                "document": document,
                "details": details
            }
            
        except Exception as e:
            logger.error(f"Error generating document: {e}")
            return {
                "success": False,
                "error": f"দলিল তৈরি করতে সমস্যা হয়েছে: {str(e)}"
            }
    
    def analyze_case(self, case_details: str) -> Dict[str, any]:
        """
        Analyze case strength and provide recommendations
        """
        if not self._ensure_gemini_client():
            return {
                "success": False,
                "error": "Gemini AI সেবা ব্যবহার করতে সমস্যা হচ্ছে।"
            }
        
        try:
            analysis = self.gemini_client.analyze_case_strength(case_details)
            
            return {
                "success": True,
                "case_details": case_details,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing case: {e}")
            return {
                "success": False,
                "error": f"মামলা বিশ্লেষণ করতে সমস্যা হয়েছে: {str(e)}"
            }
    
    def get_system_status(self) -> Dict[str, any]:
        """
        Get comprehensive system status
        """
        status = {
            "system_initialized": self._initialized,
            "documents_available": {},
            "vector_db_status": "Not loaded",
            "gemini_status": "Not initialized"
        }
        
        if self._initialized:
            status["documents_available"] = self.get_available_documents()
            status["vector_db_status"] = f"Loaded with {sum(status['documents_available'].values())} chunks"
        
        if self._ensure_gemini_client():
            gemini_status = self.gemini_client.check_api_status()
            status["gemini_status"] = gemini_status["message"]
        
        return status
    
    def rebuild_database(self) -> bool:
        """
        Force rebuild the vector database
        """
        logger.info("Force rebuilding vector database...")
        self.force_rebuild = True
        self._initialized = False
        return self.initialize_system()

def test_rag_system():
    """
    Test the complete RAG system
    """
    print("Testing Bangladesh Legal RAG System...")
    
    # Initialize system
    rag = BangladeshLegalRAGSystem()
    
    # Initialize (this will build the database from PDFs)
    print("\n1. Initializing system...")
    if rag.initialize_system():
        print("✓ System initialized successfully")
    else:
        print("✗ System initialization failed")
        return
    
    # Check system status
    print("\n2. System Status:")
    status = rag.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Test document search
    print("\n3. Testing document search...")
    search_results = rag.search_documents("সংবিধান নাগরিক অধিকার")
    print(f"   Found {len(search_results)} relevant chunks")
    if search_results:
        print(f"   Sample: {search_results[0]['text'][:100]}...")
    
    # Test legal advice (without API key it will fail)
    print("\n4. Testing legal advice...")
    advice_result = rag.get_legal_advice("নারী নির্যাতন মামলায় প্রতিরক্ষার উপায় কি?")
    print(f"   Success: {advice_result['success']}")
    if not advice_result['success']:
        print(f"   Error: {advice_result.get('error', 'Unknown error')}")
    
    print("\nRAG System test completed!")

if __name__ == "__main__":
    test_rag_system() 