# 🤖 Mini AI Chatbox

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A modular, extensible Python-based AI chatbot framework designed for learning software engineering best practices and building a professional portfolio.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

---

## 🎯 Overview

**Mini AI Chatbox** is a portfolio project demonstrating:
- ✅ Clean Architecture principles
- ✅ Modular design patterns
- ✅ Python best practices (PEP8)
- ✅ Object-Oriented Programming (OOP)
- ✅ Proper error handling and logging
- ✅ Comprehensive documentation
- ✅ Test-driven development structure
- ✅ Scalable framework design

**Purpose**: This project serves as a learning platform for software engineering concepts while creating a functional, expandable chatbot system.

---

## ✨ Features

### Current Features (Phase 1)
- 💬 **General Chat**: Natural conversation capabilities
- 🧮 **Calculator**: Mathematical operations and expressions
- 🗃️ **SQL Query Helper**: SQL syntax assistance and query generation
- 📊 **Power BI DAX Helper**: DAX formula assistance and explanations
- 📈 **SPSS Assistant**: Statistical analysis guidance

### Planned Features (Phase 2+)
- 📄 CSV/Excel Analysis
- 📑 PDF Processing
- 📊 Data Visualization
- 🧠 Advanced Memory System
- 🔐 User Authentication
- 🤖 OpenAI & Gemini Integration
- 🎤 Voice Assistant
- 🖼️ Image Analysis
- 📋 Report Generation
- 📊 Analytics Dashboard

---

## 🏗️ Architecture

This project follows **Clean Architecture** with clear separation of concerns:

```
User Interface (Streamlit)
         ↓
   Chatbot Engine
         ↓
   Intent Detector
         ↓
      Router
         ↓
   Skill Modules
         ↓
  Response Manager
         ↓
   Memory/Database
```

**Key Principles**:
- **Modularity**: Each skill is an independent module
- **Extensibility**: Add new skills without modifying core code
- **Testability**: Each component can be tested in isolation
- **Maintainability**: Clear structure and documentation

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

---

## 📁 Project Structure

```
mini_ai_chatbox/
│
├── frontend/              # User Interface Layer
│   ├── streamlit_app.py   # Main Streamlit application
│   └── assets/            # UI assets (images, CSS)
│
├── backend/               # Core Business Logic
│   ├── chatbot_engine.py  # Main chatbot controller
│   ├── router.py          # Routes requests to modules
│   ├── intent_detector.py # Detects user intent
│   ├── response_manager.py # Formats responses
│   └── exception_handler.py # Global error handling
│
├── modules/               # Skill Modules (Pluggable)
│   ├── chat/              # General conversation
│   ├── calculator/        # Math operations
│   ├── sql_helper/        # SQL assistance
│   ├── powerbi_helper/    # DAX assistance
│   ├── spss_helper/       # SPSS guidance
│   ├── analytics/         # Future: Data analysis
│   └── file_processing/   # Future: File handling
│
├── memory/                # Session & History Management
│   ├── session_manager.py # User session handling
│   └── chat_history.py    # Conversation storage
│
├── database/              # Data Persistence
│   ├── chatbot.db         # SQLite database
│   └── db_manager.py      # Database operations
│
├── config/                # Configuration Management
│   ├── settings.py        # Application settings
│   └── constants.py       # Global constants
│
├── tests/                 # Unit & Integration Tests
│   ├── test_router.py
│   ├── test_chat.py
│   └── ...
│
├── docs/                  # Documentation
│   ├── architecture.md    # Architecture details
│   ├── dependency_guide.md # Library documentation
│   ├── setup_guide.md     # Setup instructions
│   └── future_roadmap.md  # Development roadmap
│
├── logs/                  # Application Logs
│   └── chatbot.log
│
├── data/                  # User Data
│   ├── uploads/           # Uploaded files
│   ├── exports/           # Generated reports
│   └── temp/              # Temporary files
│
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mini_ai_chatbox.git
cd mini_ai_chatbox
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. **Initialize database**
```bash
python -m database.db_manager
```

---

## 💻 Usage

### Running the Application

```bash
streamlit run frontend/streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

### Example Interactions

**Calculator**:
```
User: "Calculate 25 * 4 + 10"
Bot: "The result is: 110"
```

**SQL Helper**:
```
User: "How do I join two tables in SQL?"
Bot: "Here's how to use JOIN..."
```

**DAX Helper**:
```
User: "Explain CALCULATE function in DAX"
Bot: "CALCULATE is used to..."
```

---

## 🧩 Modules

Each module is independent and follows the same interface:

| Module | Purpose | Status |
|--------|---------|--------|
| Chat | General conversation | ✅ Active |
| Calculator | Math operations | ✅ Active |
| SQL Helper | SQL assistance | ✅ Active |
| DAX Helper | Power BI DAX help | ✅ Active |
| SPSS Assistant | Statistical guidance | ✅ Active |
| CSV Analyzer | Data analysis | 🚧 Planned |
| Excel Analyzer | Excel processing | 🚧 Planned |
| PDF Reader | PDF extraction | 🚧 Planned |

---

## 🛠️ Development

### Adding a New Module

1. Create folder in `modules/`
2. Implement service class with `process()` method
3. Add module to `backend/router.py`
4. Add intent patterns to `backend/intent_detector.py`
5. Write tests in `tests/`

See [docs/setup_guide.md](docs/setup_guide.md) for detailed instructions.

### Code Style

This project follows PEP8 standards:
```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .
```

---

## 🧪 Testing

Run all tests:
```bash
pytest tests/
```

Run specific test:
```bash
pytest tests/test_router.py
```

With coverage:
```bash
pytest --cov=. tests/
```

---

## 🗺️ Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure
- [x] Core modules (Chat, Calculator, SQL, DAX, SPSS)
- [x] Basic UI
- [ ] Unit tests
- [ ] Documentation

### Phase 2: Analytics
- [ ] CSV Analyzer
- [ ] Excel Analyzer
- [ ] Data Visualization
- [ ] Report Generator

### Phase 3: Advanced Features
- [ ] PDF Processing
- [ ] Memory System
- [ ] User Authentication
- [ ] API Integration (OpenAI, Gemini)

### Phase 4: Intelligence
- [ ] Voice Assistant
- [ ] Image Analysis
- [ ] Analytics Dashboard
- [ ] Advanced NLP

See [docs/future_roadmap.md](docs/future_roadmap.md) for details.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Built as a portfolio project for university studies
- Inspired by clean architecture principles
- Designed for learning software engineering best practices

---

## 📞 Support

If you have questions or need help:
- Open an [Issue](https://github.com/yourusername/mini_ai_chatbox/issues)
- Check [Documentation](docs/)
- Contact via email

---

**⭐ If this project helped you learn, please give it a star!**
