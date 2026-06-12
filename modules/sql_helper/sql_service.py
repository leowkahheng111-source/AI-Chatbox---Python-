"""
============================================================================
SQL HELPER SERVICE
============================================================================
Purpose: Provide SQL query assistance and syntax help
Usage: Helps users learn and write SQL queries
Expansion: Add query validation, optimization suggestions, schema design
============================================================================
"""

# Standard Library Imports
import logging
from typing import Dict, Any, Optional

# Internal Project Imports
from backend.exception_handler import handle_errors, ModuleException


# Configure logger
logger = logging.getLogger(__name__)


class SQLService:
    """
    SQL query helper and syntax assistant.
    
    Why this exists:
        - Helps users learn SQL syntax
        - Provides query examples
        - Explains SQL concepts
        - Assists with common SQL tasks
    
    Current Capabilities:
        - SQL syntax help (SELECT, JOIN, WHERE, etc.)
        - Common query patterns
        - SQL concept explanations
        - Best practices
    
    Future Capabilities:
        - Query validation and optimization
        - Schema design suggestions
        - Query execution on sample databases
        - Performance analysis
        - SQL dialect conversion (MySQL ↔ PostgreSQL ↔ SQL Server)
    """
    
    def __init__(self):
        """Initialize SQL helper service."""
        self.logger = logging.getLogger(__name__)
        
        # SQL topic mappings
        self.topics = {
            'select': self._help_select,
            'insert': self._help_insert,
            'update': self._help_update,
            'delete': self._help_delete,
            'join': self._help_join,
            'where': self._help_where,
            'group by': self._help_group_by,
            'order by': self._help_order_by,
            'create table': self._help_create_table,
            'index': self._help_index,
            'primary key': self._help_primary_key,
            'foreign key': self._help_foreign_key,
        }
        
        self.logger.info("SQLService initialized")
    
    @handle_errors("sql_service_process")
    def process(
        self,
        user_input: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Process SQL help request.
        
        Args:
            user_input: User's SQL question
            session_id: Optional session ID
            
        Returns:
            SQL help response
        
        Examples:
            Input: "How do I select all from a table?"
            Output: [SELECT explanation with examples]
            
            Input: "Explain INNER JOIN"
            Output: [JOIN explanation with examples]
        """
        if not user_input:
            return "Please ask an SQL question."
        
        normalized_input = user_input.lower()
        
        self.logger.debug(f"Processing SQL query: {normalized_input[:50]}...")
        
        # Find matching topic
        for topic, handler in self.topics.items():
            if topic in normalized_input:
                return handler()
        
        # Default general SQL help
        return self._general_help()
    
    def _help_select(self) -> str:
        """Provide help for SELECT statements."""
        return """**📊 SQL SELECT Statement**

The SELECT statement retrieves data from a database table.

**Basic Syntax:**
```sql
SELECT column1, column2
FROM table_name;
```

**Select All Columns:**
```sql
SELECT * FROM employees;
```

**Select Specific Columns:**
```sql
SELECT first_name, last_name, salary
FROM employees;
```

**With WHERE Clause:**
```sql
SELECT * FROM employees
WHERE department = 'Sales';
```

**Common Variations:**
- `SELECT DISTINCT` - Remove duplicates
- `SELECT COUNT(*)` - Count rows
- `SELECT TOP 10` or `LIMIT 10` - Limit results

**Example:**
```sql
SELECT DISTINCT department
FROM employees
WHERE salary > 50000
ORDER BY department;
```"""
    
    def _help_insert(self) -> str:
        """Provide help for INSERT statements."""
        return """**➕ SQL INSERT Statement**

The INSERT statement adds new rows to a table.

**Basic Syntax:**
```sql
INSERT INTO table_name (column1, column2, column3)
VALUES (value1, value2, value3);
```

**Example:**
```sql
INSERT INTO employees (first_name, last_name, salary, department)
VALUES ('John', 'Doe', 60000, 'Sales');
```

**Insert Multiple Rows:**
```sql
INSERT INTO employees (first_name, last_name)
VALUES 
    ('Alice', 'Smith'),
    ('Bob', 'Johnson'),
    ('Carol', 'Williams');
```

**Insert from SELECT:**
```sql
INSERT INTO archived_employees
SELECT * FROM employees
WHERE hire_date < '2020-01-01';
```

**Best Practices:**
- Always specify column names
- Ensure data types match
- Check for NOT NULL constraints"""
    
    def _help_update(self) -> str:
        """Provide help for UPDATE statements."""
        return """**✏️ SQL UPDATE Statement**

The UPDATE statement modifies existing records.

**Basic Syntax:**
```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

**Example:**
```sql
UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Sales';
```

**Update Multiple Columns:**
```sql
UPDATE employees
SET salary = 70000,
    department = 'Marketing',
    last_modified = CURRENT_TIMESTAMP
WHERE employee_id = 101;
```

**⚠️ IMPORTANT:**
Always include a WHERE clause! Without it, ALL rows will be updated:
```sql
-- DANGER: Updates all rows!
UPDATE employees SET salary = 50000;

-- SAFE: Updates only matching rows
UPDATE employees SET salary = 50000
WHERE employee_id = 101;
```"""
    
    def _help_delete(self) -> str:
        """Provide help for DELETE statements."""
        return """**🗑️ SQL DELETE Statement**

The DELETE statement removes rows from a table.

**Basic Syntax:**
```sql
DELETE FROM table_name
WHERE condition;
```

**Example:**
```sql
DELETE FROM employees
WHERE employee_id = 101;
```

**Delete Multiple Rows:**
```sql
DELETE FROM employees
WHERE department = 'Temp'
AND hire_date < '2020-01-01';
```

**⚠️ CRITICAL WARNING:**
Always include a WHERE clause! Without it, ALL rows will be deleted:
```sql
-- DANGER: Deletes all data!
DELETE FROM employees;

-- SAFE: Deletes only matching rows
DELETE FROM employees
WHERE status = 'terminated';
```

**Alternative - TRUNCATE:**
To delete all rows (faster):
```sql
TRUNCATE TABLE employees;
```"""
    
    def _help_join(self) -> str:
        """Provide help for JOIN operations."""
        return """**🔗 SQL JOIN Operations**

JOINs combine rows from multiple tables based on related columns.

**INNER JOIN** (most common):
Returns only matching rows from both tables
```sql
SELECT employees.name, departments.dept_name
FROM employees
INNER JOIN departments ON employees.dept_id = departments.id;
```

**LEFT JOIN:**
Returns all rows from left table, matching rows from right
```sql
SELECT employees.name, departments.dept_name
FROM employees
LEFT JOIN departments ON employees.dept_id = departments.id;
```

**RIGHT JOIN:**
Returns all rows from right table, matching rows from left
```sql
SELECT employees.name, departments.dept_name
FROM employees
RIGHT JOIN departments ON employees.dept_id = departments.id;
```

**FULL OUTER JOIN:**
Returns all rows when there's a match in either table
```sql
SELECT employees.name, departments.dept_name
FROM employees
FULL OUTER JOIN departments ON employees.dept_id = departments.id;
```

**Multiple Joins:**
```sql
SELECT e.name, d.dept_name, p.project_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id
INNER JOIN projects p ON e.project_id = p.id;
```"""
    
    def _help_where(self) -> str:
        """Provide help for WHERE clause."""
        return """**🔍 SQL WHERE Clause**

The WHERE clause filters rows based on conditions.

**Basic Syntax:**
```sql
SELECT * FROM employees
WHERE condition;
```

**Comparison Operators:**
```sql
WHERE salary > 50000          -- Greater than
WHERE age >= 25               -- Greater than or equal
WHERE department = 'Sales'    -- Equal to
WHERE status != 'Inactive'    -- Not equal
```

**Logical Operators:**
```sql
-- AND: Both conditions must be true
WHERE salary > 50000 AND department = 'Sales'

-- OR: At least one condition must be true
WHERE department = 'Sales' OR department = 'Marketing'

-- NOT: Negates a condition
WHERE NOT department = 'Temp'
```

**Other Useful Operators:**
```sql
-- BETWEEN: Range of values
WHERE salary BETWEEN 40000 AND 60000

-- IN: Match any value in list
WHERE department IN ('Sales', 'Marketing', 'IT')

-- LIKE: Pattern matching
WHERE name LIKE 'John%'    -- Starts with 'John'
WHERE name LIKE '%son'     -- Ends with 'son'
WHERE name LIKE '%and%'    -- Contains 'and'

-- IS NULL: Check for NULL values
WHERE phone_number IS NULL
```"""
    
    def _help_group_by(self) -> str:
        """Provide help for GROUP BY."""
        return """**📊 SQL GROUP BY Clause**

GROUP BY groups rows with same values for aggregation.

**Basic Syntax:**
```sql
SELECT column, aggregate_function(column)
FROM table
GROUP BY column;
```

**Count employees per department:**
```sql
SELECT department, COUNT(*) as employee_count
FROM employees
GROUP BY department;
```

**Average salary per department:**
```sql
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department;
```

**Multiple Columns:**
```sql
SELECT department, job_title, COUNT(*) as count
FROM employees
GROUP BY department, job_title;
```

**With HAVING (filter grouped results):**
```sql
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 60000;
```

**Aggregate Functions:**
- `COUNT()` - Count rows
- `SUM()` - Sum values
- `AVG()` - Average value
- `MAX()` - Maximum value
- `MIN()` - Minimum value"""
    
    def _help_order_by(self) -> str:
        """Provide help for ORDER BY."""
        return """**🔢 SQL ORDER BY Clause**

ORDER BY sorts the result set.

**Basic Syntax:**
```sql
SELECT * FROM employees
ORDER BY column_name [ASC|DESC];
```

**Ascending (default):**
```sql
SELECT * FROM employees
ORDER BY salary ASC;
-- or simply
ORDER BY salary;
```

**Descending:**
```sql
SELECT * FROM employees
ORDER BY salary DESC;
```

**Multiple Columns:**
```sql
SELECT * FROM employees
ORDER BY department ASC, salary DESC;
```

**By Column Position:**
```sql
SELECT name, salary, department
FROM employees
ORDER BY 2 DESC;  -- Sort by 2nd column (salary)
```"""
    
    def _help_create_table(self) -> str:
        """Provide help for CREATE TABLE."""
        return """**🏗️ SQL CREATE TABLE Statement**

CREATE TABLE creates a new table in the database.

**Basic Syntax:**
```sql
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints,
    ...
);
```

**Example:**
```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE,
    salary DECIMAL(10, 2),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

