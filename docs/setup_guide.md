# Mini AI Chatbox - Setup Guide

## Prerequisites

Before setting up the project, ensure you have:
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning repository)

## Installation Steps

### 1. Clone or Download the Project

**Option A: Clone with Git**
```bash
git clone https://github.com/yourusername/mini_ai_chatbox.git
cd mini_ai_chatbox
```

**Option B: Download ZIP**
- Download and extract the ZIP file
- Navigate to the extracted folder

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Easy to manage and reproduce

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required libraries including:
- Streamlit (web interface)
- Pandas (data processing)
- Python-dotenv (environment variables)
- Testing frameworks

### 4. Configure Environment Variables

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` file with your settings (optional for basic usage):
```
APP_NAME=Mini AI Chatbox
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

### 5. Initialize Database

```bash
python database/db_manager.py
```

This creates:
- `database/chatbot.db` - SQLite database
- Required tables (chat_history, sessions)
- Indexes for performance

### 6. Run the Application

**Simple Method:**
```bash
python run_app.py
```

**Manual Method:**
```bash
streamlit run frontend/streamlit_app.py
```

The application will open in your default browser at: `http://localhost:8501`

## Verification

To verify everything is working:

1. **Check Application Starts**
   - Browser opens automatically
   - You see the chatbot interface

2. **Test Calculator**
   - Type: "calculate 2 + 2"
   - Expected: Response with "4"

3. **Test SQL Helper**
   - Type: "how do I use SELECT in SQL?"
   - Expected: SQL tutorial response

4. **Test General Chat**
   - Type: "hello"
   - Expected: Greeting response

## Project Structure

```
mini_ai_chatbox/
├── backend/              # Core logic
│   ├── chatbot_engine.py
│   ├── router.py
│   └── ...
├── frontend/             # User interface
│   └── streamlit_app.py
├── modules/              # Skill modules
│   ├── calculator/
│   ├── chat/
│   └── ...
├── config/               # Configuration
├── database/             # Data storage
├── logs/                 # Application logs
└── requirements.txt      # Dependencies
```

## Troubleshooting

### Issue: "streamlit: command not found"

**Solution:**
```bash
pip install streamlit
```

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install missing package individually
pip install <package-name>
```

### Issue: Database Error

**Solution:**
```bash
# Delete and recreate database
rm database/chatbot.db
python database/db_manager.py
```

### Issue: Port Already in Use

**Solution:**
```bash
# Use different port
streamlit run frontend/streamlit_app.py --server.port 8502
```

### Issue: Import Errors

**Solution:**
```bash
# Ensure you're in project root directory
cd mini_ai_chatbox

# Verify Python path
python -c "import sys; print(sys.path)"
```

## Development Setup

For development work:

### 1. Install Development Dependencies

```bash
pip install pytest pytest-cov black flake8 mypy
```

### 2. Run Tests

```bash
pytest tests/
```

### 3. Code Formatting

```bash
black .
```

### 4. Linting

```bash
flake8 .
```

### 5. Type Checking

```bash
mypy .
```

## IDE Setup

### VS Code

Create `.vscode/settings.json`:
```json
{
    "python.pythonPath": ".venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}
```

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing Environment
3. Select `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (macOS/Linux)

## Next Steps

After successful setup:

1. **Explore Features**
   - Try different modules (Calculator, SQL, DAX, SPSS)
   - Test various queries

2. **Review Documentation**
   - Read `docs/architecture.md`
   - Check module documentation

3. **Customize**
   - Modify settings in `config/settings.py`
   - Adjust constants in `config/constants.py`

4. **Extend**
   - Add new modules (see module development guide)
   - Customize UI (edit `frontend/streamlit_app.py`)

## Deployment (Future)

For production deployment:

1. **Use Production Server**
   - Gunicorn/Uvicorn for backend API
   - Nginx as reverse proxy

2. **Use Production Database**
   - PostgreSQL instead of SQLite
   - Implement connection pooling

3. **Enable Security**
   - HTTPS/SSL certificates
   - User authentication
   - Rate limiting

4. **Cloud Deployment Options**
   - Heroku
   - AWS EC2/Elastic Beanstalk
   - Google Cloud Platform
   - Azure App Service
   - Streamlit Cloud (easiest)

## Getting Help

If you encounter issues:

1. Check this guide
2. Review error logs in `logs/chatbot.log`
3. Search existing issues
4. Create new issue with:
   - Error message
   - Steps to reproduce
   - Python version
   - Operating system

## Contributing

To contribute:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

---

**Questions?** Open an issue or contact: your.email@example.com

**Last Updated**: 2024-01-01
