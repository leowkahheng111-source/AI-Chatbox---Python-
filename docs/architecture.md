# Mini AI Chatbox - Architecture Documentation

## Overview

This document provides detailed architecture information for the Mini AI Chatbox project.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Frontend Layer                         │
│              (Streamlit Web Interface)                  │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              Chatbot Engine                             │
│         (Main Orchestration Layer)                      │
└──────────────────┬──────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │               │
┌───▼───┐    ┌────▼────┐    ┌────▼─────┐
│Router │    │ Intent  │    │Response  │
│       │    │Detector │    │ Manager  │
└───┬───┘    └─────────┘    └──────────┘
    │
    ├─────┬─────┬─────┬─────┬─────┐
    │     │     │     │     │     │
┌───▼──┐┌─▼──┐┌─▼──┐┌─▼──┐┌─▼──┐│
│Chat  ││Calc││SQL ││DAX ││SPSS││
│Module││    ││    ││    ││    ││
└──────┘└────┘└────┘└────┘└────┘│
                                 │
            ┌────────────────────┘
            │
    ┌───────┴────────┐
┌───▼────┐    ┌──────▼──┐
│Database│    │  Memory │
│Manager │    │ Manager │
└────────┘    └─────────┘
```

## Design Patterns Used

### 1. Clean Architecture
- Separation of concerns across layers
- Independence of frameworks
- Testable business logic

### 2. Facade Pattern
- ChatbotEngine provides simple interface to complex subsystems
- ResponseManager simplifies response creation

### 3. Router Pattern
- Central routing mechanism for module selection
- Easy to add new modules without changing core code

### 4. Factory Pattern
- Module instances created and managed by router
- Flexible module registration

### 5. Strategy Pattern
- Different intent detection strategies
- Interchangeable module implementations

## Component Responsibilities

### Frontend Layer
**File**: `frontend/streamlit_app.py`

**Responsibilities**:
- User interface rendering
- User input handling
- Response display
- Session state management

**Future Enhancements**:
- File upload interface
- Data visualization widgets
- User authentication UI

### Backend Layer

#### Chatbot Engine
**File**: `backend/chatbot_engine.py`

**Responsibilities**:
- Main entry point for all operations
- Subsystem coordination
- Session lifecycle management

#### Router
**File**: `backend/router.py`

**Responsibilities**:
- Route requests to appropriate modules
- Module registration and management
- Handle unavailable modules

#### Intent Detector
**File**: `backend/intent_detector.py`

**Responsibilities**:
- Analyze user input
- Determine appropriate module
- Provide confidence scores

#### Response Manager
**File**: `backend/response_manager.py`

**Responsibilities**:
- Format responses consistently
- Add metadata
- Handle different response types

### Module Layer

Each module follows the same interface:
```python
class ModuleService:
    def process(self, user_input: str, session_id: Optional[str]) -> str:
        # Process input and return response
        pass
```

**Current Modules**:
1. Chat Service - General conversation
2. Calculator Service - Mathematical operations
3. SQL Service - SQL assistance
4. DAX Service - Power BI help
5. SPSS Service - Statistical guidance

### Data Layer

#### Database Manager
**File**: `database/db_manager.py`

**Responsibilities**:
- SQLite database operations
- Chat history persistence
- Session management

**Tables**:
- `chat_history` - Conversation messages
- `sessions` - User sessions

## Configuration Management

**Files**: 
- `config/settings.py` - Application settings
- `config/constants.py` - Global constants

**Pattern**: Centralized configuration
- Environment variables via `.env`
- Type-safe constants
- Easy to modify without code changes

## Error Handling

**File**: `backend/exception_handler.py`

**Strategy**:
- Custom exception hierarchy
- Centralized error handling
- User-friendly error messages
- Detailed logging for debugging

## Data Flow

### User Message Processing Flow

1. **User Input** → Frontend captures message
2. **Streamlit App** → Calls `engine.process_message()`
3. **Chatbot Engine** → Routes to Router
4. **Intent Detector** → Analyzes input, determines module
5. **Router** → Selects and calls appropriate module
6. **Module** → Processes request, returns result
7. **Response Manager** → Formats response
8. **Database** → Saves conversation (optional)
9. **Frontend** → Displays formatted response

### Module Registration Flow

1. **Chatbot Engine** → Initializes Router
2. **Engine** → Imports all module classes
3. **Engine** → Creates module instances
4. **Engine** → Calls `router.register_module()` for each
5. **Router** → Stores module in registry
6. **System** → Ready to handle requests

## Scalability Considerations

### Current Implementation
- Single-process application
- SQLite database
- In-memory session state

### Future Scaling Options

**Horizontal Scaling**:
- Move to PostgreSQL/MySQL
- Implement Redis for session state
- Use message queue for async processing

**Performance**:
- Cache frequent queries
- Lazy load modules
- Implement connection pooling

**Features**:
- Multi-user support
- Real-time collaboration
- Cloud deployment (AWS, Azure, GCP)

## Security Considerations

### Current Measures
- Input validation
- Safe expression evaluation (Calculator)
- No raw `eval()` usage
- SQL parameterized queries

### Future Enhancements
- User authentication
- API key management
- Rate limiting
- Input sanitization
- HTTPS enforcement

## Testing Strategy

### Unit Tests
- Test individual functions
- Mock external dependencies
- Fast execution

### Integration Tests
- Test module interactions
- Test router → module flow
- Database operations

### End-to-End Tests
- Test complete user flows
- UI interaction testing
- Real database testing

## Deployment

### Development
```bash
streamlit run frontend/streamlit_app.py
```

### Production Considerations
- Use production WSGI server
- Enable HTTPS
- Configure proper logging
- Set up monitoring
- Implement backup strategy

## Monitoring & Logging

### Logging Levels
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical issues

### Log Files
- `logs/chatbot.log` - Application logs
- Rotation policy (future)
- Centralized logging (future)

## Future Architecture Enhancements

1. **Microservices**: Split modules into independent services
2. **API Layer**: RESTful API for frontend-backend communication
3. **Caching**: Redis for response caching
4. **Queue System**: RabbitMQ/Celery for async tasks
5. **Container**: Docker for consistent deployment
6. **Orchestration**: Kubernetes for scaling
7. **CI/CD**: Automated testing and deployment

## Conclusion

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Easy to extend with new modules
- ✅ Testable components
- ✅ Maintainable codebase
- ✅ Professional structure for portfolio

---

**Last Updated**: 2024-01-01  
**Version**: 1.0.0  
**Author**: Your Name