**Common Data Types:**
- `INT` - Integer numbers
- `VARCHAR(n)` - Variable-length string
- `TEXT` - Long text
- `DATE` - Date (YYYY-MM-DD)
- `DATETIME` - Date and time
- `DECIMAL(p,s)` - Exact decimal numbers
- `BOOLEAN` - True/False

**Common Constraints:**
- `PRIMARY KEY` - Unique identifier
- `NOT NULL` - Cannot be NULL
- `UNIQUE` - All values must be unique
- `DEFAULT` - Default value
- `CHECK` - Value must satisfy condition
- `FOREIGN KEY` - Links to another table"""
    
    def _help_index(self) -> str:
        """Provide help for indexes."""
        return """**⚡ SQL Indexes**

Indexes speed up data retrieval (like a book index).

**Create Index:**
```sql
CREATE INDEX idx_lastname
ON employees(last_name);
```

**Create Unique Index:**
```sql
CREATE UNIQUE INDEX idx_email
ON employees(email);
```

**Composite Index (multiple columns):**
```sql
CREATE INDEX idx_dept_salary
ON employees(department_id, salary);
```

**Drop Index:**
```sql
DROP INDEX idx_lastname;
```

**When to Use:**
✅ Columns used in WHERE clauses
✅ Columns used in JOIN conditions
✅ Columns used in ORDER BY
✅ Large tables with frequent queries

