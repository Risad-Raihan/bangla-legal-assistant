import google.generativeai as genai
from typing import Optional, Dict, List
import logging
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiLegalAssistant:
    """
    Gemini AI client for Bengali legal assistance
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GOOGLE_API_KEY
        
        if not self.api_key:
            raise ValueError("""
            Google API Key not provided! 
            
            Please set your API key in one of these ways:
            1. Set GOOGLE_API_KEY environment variable
            2. Pass api_key parameter when creating GeminiLegalAssistant
            3. Add your key in config.py
            
            Get your API key from: https://makersuite.google.com/app/apikey
            """)
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model_name = Config.GEMINI_MODEL
        self.model = genai.GenerativeModel(self.model_name)
        
        # Generation configuration
        self.generation_config = {
            "temperature": Config.TEMPERATURE,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": Config.MAX_TOKENS,
        }
        
        logger.info(f"Initialized Gemini Legal Assistant with model: {self.model_name}")
    
    def generate_legal_advice(self, query: str, context: str = "") -> str:
        """
        Generate legal advice using RAG context
        """
        # Construct the prompt with context and system instructions
        prompt = self._build_legal_prompt(query, context)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "দুঃখিত, এই মুহূর্তে আমি আপনার প্রশ্নের উত্তর দিতে পারছি না। অনুগ্রহ করে আবার চেষ্টা করুন।"
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"দুঃখিত, একটি ত্রুটি ঘটেছে: {str(e)}"
    
    def _build_legal_prompt(self, query: str, context: str) -> str:
        """
        Build a comprehensive legal prompt with context
        """
        prompt = f"""
{Config.SYSTEM_PROMPT}

নিম্নলিখিত প্রাসঙ্গিক আইনি তথ্য ব্যবহার করে প্রশ্নের উত্তর দাও:

=== প্রাসঙ্গিক আইনি তথ্য ===
{context if context else "কোনো সুনির্দিষ্ট প্রাসঙ্গিক তথ্য পাওয়া যায়নি।"}

=== আইনজীবীর প্রশ্ন ===
{query}

=== নির্দেশনা ===
1. উপরের প্রাসঙ্গিক তথ্য থেকে সুনির্দিষ্ট রেফারেন্স দাও
2. বাংলাদেশের সংবিধান ও আইনের ধারা উল্লেখ করো
3. ধাপে ধাপে সমাধানের পথ বলো
4. প্রয়োজনীয় দলিল ও কাগজপত্রের তালিকা দাও
5. আদালতে করণীয় সম্পর্কে বিস্তারিত পরামর্শ দাও
6. সতর্কতা ও ঝুঁকির বিষয়গুলো উল্লেখ করো

তোমার উত্তর অবশ্যই পেশাদারী, নিখুঁত এবং বাস্তব প্রয়োগযোগ্য হতে হবে।
"""
        return prompt
    
    def check_api_status(self) -> Dict[str, str]:
        """
        Check if the API is working properly
        """
        try:
            test_response = self.model.generate_content(
                "পরীক্ষা: 'বাংলাদেশ' শব্দটি বাংলায় লিখো।",
                generation_config={"max_output_tokens": 50}
            )
            
            if test_response.text:
                return {
                    "status": "success",
                    "message": "API সফলভাবে কাজ করছে",
                    "test_response": test_response.text.strip()
                }
            else:
                return {
                    "status": "error",
                    "message": "API থেকে কোনো উত্তর পাওয়া যায়নি"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"API ত্রুটি: {str(e)}"
            }
    
    def generate_legal_document_draft(self, document_type: str, details: Dict[str, str]) -> str:
        """
        Generate legal document drafts (notices, petitions, etc.)
        """
        if document_type.lower() == "legal_notice":
            return self._generate_legal_notice(details)
        elif document_type.lower() == "petition":
            return self._generate_petition(details)
        else:
            return "দুঃখিত, এই ধরনের দলিল তৈরির সুবিধা এখনো যোগ করা হয়নি।"
    
    def _generate_legal_notice(self, details: Dict[str, str]) -> str:
        """
        Generate a legal notice draft
        """
        prompt = f"""
একটি আইনি নোটিশের ড্রাফট তৈরি করো নিম্নলিখিত তথ্যের ভিত্তিতে:

বিবরণ:
{details}

নোটিশটি অবশ্যই:
1. বাংলাদেশের আইনের সাথে সামঞ্জস্যপূর্ণ হতে হবে
2. প্রয়োজনীয় আইনি ধারা উল্লেখ করতে হবে
3. পেশাদারী ভাষায় লেখা হতে হবে
4. সুনির্দিষ্ট সময়সীমা উল্লেখ করতে হবে

উচ্চমানের আইনি নোটিশ তৈরি করো।
"""
        
        try:
            response = self.model.generate_content(prompt, generation_config=self.generation_config)
            return response.text if response.text else "নোটিশ তৈরি করতে সমস্যা হয়েছে।"
        except Exception as e:
            return f"ত্রুটি: {str(e)}"
    
    def analyze_case_strength(self, case_details: str) -> str:
        """
        Analyze the strength of a legal case
        """
        prompt = f"""
নিম্নলিখিত মামলার বিবরণ বিশ্লেষণ করে মামলার শক্তি-দুর্বলতা মূল্যায়ন করো:

মামলার বিবরণ:
{case_details}

বিশ্লেষণে অন্তর্ভুক্ত করো:
1. মামলার আইনি ভিত্তি
2. প্রমাণের শক্তি
3. সফল হওয়ার সম্ভাবনা
4. ঝুঁকিসমূহ
5. প্রতিপক্ষের সম্ভাব্য আর্গুমেন্ট
6. উন্নতির সুপারিশ

বাংলাদেশের আইনের প্রেক্ষিতে বিশ্লেষণ করো।
"""
        
        try:
            response = self.model.generate_content(prompt, generation_config=self.generation_config)
            return response.text if response.text else "বিশ্লেষণ করতে সমস্যা হয়েছে।"
        except Exception as e:
            return f"ত্রুটি: {str(e)}"

def test_gemini_client():
    """
    Test function for Gemini client
    """
    try:
        # Note: This will fail without a valid API key
        client = GeminiLegalAssistant()
        
        # Test API status
        status = client.check_api_status()
        print(f"API Status: {status}")
        
        # Test legal advice generation
        test_query = "নারী নির্যাতন মামলায় জামিনের নিয়ম কি?"
        test_context = "দণ্ডবিধির ৪৯৭ ধারা অনুযায়ী জামিনের বিধান রয়েছে।"
        
        response = client.generate_legal_advice(test_query, test_context)
        print(f"Response: {response[:200]}...")
        
    except Exception as e:
        print(f"Test failed: {e}")
        print("Note: You need to set up your Google API key first.")

if __name__ == "__main__":
    test_gemini_client() 