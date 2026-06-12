"""
============================================================================
STREAMLIT FRONTEND APPLICATION
============================================================================
Purpose: User interface for the Mini AI Chatbox
Usage: Run with: streamlit run frontend/streamlit_app.py
Interactions: Communicates with chatbot_engine for processing
Expansion: Add file upload, visualizations, user authentication
============================================================================
"""

# Standard Library Imports
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from datetime import datetime

# Third-Party Imports
import streamlit as st

# Internal Project Imports
from backend.chatbot_engine import ChatbotEngine, get_engine
from config.settings import Settings
from config.constants import UIConstants, ResponseType


# Configure logging
logging.basicConfig(
    level=Settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Settings.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# =============================================================================
# STREAMLIT PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title=UIConstants.PAGE_TITLE,
    page_icon=UIConstants.PAGE_ICON,
    layout=UIConstants.LAYOUT,
    initial_sidebar_state="expanded"
)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    
    Why: Streamlit reruns on every interaction, session_state persists data
    """
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'engine' not in st.session_state:
        st.session_state.engine = get_engine()
        logger.info("Chatbot engine initialized")
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def add_message_to_history(role: str, content: str):
    """
    Add a message to chat history.
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
    """
    st.session_state.chat_history.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now()
    })
    st.session_state.message_count += 1


def display_message(role: str, content: str):
    """
    Display a chat message.
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
    """
    with st.chat_message(role):
        st.markdown(content)


def get_response_style(response_type: str) -> tuple:
    """
    Get emoji and color for response type.
    
    Args:
        response_type: Type of response
        
    Returns:
        Tuple of (emoji, color)
    """
    styles = {
        ResponseType.SUCCESS.value: ("✅", "green"),
        ResponseType.ERROR.value: ("❌", "red"),
        ResponseType.WARNING.value: ("⚠️", "orange"),
        ResponseType.INFO.value: ("ℹ️", "blue"),
    }
    return styles.get(response_type, ("💬", "gray"))


def clear_chat():
    """Clear chat history."""
    st.session_state.chat_history = []
    st.session_state.message_count = 0
    logger.info("Chat history cleared")


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar():
    """Render sidebar with app information and controls."""
    with st.sidebar:
        st.title("🤖 Mini AI Chatbox")
        st.markdown("---")
        
        # About section
        st.subheader("About")
        st.info("""
        Your intelligent assistant for:
        - 💬 General conversation
        - 🧮 Math calculations
        - 🗃️ SQL queries
        - 📊 Power BI DAX
        - 📈 SPSS statistics
        """)
        
        st.markdown("---")
        
        # Available Skills
        st.subheader("📚 Available Skills")
        if st.button("Show Skills", use_container_width=True):
            response = st.session_state.engine.get_available_skills()
            st.success(response['content'])
        
        st.markdown("---")
        
        # Chat Controls
        st.subheader("⚙️ Controls")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
            st.rerun()
        
        if st.button("ℹ️ System Info", use_container_width=True):
            health = st.session_state.engine.get_health_status()
            st.json(health)
        
        st.markdown("---")
        
        # Statistics
        st.subheader("📊 Statistics")
        st.metric("Messages", st.session_state.message_count)
        st.metric("Session", st.session_state.session_id)
        
        st.markdown("---")
        
        # Footer
        st.caption("Built with ❤️ using Python & Streamlit")
        st.caption(f"Version {Settings.APP_VERSION}")


# =============================================================================
# MAIN CHAT INTERFACE
# =============================================================================

def render_chat_interface():
    """Render main chat interface."""
    
    # Title
    st.title("💬 Chat with Mini AI")
    
    # Display chat history
    for message in st.session_state.chat_history:
        display_message(message['role'], message['content'])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Display user message
        display_message("user", prompt)
        add_message_to_history("user", prompt)
        
        # Get bot response
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.engine.process_message(
                    prompt,
                    session_id=st.session_state.session_id
                )
                
                # Extract content
                response_content = response.get('content', 'No response generated')
                response_type = response.get('type', ResponseType.SUCCESS.value)
                
                # Add emoji based on response type
                emoji, _ = get_response_style(response_type)
                formatted_response = f"{emoji} {response_content}"
                
                # Display and save response
                display_message("assistant", formatted_response)
                add_message_to_history("assistant", formatted_response)
                
                # Log successful interaction
                logger.info(
                    f"Processed message successfully. "
                    f"Intent: {response.get('routing_info', {}).get('detected_intent', 'unknown')}"
                )
                
            except Exception as e:
                error_message = f"❌ An error occurred: {str(e)}"
                display_message("assistant", error_message)
                add_message_to_history("assistant", error_message)
                logger.error(f"Error processing message: {e}", exc_info=True)


# =============================================================================
# WELCOME SCREEN
# =============================================================================

def render_welcome():
    """Render welcome message for new users."""
    if st.session_state.message_count == 0:
        st.info("""
        👋 **Welcome to Mini AI Chatbox!**
        
        I'm here to help you with:
        - **Calculator**: Try "calculate 25 * 4 + 10"
        - **SQL Helper**: Ask "how do I use JOIN in SQL?"
        - **Power BI DAX**: Ask "explain CALCULATE function"
        - **SPSS**: Ask "how to run a t-test?"
        - **General Chat**: Just chat with me!
        
        Type your message below to get started! 👇
        """)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    try:
        # Initialize session state FIRST
        initialize_session_state()
        
        # Render welcome screen
        render_welcome()
        
        # Render chat interface
        render_chat_interface()
        
        # Render sidebar
        render_sidebar()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {e}", exc_info=True)
        
        if st.button("Restart Application"):
            st.rerun()


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()


# TODO: Future enhancements
# - Add file upload capability
# - Add data visualization widgets
# - Add user authentication
# - Add conversation export (PDF, TXT)
# - Add voice input/output
# - Add dark/light theme toggle
# - Add response rating system
# - Add conversation search
# - Add typing indicators
# - Add message editing
# - Add conversation branching
# - Add analytics dashboard