**When to Avoid:**
❌ Small tables
❌ Columns with many NULL values
❌ Tables with frequent INSERT/UPDATE/DELETE
❌ Columns rarely used in queries"""
    
    def _help_primary_key(self) -> str:
        """Provide help for primary keys."""
        return """**🔑 SQL Primary Key**

A PRIMARY KEY uniquely identifies each record in a table.

**Define in CREATE TABLE:**
```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

**Or:**
```sql
CREATE TABLE employees (
    employee_id INT,
    name VARCHAR(100),
    PRIMARY KEY (employee_id)
);
```

**Composite Primary Key (multiple columns):**
```sql
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

**Add to Existing Table:**
```sql
ALTER TABLE employees
ADD PRIMARY KEY (employee_id);
```

**Rules:**
- Must be UNIQUE
- Cannot be NULL
- Only ONE primary key per table
- Often auto-incrementing"""
    
    def _help_foreign_key(self) -> str:
        """Provide help for foreign keys."""
        return """**🔗 SQL Foreign Key**

A FOREIGN KEY links two tables together.

**Define in CREATE TABLE:**
```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

**Named Foreign Key:**
```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    department_id INT,
    CONSTRAINT fk_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
);
```

**Add to Existing Table:**
```sql
ALTER TABLE employees
ADD FOREIGN KEY (department_id)
REFERENCES departments(id);
```

**With Actions:**
```sql
FOREIGN KEY (department_id)
REFERENCES departments(id)
ON DELETE CASCADE      -- Delete child rows when parent deleted
ON UPDATE CASCADE;     -- Update child rows when parent updated
```

**Benefits:**
- Maintains referential integrity
- Prevents invalid data
- Documents relationships"""
    
    def _general_help(self) -> str:
        """Provide general SQL help."""
        return """**🗃️ SQL Helper**

I can help you with SQL queries and concepts!

**Topics I cover:**
- `SELECT` - Retrieve data
- `INSERT` - Add new data
- `UPDATE` - Modify data
- `DELETE` - Remove data
- `JOIN` - Combine tables
- `WHERE` - Filter results
- `GROUP BY` - Aggregate data
- `ORDER BY` - Sort results
- `CREATE TABLE` - Create tables
- `INDEX` - Speed up queries
- `Primary Keys` - Unique identifiers
- `Foreign Keys` - Table relationships

**Examples:**
"How do I use SELECT?"
"Explain INNER JOIN"
"Show me how to CREATE TABLE"

Ask me anything about SQL!"""


# TODO: Future enhancements
# - Query validation and syntax checking
# - Query optimization suggestions
# - Schema design recommendations
# - SQL dialect conversion (MySQL ↔ PostgreSQL)
# - Sample database for query execution
# - Visual query builder
# - Performance analysis
# - Security best practices (SQL injection prevention)
