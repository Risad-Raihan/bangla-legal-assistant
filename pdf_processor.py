import os
import PyPDF2
import re
from typing import List, Dict
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BengaliPDFProcessor:
    """
    A class to process Bengali PDF documents for the legal RAG system
    """
    
    def __init__(self, data_path: str = "./data"):
        self.data_path = Path(data_path)
        self.processed_texts = {}
        
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from a PDF file
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n\n--- পৃষ্ঠা {page_num + 1} ---\n\n"
                            text += page_text
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1} of {pdf_path.name}: {e}")
                        continue
                        
            return self.clean_bengali_text(text)
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path.name}: {e}")
            return ""
    
    def clean_bengali_text(self, text: str) -> str:
        """
        Clean and normalize Bengali text
        """
        if not text:
            return ""
            
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove empty lines
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Fix common OCR issues with Bengali text
        text = text.replace('ি', 'ি')  # Fix some Unicode normalization issues
        text = text.replace('ী', 'ী')
        
        # Remove page headers/footers that might be repeated
        text = re.sub(r'পৃষ্ঠা\s*\d+.*?\n', '', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks for better retrieval
        """
        if not text:
            return []
            
        # Split by sentences first (Bengali sentence endings)
        sentences = re.split(r'[।৷!?]', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # If adding this sentence would exceed chunk size, save current chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                
                # Create overlap by keeping last part of current chunk
                words = current_chunk.split()
                overlap_words = words[-overlap//10:] if len(words) > overlap//10 else words
                current_chunk = " ".join(overlap_words) + " " + sentence
            else:
                current_chunk += " " + sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def process_all_pdfs(self, chunk_size: int = 1000, overlap: int = 200) -> Dict[str, List[str]]:
        """
        Process all PDF files in the data directory
        """
        all_chunks = {}
        
        if not self.data_path.exists():
            logger.error(f"Data path {self.data_path} does not exist")
            return all_chunks
            
        pdf_files = list(self.data_path.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.data_path}")
            return all_chunks
            
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            logger.info(f"Processing: {pdf_file.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_file)
            
            if not text:
                logger.warning(f"No text extracted from {pdf_file.name}")
                continue
                
            # Create chunks
            chunks = self.chunk_text(text, chunk_size, overlap)
            
            if chunks:
                # Add document metadata to each chunk
                processed_chunks = []
                for i, chunk in enumerate(chunks):
                    chunk_with_metadata = f"নথি: {pdf_file.stem}\nঅংশ: {i+1}/{len(chunks)}\n\n{chunk}"
                    processed_chunks.append(chunk_with_metadata)
                
                all_chunks[pdf_file.stem] = processed_chunks
                logger.info(f"Created {len(chunks)} chunks from {pdf_file.name}")
            else:
                logger.warning(f"No chunks created from {pdf_file.name}")
        
        return all_chunks
    
    def get_document_summary(self) -> Dict[str, Dict]:
        """
        Get summary information about processed documents
        """
        summary = {}
        
        for doc_name, chunks in self.processed_texts.items():
            total_text_length = sum(len(chunk) for chunk in chunks)
            summary[doc_name] = {
                "chunk_count": len(chunks),
                "total_length": total_text_length,
                "avg_chunk_length": total_text_length // len(chunks) if chunks else 0
            }
            
        return summary

def test_pdf_processor():
    """
    Test function to verify PDF processing works correctly
    """
    processor = BengaliPDFProcessor("./data")
    
    # Process all PDFs
    all_chunks = processor.process_all_pdfs()
    
    print(f"Processed {len(all_chunks)} documents:")
    for doc_name, chunks in all_chunks.items():
        print(f"  {doc_name}: {len(chunks)} chunks")
        if chunks:
            print(f"    Sample: {chunks[0][:100]}...")
    
    return all_chunks

if __name__ == "__main__":
    test_pdf_processor() 