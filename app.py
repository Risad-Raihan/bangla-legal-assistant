import streamlit as st
import time
from rag_system import BangladeshLegalRAGSystem
from config import Config
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="বাংলাদেশ আইনি সহায়ক - Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Bengali fonts and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Noto Sans Bengali', sans-serif;
    }
    
    .stTitle {
        font-family: 'Noto Sans Bengali', sans-serif;
        color: #1f4e79;
        text-align: center;
        border-bottom: 3px solid #1f4e79;
        padding-bottom: 10px;
    }
    
    .legal-advice-box {
        background-color: #f8f9fa;
        border-left: 5px solid #28a745;
        padding: 20px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .sidebar .sidebar-content {
        font-family: 'Noto Sans Bengali', sans-serif;
    }
    
    .chat-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20px;
    }
    
    .assistant-message {
        background-color: #f1f8e9;
        margin-right: 20px;
        color: #1a1a1a;
    }
    
    .legal-advice-box {
        color: #1a1a1a !important;
    }
    
    .legal-advice-box h4 {
        color: #1f4e79 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
    st.session_state.system_initialized = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# Helper functions
def initialize_system(api_key=None):
    """Initialize the RAG system"""
    try:
        with st.spinner('সিস্টেম প্রস্তুত করা হচ্ছে... এটি প্রথমবার কয়েক মিনিট সময় নিতে পারে।'):
            st.session_state.rag_system = BangladeshLegalRAGSystem(api_key=api_key)
            success = st.session_state.rag_system.initialize_system()
            st.session_state.system_initialized = success
            return success
    except Exception as e:
        st.error(f"সিস্টেম ইনিশিয়ালাইজেশনে সমস্যা: {str(e)}")
        return False

def display_chat_message(message, is_user=True):
    """Display a chat message"""
    css_class = "user-message" if is_user else "assistant-message"
    icon = "👨‍💼" if is_user else "⚖️"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{icon} {'আইনজীবী' if is_user else 'আইনি সহায়ক'}:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Header
    st.markdown("""
    <h1 class="stTitle">⚖️ বাংলাদেশ আইনি সহায়ক</h1>
    <h3 style="text-align: center; color: #666; font-family: 'Noto Sans Bengali', sans-serif;">
    Legal Assistant for Bangladesh - Powered by AI
    </h3>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration and controls
    with st.sidebar:
        st.markdown("### ⚙️ সেটিংস")
        
        # Auto-initialize system if not already done
        if not st.session_state.system_initialized:
            if st.button("🚀 সিস্টেম চালু করুন", key="init_system"):
                if initialize_system():
                    st.success("✅ সিস্টেম সফলভাবে চালু হয়েছে!")
                    st.rerun()
                else:
                    st.error("❌ সিস্টেম চালু করতে সমস্যা হয়েছে")
        
        # System status
        st.markdown("### 📊 সিস্টেম স্ট্যাটাস")
        if st.session_state.system_initialized and st.session_state.rag_system:
            status = st.session_state.rag_system.get_system_status()
            
            if status["system_initialized"]:
                st.success("✅ সিস্টেম প্রস্তুত")
                
                # Document information
                docs = status["documents_available"]
                if docs:
                    st.markdown("**📚 উপলব্ধ নথি:**")
                    for doc, count in docs.items():
                        st.write(f"• {doc}: {count} অংশ")
                
                st.info(f"🔍 {status['vector_db_status']}")
                
                # Gemini status
                if "API সফলভাবে কাজ করছে" in status["gemini_status"]:
                    st.success(f"🤖 {status['gemini_status']}")
                else:
                    st.warning(f"🤖 {status['gemini_status']}")
            else:
                st.error("❌ সিস্টেম প্রস্তুত নয়")
        else:
            st.warning("⚠️ সিস্টেম এখনো চালু করা হয়নি")
        
        # Clear chat button
        if st.button("🗑️ চ্যাট ক্লিয়ার করুন"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Help section
        with st.expander("📖 সহায়তা"):
            st.markdown("""
            **কিভাবে ব্যবহার করবেন:**
            
            1. **সিস্টেম চালু করুন**: 'সিস্টেম চালু করুন' বাটনে ক্লিক করুন
            
            2. **প্রশ্ন করুন**: নিচের টেক্সট বক্সে আপনার আইনি প্রশ্ন লিখুন
            
            **প্রশ্নের উদাহরণ:**
            - নারী নির্যাতন মামলায় জামিনের নিয়ম কি?
            - জমি দখল মামলা কিভাবে করবো?
            - আইনি নোটিশ কিভাবে দিতে হয়?
            """)
    
    # Main content area
    if not st.session_state.system_initialized:
        st.markdown("""
        <div class="warning-box">
            <h3>🔧 সিস্টেম সেটআপ প্রয়োজন</h3>
            <p>আইনি সহায়ক ব্যবহার করতে প্রথমে সাইডবার থেকে 'সিস্টেম চালু করুন' বাটনে ক্লিক করুন।</p>
            <p>প্রথমবার চালু করতে কয়েক মিনিট সময় লাগতে পারে কারণ সিস্টেম সব আইনি নথি প্রক্রিয়া করবে।</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 আইনি পরামর্শ", 
        "📄 ডকুমেন্ট তৈরি", 
        "🔍 নথি খোঁজ", 
        "📊 মামলা বিশ্লেষণ"
    ])
    
    with tab1:
        st.markdown("### 💬 আইনি পরামর্শ চান")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("**আগের কথোপকথন:**")
            for entry in st.session_state.chat_history:
                display_chat_message(entry["query"], is_user=True)
                display_chat_message(entry["response"], is_user=False)
                st.markdown("---")
        
        # Input form
        with st.form("legal_advice_form"):
            user_query = st.text_area(
                "আপনার আইনি প্রশ্ন লিখুন:",
                height=100,
                placeholder="উদাহরণ: একজন তার স্ত্রীর দেয়া মিথ্যা নারী নির্যাতন মামলার সম্মুখীন। আমি একজন এডভোকেট হিসাবে কিভাবে তার মামলা সমাধান করবো?"
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                submit_button = st.form_submit_button("📤 প্রশ্ন করুন")
            with col2:
                use_context = st.checkbox("প্রাসঙ্গিক নথি ব্যবহার করুন", value=True)
        
        if submit_button and user_query.strip():
            with st.spinner('আইনি পরামর্শ তৈরি করা হচ্ছে...'):
                result = st.session_state.rag_system.get_legal_advice(user_query, use_context)
                
                if result["success"]:
                    # Display the advice
                    st.markdown(f"""
                    <div class="legal-advice-box">
                        <h4>⚖️ আইনি পরামর্শ:</h4>
                        {result["advice"].replace('\n', '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show sources if available
                    if result["sources"]:
                        st.markdown("**📚 ব্যবহৃত সূত্র:**")
                        for source in set(result["sources"]):
                            st.write(f"• {source}")
                    
                    # Save to chat history
                    st.session_state.chat_history.append({
                        "query": user_query,
                        "response": result["advice"],
                        "timestamp": datetime.now()
                    })
                    
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <h4>❌ ত্রুটি:</h4>
                        {result["error"]}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📄 আইনি ডকুমেন্ট তৈরি")
        
        document_type = st.selectbox(
            "ডকুমেন্টের ধরন নির্বাচন করুন:",
            ["Legal Notice", "Petition", "Other"]
        )
        
        if document_type == "Legal Notice":
            st.markdown("**আইনি নোটিশের তথ্য দিন:**")
            
            with st.form("legal_notice_form"):
                client_name = st.text_input("ক্লায়েন্টের নাম:")
                respondent_name = st.text_input("প্রতিপক্ষের নাম:")
                case_details = st.text_area("মামলার বিবরণ:", height=150)
                demands = st.text_area("দাবি সমূহ:", height=100)
                time_limit = st.selectbox("সময়সীমা:", ["15 দিন", "30 দিন", "অন্যান্য"])
                
                if st.form_submit_button("📄 নোটিশ তৈরি করুন"):
                    details = {
                        "client_name": client_name,
                        "respondent_name": respondent_name,
                        "case_details": case_details,
                        "demands": demands,
                        "time_limit": time_limit
                    }
                    
                    with st.spinner('আইনি নোটিশ তৈরি করা হচ্ছে...'):
                        result = st.session_state.rag_system.generate_legal_document("legal_notice", details)
                        
                        if result["success"]:
                            st.markdown("### 📄 তৈরিকৃত আইনি নোটিশ:")
                            st.text_area("", value=result["document"], height=400)
                        else:
                            st.error(result["error"])
    
    with tab3:
        st.markdown("### 🔍 নথি অনুসন্ধান")
        
        search_query = st.text_input(
            "খুঁজতে চান:",
            placeholder="উদাহরণ: সংবিধান নাগরিক অধিকার"
        )
        
        available_docs = st.session_state.rag_system.get_available_documents()
        doc_filter = st.selectbox(
            "নির্দিষ্ট নথি (ঐচ্ছিক):",
            ["সব নথি"] + list(available_docs.keys())
        )
        
        if st.button("🔍 খুঁজুন") and search_query:
            doc_name = None if doc_filter == "সব নথি" else doc_filter
            
            with st.spinner('অনুসন্ধান করা হচ্ছে...'):
                results = st.session_state.rag_system.search_documents(search_query, doc_name)
                
                if results:
                    st.markdown(f"**📋 {len(results)}টি ফলাফল পাওয়া গেছে:**")
                    
                    for i, result in enumerate(results, 1):
                        with st.expander(f"ফলাফল {i}: {result['document']} (স্কোর: {result['score']:.3f})"):
                            st.write(result['text'])
                else:
                    st.warning("কোনো ফলাফল পাওয়া যায়নি।")
    
    with tab4:
        st.markdown("### 📊 মামলা বিশ্লেষণ")
        
        with st.form("case_analysis_form"):
            case_details = st.text_area(
                "মামলার বিস্তারিত বিবরণ দিন:",
                height=200,
                placeholder="মামলার ধরন, ঘটনার বিবরণ, প্রমাণ, সাক্ষী ইত্যাদি সম্পর্কে বিস্তারিত লিখুন..."
            )
            
            if st.form_submit_button("📊 বিশ্লেষণ করুন"):
                if case_details.strip():
                    with st.spinner('মামলা বিশ্লেষণ করা হচ্ছে...'):
                        result = st.session_state.rag_system.analyze_case(case_details)
                        
                        if result["success"]:
                            st.markdown("### 📊 মামলা বিশ্লেষণ:")
                            st.markdown(f"""
                            <div class="legal-advice-box">
                                {result["analysis"].replace('\n', '<br>')}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(result["error"])
                else:
                    st.warning("মামলার বিবরণ দিন।")

if __name__ == "__main__":
    main() 