"""
============================================================================
DATABASE MANAGER
============================================================================
Purpose: Handle database operations for chat history and user data
Usage: from database.db_manager import DatabaseManager
Interactions: Used by chatbot_engine and memory modules
Expansion: Add user management, analytics, session persistence
============================================================================
"""

# Standard Library Imports
import sqlite3
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path

# Internal Project Imports
from config.settings import Settings
from backend.exception_handler import DatabaseException


# Configure logger
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages SQLite database operations.
    
    Why this exists:
        - Persist chat conversations
        - Store user preferences
        - Track usage analytics
        - Session management
    
    Current Tables:
        - chat_history: Conversation messages
        - sessions: User sessions
        
    Future Tables:
        - users: User accounts
        - preferences: User settings
        - analytics: Usage metrics
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or Settings.DATABASE_PATH
        self.logger = logging.getLogger(__name__)
        
        # Ensure database directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._initialize_database()
    
    def _initialize_database(self):
        """
        Create database tables if they don't exist.
        
        Why: Ensures database schema is ready on first run
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create chat_history table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        user_id TEXT,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        module_used TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        user_id TEXT,
                        start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                        message_count INTEGER DEFAULT 0
                    )
                ''')
                
                # Create indexes for better query performance
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_chat_session 
                    ON chat_history(session_id)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_chat_timestamp 
                    ON chat_history(timestamp)
                ''')
                
                conn.commit()
                self.logger.info(f"Database initialized: {self.db_path}")
                
        except sqlite3.Error as e:
            raise DatabaseException(
                f"Failed to initialize database: {str(e)}",
                details={"db_path": self.db_path}
            )
    
    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        module_used: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> int:
        """
        Save a chat message to database.
        
        Args:
            session_id: Session identifier
            role: 'user' or 'assistant'
            content: Message content
            module_used: Module that processed this message
            user_id: Optional user identifier
            
        Returns:
            Message ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO chat_history 
                    (session_id, user_id, role, content, module_used)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session_id, user_id, role, content, module_used))
                
                message_id = cursor.lastrowid
                conn.commit()
                
                # Update session activity
                self._update_session_activity(session_id, user_id)
                
                return message_id
                
        except sqlite3.Error as e:
            raise DatabaseException(
                f"Failed to save message: {str(e)}",
                details={"session_id": session_id}
            )
    
    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve chat history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if limit:
                    cursor.execute('''
                        SELECT * FROM chat_history
                        WHERE session_id = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (session_id, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM chat_history
                        WHERE session_id = ?
                        ORDER BY timestamp ASC
                    ''', (session_id,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except sqlite3.Error as e:
            raise DatabaseException(
                f"Failed to retrieve session history: {str(e)}",
                details={"session_id": session_id}
            )
    
    def _update_session_activity(
        self,
        session_id: str,
        user_id: Optional[str] = None
    ):
        """Update session last activity time."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if session exists
                cursor.execute(
                    'SELECT id FROM sessions WHERE session_id = ?',
                    (session_id,)
                )
                
                if cursor.fetchone():
                    # Update existing session
                    cursor.execute('''
                        UPDATE sessions
                        SET last_activity = CURRENT_TIMESTAMP,
                            message_count = message_count + 1
                        WHERE session_id = ?
                    ''', (session_id,))
                else:
                    # Create new session
                    cursor.execute('''
                        INSERT INTO sessions (session_id, user_id)
                        VALUES (?, ?)
                    ''', (session_id, user_id))
                
                conn.commit()
                
        except sqlite3.Error as e:
            self.logger.error(f"Failed to update session: {e}")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

_global_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get or create global database manager instance."""
    global _global_db_manager
    
    if _global_db_manager is None:
        _global_db_manager = DatabaseManager()
    
    return _global_db_manager


# =============================================================================
# DATABASE INITIALIZATION SCRIPT
# =============================================================================

if __name__ == "__main__":
    """Run this script to initialize the database."""
    print("Initializing database...")
    db = DatabaseManager()
    print(f"Database initialized successfully at: {db.db_path}")
    print("Tables created: chat_history, sessions")


# TODO: Future enhancements
# - Add user management (registration, authentication)
# - Add analytics tables (module usage, response times)
# - Add user preferences storage
# - Implement database migrations
# - Add data export functionality
# - Implement database backup/restore
# - Add full-text search for chat history
# - Implement data retention policies
