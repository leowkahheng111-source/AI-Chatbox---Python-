# Mini AI Chatbox - Dependency Guide

## Complete Library Documentation

This document explains every external library used in the project.

---

## 📦 Core Dependencies

### 1. Streamlit
**Version**: 1.29.0  
**Purpose**: Web-based user interface framework  
**Files Using**: `frontend/streamlit_app.py`

**Import Statement:**
```python
import streamlit as st
```

**Why Chosen:**
- Quick prototyping and deployment
- Built-in chat interface components
- No HTML/CSS/JavaScript required
- Perfect for data applications
- Active community and documentation

**Alternatives:**
- Flask + HTML/CSS (more control, more code)
- Gradio (similar, less flexible)
- Dash (Plotly-based, good for dashboards)

**Key Features Used:**
- `st.chat_message()` - Chat UI
- `st.session_state` - State management
- `st.sidebar` - Side panel
- `st.spinner()` - Loading indicators

---

### 2. Pandas
**Version**: 2.1.4  
**Purpose**: Data manipulation and analysis  
**Files Using**: Future modules (CSV analyzer, Excel analyzer)

**Import Statement:**
```python
import pandas as pd
```

**Why Chosen:**
- Industry standard for data manipulation
- Excellent CSV/Excel support
- Rich data analysis capabilities
- Integrates well with other libraries

**Alternatives:**
- Polars (faster, modern)
- NumPy (lower-level, faster but less features)

**Planned Usage:**
```python
# Future CSV Analyzer
df = pd.read_csv("data.csv")
summary = df.describe()
```

---

### 3. NumPy
**Version**: 1.26.2  
**Purpose**: Numerical computations  
**Files Using**: Future analytics modules

**Import Statement:**
```python
import numpy as np
```

**Why Chosen:**
- Foundation for scientific computing
- Fast array operations
- Required by Pandas
- Statistical functions

**Alternatives:**
- Built-in Python math (slower)

---

## 🛠️ Development Dependencies

### 4. pytest
**Version**: 7.4.3  
**Purpose**: Testing framework  
**Files Using**: All `tests/` files

**Import Statement:**
```python
import pytest
```

**Why Chosen:**
- Simple and powerful
- Great plugin ecosystem
- Clear assertion syntax
- Industry standard

**Alternatives:**
- unittest (built-in but more verbose)
- nose2 (deprecated)

**Usage:**
```bash
pytest tests/
pytest tests/test_router.py -v
pytest --cov=. tests/
```

---

### 5. Black
**Version**: 23.12.1  
**Purpose**: Code formatter  
**Files Using**: All Python files

**Why Chosen:**
- Opinionated formatting (no configuration needed)
- PEP 8 compliant
- Widely adopted standard
- Saves time on style debates

**Alternatives:**
- autopep8 (less opinionated)
- yapf (more configurable)

**Usage:**
```bash
black .
black --check .
```

---

### 6. flake8
**Version**: 6.1.0  
**Purpose**: Linting and style checking  
**Files Using**: All Python files

**Why Chosen:**
- Catches common errors
- Enforces PEP 8
- Finds unused imports
- Identifies complexity issues

**Alternatives:**
- pylint (more features, slower)
- pycodestyle (simpler)

**Usage:**
```bash
flake8 .
flake8 --max-line-length=100 .
```

---

### 7. mypy
**Version**: 1.7.1  
**Purpose**: Static type checking  
**Files Using**: All Python files

**Why Chosen:**
- Catches type errors before runtime
- Improves code documentation
- Better IDE support
- Gradual typing (optional)

**Alternatives:**
- pyright (Microsoft, faster)
- pyre (Facebook)

**Usage:**
```bash
mypy .
mypy --strict backend/
```

---

## 🔧 Configuration & Utilities

### 8. python-dotenv
**Version**: 1.0.0  
**Purpose**: Load environment variables from `.env` file  
**Files Using**: `config/settings.py`

**Import Statement:**
```python
from dotenv import load_dotenv
```

**Why Chosen:**
- Standard for environment variable management
- Keeps secrets out of code
- Easy configuration per environment

