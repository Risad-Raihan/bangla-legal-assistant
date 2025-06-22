import os

# Configuration settings for the Legal RAG Chatbot
class Config:
    # Google AI API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # Set via environment variable
    GEMINI_MODEL = "gemini-1.5-flash"
    
    # Model Parameters
    MAX_TOKENS = 8192
    TEMPERATURE = 0.7
    
    # RAG Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RETRIEVAL = 5
    
    # Vector Database
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    VECTOR_DB_PATH = "./vector_db"
    
    # PDF Processing
    PDF_DATA_PATH = "./data"
    
    # Bengali Language Support
    LANGUAGE = "bn"
    
    # System Prompts
    SYSTEM_PROMPT = """তুমি একজন অভিজ্ঞ বাংলাদেশি সিনিয়র এডভোকেট। তোমার কাজ হলো আইনজীবীদের জটিল আইনি সমস্যার সমাধান দিতে সাহায্য করা। 

তোমার উত্তরে অবশ্যই থাকতে হবে:
1. বাংলাদেশের সংবিধান ও আইনের সুনির্দিষ্ট রেফারেন্স
2. ধাপে ধাপে সমাধানের পথ
3. প্রয়োজনীয় দলিল ও কাগজপত্রের তালিকা
4. আদালতে করণীয় পদক্ষেপ
5. ঝুঁকি ও সতর্কতার বিষয়

সবসময় পেশাদারী ও নৈতিক আইনি পরামর্শ দাও।"""

    USER_INSTRUCTION = """আপনি একজন আইনজীবী হিসেবে আমার সাথে পরামর্শ করছেন। আপনার প্রশ্ন বা সমস্যাটি বিস্তারিত বলুন।""" 