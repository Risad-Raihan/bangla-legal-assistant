#!/usr/bin/env python3
"""
Setup script for Bangladesh Legal RAG Chatbot
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(step, message):
    """Print formatted step information"""
    print(f"\n{'='*60}")
    print(f"Step {step}: {message}")
    print('='*60)

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.8 or higher")
        return False

def install_dependencies():
    """Install required dependencies"""
    commands = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements.txt", "Installing dependencies from requirements.txt"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "vector_db",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_data_files():
    """Check if data files exist"""
    data_path = Path("data")
    if not data_path.exists():
        print("❌ Data directory not found!")
        return False
    
    pdf_files = list(data_path.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in data directory!")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF files in data directory:")
    for pdf_file in pdf_files:
        print(f"  • {pdf_file.name}")
    
    return True

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🧪 Testing package imports...")
    
    packages_to_test = [
        "streamlit",
        "google.generativeai",
        "faiss",
        "PyPDF2",
        "sentence_transformers",
        "numpy",
        "pandas"
    ]
    
    failed_imports = []
    
    for package in packages_to_test:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True

def create_env_template():
    """Create environment template file"""
    env_content = """# Google AI Studio API Key
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_api_key_here

# Optional: Model Configuration
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=8192
TEMPERATURE=0.7
"""
    
    env_file = Path(".env.template")
    if not env_file.exists():
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Created .env.template file")
    else:
        print("📁 .env.template already exists")

def main():
    """Main setup function"""
    print("🚀 Bangladesh Legal RAG Chatbot Setup")
    print("=====================================")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create directories
    print_step(2, "Creating necessary directories")
    create_directories()
    
    # Step 3: Install dependencies
    print_step(3, "Installing dependencies")
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check the error messages above.")
        sys.exit(1)
    
    # Step 4: Test imports
    print_step(4, "Testing package imports")
    if not test_imports():
        print("❌ Some packages failed to import. Please check the installation.")
        sys.exit(1)
    
    # Step 5: Check data files
    print_step(5, "Checking data files")
    if not check_data_files():
        print("⚠️  Warning: No PDF files found. Please add Bengali legal documents to the 'data' directory.")
    
    # Step 6: Create environment template
    print_step(6, "Creating environment template")
    create_env_template()
    
    # Final instructions
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Get your Google API Key from: https://makersuite.google.com/app/apikey")
    print("2. Either:")
    print("   a) Set GOOGLE_API_KEY environment variable, OR")
    print("   b) Enter it in the Streamlit app when prompted")
    print("3. Run the application:")
    print("   streamlit run app.py")
    print("\n4. For first-time setup, the system will:")
    print("   - Process all PDF files in the data directory")
    print("   - Create vector embeddings (this may take a few minutes)")
    print("   - Save the database for future use")
    
    print("\n🔗 Useful Commands:")
    print("   • Start app: streamlit run app.py")
    print("   • Test system: python rag_system.py")
    print("   • Process PDFs: python pdf_processor.py")
    print("   • Test vector DB: python vector_database.py")
    
    print("\n💡 Tips:")
    print("   • Add more PDF files to 'data' directory and rebuild database")
    print("   • Check logs directory for detailed error messages")
    print("   • Use Bengali fonts for better display")

if __name__ == "__main__":
    main() 