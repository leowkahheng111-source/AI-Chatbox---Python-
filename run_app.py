"""
============================================================================
APPLICATION LAUNCHER
============================================================================
Purpose: Simple script to launch the Mini AI Chatbox application
Usage: python run_app.py
============================================================================
"""

import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from database.db_manager import DatabaseManager


def main():
    """Launch the application."""
    print("=" * 60)
    print("🤖 MINI AI CHATBOX")
    print("=" * 60)
    print()
    
    # Initialize database
    print("📦 Initializing database...")
    try:
        db = DatabaseManager()
        print(f"✅ Database ready: {db.db_path}")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    print()
    print("🚀 Starting Streamlit application...")
    print()
    print("=" * 60)
    print("📝 Instructions:")
    print("   - The app will open in your browser automatically")
    print("   - If not, navigate to: http://localhost:8501")
    print("   - Press Ctrl+C to stop the application")
    print("=" * 60)
    print()
    
    # Launch Streamlit
    try:
        subprocess.run([
            "streamlit", "run",
            "frontend/streamlit_app.py",
            "--server.port", str(Settings.STREAMLIT_PORT)
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Streamlit is installed: pip install streamlit")
        print("2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("3. Verify you're in the project root directory")


if __name__ == "__main__":
    main()
