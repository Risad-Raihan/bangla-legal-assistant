#!/usr/bin/env python3
"""
Quick Start Script for Bangladesh Legal RAG Assistant
"""

import sys
import os
import subprocess

def main():
    """Main function to run the application"""
    
    print("🏛️ Bangladesh Legal RAG Assistant")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'setup':
            print("⚙️ Running setup...")
            subprocess.run([sys.executable, "setup.py"])
            
        elif command == 'test':
            print("🧪 Testing system...")
            subprocess.run([sys.executable, "rag_system.py"])
            
        elif command == 'clean':
            print("🧹 Cleaning cache...")
            import shutil
            from pathlib import Path
            
            dirs_to_clean = ["vector_db", "__pycache__", ".streamlit"]
            for dir_path in dirs_to_clean:
                if Path(dir_path).exists():
                    shutil.rmtree(dir_path)
                    print(f"Cleaned {dir_path}")
            
        elif command == 'help':
            print("""
Available commands:
  start    - Start the application (default)
  setup    - Run system setup
  test     - Test the system
  clean    - Clean cache files
  help     - Show this help
            """)
            return
            
        else:
            print(f"Unknown command: {command}")
            print("Use 'python run.py help' for available commands")
            return
    
    else:
        # Default: start the application
        print("🚀 Starting application...")
        print("💡 Opening in browser at http://localhost:8501")
        print("📝 Remember to add your Google API Key!")
        print()
        
        try:
            subprocess.run(["streamlit", "run", "app.py"])
        except KeyboardInterrupt:
            print("\n👋 Application stopped")
        except Exception as e:
            print(f"\n❌ Error starting app: {e}")
            print("Try running: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 