**Alternatives:**
- os.environ (built-in but less convenient)
- python-decouple (similar)

**Usage:**
```python
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

---

### 9. PyYAML
**Version**: 6.0.1  
**Purpose**: YAML configuration file parsing  
**Files Using**: Future config management

**Import Statement:**
```python
import yaml
```

**Why Chosen:**
- Human-readable config format
- Better than JSON for configuration
- Support for comments

**Alternatives:**
- configparser (INI files)
- JSON (built-in but no comments)

---

## 📊 File Processing (Future)

### 10. openpyxl
**Version**: 3.1.2  
**Purpose**: Excel file reading and writing  
**Files Using**: Future Excel analyzer

**Import Statement:**
```python
from openpyxl import load_workbook
```

**Why Chosen:**
- Read/write .xlsx files
- Preserve formatting
- Active development

**Alternatives:**
- xlrd/xlwt (older format)
- pandas ExcelWriter (simpler)

---

### 11. python-dateutil
**Version**: 2.8.2  
**Purpose**: Date and time utilities  
**Files Using**: Database, logging modules

**Import Statement:**
```python
from dateutil import parser
```

**Why Chosen:**
- Parse various date formats
- Timezone handling
- Date arithmetic

**Alternatives:**
- Built-in datetime (less flexible)

---

## 🔮 Future AI Integration

### OpenAI (Commented Out)
**Version**: 1.3.7  
**Purpose**: GPT model integration  

**Usage (Future):**
```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
```

---

### Google Generative AI (Commented Out)
**Version**: 0.3.1  
**Purpose**: Gemini model integration  

**Usage (Future):**
```python
import google.generativeai as genai

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Hello")
```

---

## 📈 Data Visualization (Future)

### Matplotlib (Commented Out)
**Version**: 3.8.2  
**Purpose**: Data visualization  

### Seaborn (Commented Out)
**Version**: 0.13.0  
**Purpose**: Statistical visualization  

### Plotly (Commented Out)
**Version**: 5.18.0  
**Purpose**: Interactive visualizations  

---

## 🔐 Authentication (Future)

### bcrypt (Commented Out)
**Version**: 4.1.2  
**Purpose**: Password hashing  

### PyJWT (Commented Out)
**Version**: 2.8.0  
**Purpose**: JWT token generation  

---

## 📋 Dependency Table Summary

| Library | Category | Priority | Status |
|---------|----------|----------|--------|
| streamlit | Frontend | High | ✅ Active |
| pandas | Data | Medium | ✅ Active |
| numpy | Math | Medium | ✅ Active |
| python-dotenv | Config | High | ✅ Active |
| pytest | Testing | Medium | ✅ Active |
| black | Dev | Low | ✅ Active |
| flake8 | Dev | Low | ✅ Active |
| mypy | Dev | Low | ✅ Active |
| openpyxl | File | Low | 🔮 Future |
| openai | AI | Low | 🔮 Future |

---

## 🚀 Installation

### Minimum (Production)
```bash
pip install streamlit pandas numpy python-dotenv
```

### Complete (Development)
```bash
pip install -r requirements.txt
```

### Update All
```bash
pip install --upgrade -r requirements.txt
```

---

## 🔍 Checking Installed Versions

```bash
pip list
pip show streamlit
pip freeze > current_versions.txt
```

---

## 🐛 Troubleshooting

### Issue: Dependency Conflicts

```bash
# Create fresh virtual environment
python -m venv new_venv
new_venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Missing Dependencies

```bash
# Install individually
pip install streamlit
pip install pandas
# etc...
```

### Issue: Version Incompatibilities

```bash
# Pin specific versions
pip install streamlit==1.29.0
```

---

## 📚 Further Reading

- **Streamlit**: https://docs.streamlit.io
- **Pandas**: https://pandas.pydata.org/docs
- **Pytest**: https://docs.pytest.org
- **Black**: https://black.readthedocs.io

---

**Last Updated**: 2024-01-01  
**Maintained By**: Your Name
