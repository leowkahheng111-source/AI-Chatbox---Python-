"""
============================================================================
POWER BI DAX HELPER SERVICE
============================================================================
Purpose: Provide Power BI DAX formula assistance
Usage: Helps users learn and write DAX formulas
Expansion: Add DAX validation, optimization suggestions, pattern library
============================================================================
"""

# Standard Library Imports
import logging
from typing import Optional

# Internal Project Imports
from backend.exception_handler import handle_errors


# Configure logger
logger = logging.getLogger(__name__)


class DAXService:
    """
    Power BI DAX formula helper.
    
    Why this exists:
        - Helps users learn DAX syntax
        - Provides DAX formula examples
        - Explains DAX concepts
        - Assists with Power BI measures and calculations
    
    Current Capabilities:
        - DAX function explanations
        - Common formula patterns
        - Context explanations (row context vs filter context)
        - Best practices
    
    Future Capabilities:
        - DAX formula validation
        - Performance optimization suggestions
        - Data model recommendations
        - Interactive formula builder
    """
    
    def __init__(self):
        """Initialize DAX helper service."""
        self.logger = logging.getLogger(__name__)
        
        # DAX topic mappings
        self.topics = {
            'calculate': self._help_calculate,
            'sum': self._help_sum,
            'sumx': self._help_sumx,
            'filter': self._help_filter,
            'all': self._help_all,
            'related': self._help_related,
            'earlier': self._help_earlier,
            'time intelligence': self._help_time_intelligence,
            'measure': self._help_measure,
            'calculated column': self._help_calculated_column,
            'context': self._help_context,
        }
        
        self.logger.info("DAXService initialized")
    
    @handle_errors("dax_service_process")
    def process(
        self,
        user_input: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Process DAX help request.
        
        Args:
            user_input: User's DAX question
            session_id: Optional session ID
            
        Returns:
            DAX help response
        """
        if not user_input:
            return "Please ask a Power BI DAX question."
        
        normalized_input = user_input.lower()
        
        self.logger.debug(f"Processing DAX query: {normalized_input[:50]}...")
        
        # Find matching topic
        for topic, handler in self.topics.items():
            if topic in normalized_input:
                return handler()
        
        # Default general help
        return self._general_help()
    
    def _help_calculate(self) -> str:
        """Provide help for CALCULATE function."""
        return """**📊 DAX CALCULATE Function**

CALCULATE is the most important DAX function. It evaluates an expression in a modified filter context.

**Syntax:**
```dax
CALCULATE(<expression>, <filter1>, <filter2>, ...)
```

**Example 1: Basic Sales Calculation**
```dax
Sales Amount = SUM(Sales[Amount])

Sales Amount 2023 = 
CALCULATE(
    SUM(Sales[Amount]),
    Year[Year] = 2023
)
```

**Example 2: Multiple Filters**
```dax
Sales Red Products = 
CALCULATE(
    SUM(Sales[Amount]),
    Product[Color] = "Red",
    Product[Category] = "Electronics"
)
```

**Example 3: Clear Filters**
```dax
Total Sales All Regions = 
CALCULATE(
    SUM(Sales[Amount]),
    ALL(Region)
)
```

**Key Concepts:**
- Modifies filter context
- Can add, replace, or remove filters
- Essential for creating complex measures
- Understands relationships in your model

**Common Patterns:**
```dax
-- Year-over-Year Comparison
Sales YOY = 
CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR(Date[Date])
)
```"""
    
    def _help_sum(self) -> str:
        """Provide help for SUM function."""
        return """**➕ DAX SUM Function**

SUM adds all numbers in a column.

**Syntax:**
```dax
SUM(<column>)
```

**Example:**
```dax
Total Sales = SUM(Sales[Amount])

Total Quantity = SUM(Sales[Quantity])
```

**Important:**
- Works only on numeric columns
- Ignores blank cells
- Cannot use calculated expressions (use SUMX for that)

**When to Use:**
✅ Simple column aggregation
✅ In measures
✅ Fast performance

**SUM vs SUMX:**
```dax
-- SUM: Aggregates existing column
Total Sales = SUM(Sales[Amount])

-- SUMX: Calculates row-by-row then sums
Total Revenue = 
SUMX(
    Sales,
    Sales[Quantity] * Sales[Price]
)
```"""
    
    def _help_sumx(self) -> str:
        """Provide help for SUMX function."""
        return """**🔄 DAX SUMX Function**

SUMX is an iterator that evaluates an expression for each row, then sums the results.

**Syntax:**
```dax
SUMX(<table>, <expression>)
```

**Example 1: Calculate Revenue**
```dax
Total Revenue = 
SUMX(
    Sales,
    Sales[Quantity] * Sales[UnitPrice]
)
```

**Example 2: With RELATED**
```dax
Total Cost = 
SUMX(
    Sales,
    Sales[Quantity] * RELATED(Product[Cost])
)
```

**Example 3: With FILTER**
```dax
Large Order Revenue = 
SUMX(
    FILTER(Sales, Sales[Quantity] > 100),
    Sales[Quantity] * Sales[UnitPrice]
)
```

**Key Points:**
- Iterates row-by-row
- Can use complex expressions
- Slower than SUM (but more flexible)
- Essential for calculated aggregations

**Common Use Cases:**
- Row-level calculations
- Applying discounts
- Currency conversions
- Weighted averages"""
    
    def _help_filter(self) -> str:
        """Provide help for FILTER function."""
        return """**🔍 DAX FILTER Function**

FILTER returns a table that represents a subset of another table.

**Syntax:**
```dax
FILTER(<table>, <condition>)
```

**Example 1: Filter Products**
```dax
Red Product Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(Product, Product[Color] = "Red")
)
```

**Example 2: Complex Conditions**
```dax
High Value Sales = 
SUMX(
    FILTER(
        Sales,
        Sales[Amount] > 1000 && Sales[Quantity] > 10
    ),
    Sales[Amount]
)
```

**Example 3: Dynamic Filters**
```dax
Above Average Sales = 
SUMX(
    FILTER(
        Sales,
        Sales[Amount] > AVERAGE(Sales[Amount])
    ),
    Sales[Amount]
)
```

**Performance Tips:**
⚡ Use simple filters in CALCULATE when possible
⚡ Apply filters on smaller tables
⚡ Avoid filtering large fact tables

**Better:**
```dax
-- Simpler and faster
Sales Red = 
CALCULATE(
    SUM(Sales[Amount]),
    Product[Color] = "Red"
)

-- More complex but slower
Sales Red = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(ALL(Product), Product[Color] = "Red")
)
```"""
    
    def _help_all(self) -> str:
        """Provide help for ALL function."""
        return """**🌐 DAX ALL Function**

ALL removes all filters from specified columns or tables.

**Syntax:**
```dax
ALL(<table_or_column>)
```

**Example 1: Calculate % of Total**
```dax
Sales % of Total = 
DIVIDE(
    SUM(Sales[Amount]),
    CALCULATE(SUM(Sales[Amount]), ALL(Sales))
)
```

**Example 2: Ignore Specific Filters**
```dax
Sales All Regions = 
CALCULATE(
    SUM(Sales[Amount]),
    ALL(Region)
)
```

**Example 3: Preserve Some Filters**
```dax
Sales This Year All Regions = 
CALCULATE(
    SUM(Sales[Amount]),
    ALL(Region),
    Date[Year] = 2023
)
```

**Variants:**
```dax
-- ALL: Removes all filters
ALL(Sales)

-- ALLEXCEPT: Removes all filters except specified
ALLEXCEPT(Sales, Sales[Year])

-- ALLSELECTED: Respects visual-level filters
ALLSELECTED(Product)
```

**Common Uses:**
- Grand totals
- Percentages
- Rankings
- Comparing to overall values"""
    
    def _help_related(self) -> str:
        """Provide help for RELATED function."""
        return """**🔗 DAX RELATED Function**

RELATED returns a value from another table using relationships.

**Syntax:**
```dax
RELATED(<column>)
```

**Example 1: Get Product Category**
```dax
Sales Category = 
RELATED(Product[Category])
```

**Example 2: Calculate Extended Price**
```dax
Extended Price = 
Sales[Quantity] * RELATED(Product[UnitPrice])
```

**Example 3: Use in Measure**
```dax
Total Cost = 
SUMX(
    Sales,
    Sales[Quantity] * RELATED(Product[Cost])
)
```

**Requirements:**
- Must have relationship between tables
- Follows many-to-one direction
- Used in calculated columns or row context

**RELATED vs RELATEDTABLE:**
```dax
-- RELATED: Get single value (many-to-one)
Product Category = RELATED(Category[Name])

-- RELATEDTABLE: Get table (one-to-many)
Customer Sales Count = 
COUNTROWS(RELATEDTABLE(Sales))
```

**Typical Scenarios:**
- Pulling lookup values
- Price calculations
- Category aggregations
- Hierarchical data"""
    
    def _help_earlier(self) -> str:
        """Provide help for EARLIER function."""
        return """**⏪ DAX EARLIER Function**

EARLIER accesses row context from an outer loop (used in nested iterations).

**Syntax:**
```dax
EARLIER(<column>, <num>)
```

**Example 1: Running Total**
```dax
Running Total = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALL(Sales),
        Sales[Date] <= EARLIER(Sales[Date])
    )
)
```

**Example 2: Ranking**
```dax
Rank = 
COUNTROWS(
    FILTER(
        ALL(Product),
        Product[Sales] > EARLIER(Product[Sales])
    )
) + 1
```

**Example 3: Find Duplicates**
```dax
Duplicate Count = 
COUNTROWS(
    FILTER(
        ALL(Customer),
        Customer[Email] = EARLIER(Customer[Email])
    )
)
```

**When to Use:**
- Running totals
- Rankings
- Comparing current row to other rows
- Nested iterations

**Modern Alternative:**
Many EARLIER scenarios can now use variables:
```dax
-- Old way with EARLIER
Running Total Old = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(ALL(Sales), Sales[Date] <= EARLIER(Sales[Date]))
)

-- New way with VAR
Running Total New = 
VAR CurrentDate = Sales[Date]
RETURN
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(ALL(Sales), Sales[Date] <= CurrentDate)
    )
```"""
    
    def _help_time_intelligence(self) -> str:
        """Provide help for time intelligence functions."""
        return """**📅 DAX Time Intelligence**

Time intelligence functions perform calculations over time periods.

**Requirements:**
- Must have a Date table
- Mark table as Date table in Power BI
- Continuous date range

**Year-to-Date (YTD):**
```dax
Sales YTD = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESYTD(Date[Date])
)
```

**Previous Year:**
```dax
Sales Last Year = 
CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR(Date[Date])
)
```

**Year-over-Year Growth:**
```dax
YOY Growth = 
VAR CurrentYear = SUM(Sales[Amount])
VAR LastYear = CALCULATE(SUM(Sales[Amount]), SAMEPERIODLASTYEAR(Date[Date]))
RETURN
    DIVIDE(CurrentYear - LastYear, LastYear)
```

**Moving Average:**
```dax
3 Month Moving Average = 
CALCULATE(
    AVERAGE(Sales[Amount]),
    DATESINPERIOD(Date[Date], LASTDATE(Date[Date]), -3, MONTH)
)
```

**Common Functions:**
- `DATESYTD()` - Year to date
- `DATESMTD()` - Month to date
- `DATESQTD()` - Quarter to date
- `SAMEPERIODLASTYEAR()` - Previous year same period
- `DATEADD()` - Shift dates by interval
- `DATESBETWEEN()` - Date range
- `PARALLELPERIOD()` - Parallel period

**Example Dashboard Measures:**
```dax
Sales This Month = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESMTD(Date[Date])
)

Sales vs Last Month % = 
VAR ThisMonth = [Sales This Month]
VAR LastMonth = CALCULATE([Sales This Month], DATEADD(Date[Date], -1, MONTH))
RETURN DIVIDE(ThisMonth - LastMonth, LastMonth)
```"""
    
    def _help_measure(self) -> str:
        """Provide help for measures."""
        return """**📏 DAX Measures**

Measures are dynamic calculations evaluated in filter context.

**Creating a Measure:**
```dax
Total Sales = SUM(Sales[Amount])
```

**Measure vs Calculated Column:**

**Measure:**
- Calculated at query time
- Responds to filters/slicers
- Doesn't use storage
- For aggregations

```dax
Total Sales = SUM(Sales[Amount])
Average Price = AVERAGE(Product[Price])
```

**Calculated Column:**
- Calculated at refresh time
- Fixed value per row
- Uses storage
- For row-level logic

```dax
Full Name = Customer[FirstName] & " " & Customer[LastName]
Profit = Sales[Revenue] - Sales[Cost]
```

**Best Practices:**
✅ Use measures for aggregations
✅ Use clear naming
✅ Add descriptions
✅ Group related measures in folders
✅ Use variables for readability

**Example with Variables:**
```dax
Sales Analysis = 
VAR TotalSales = SUM(Sales[Amount])
VAR TotalCost = SUM(Sales[Cost])
VAR Profit = TotalSales - TotalCost
VAR MarginPercent = DIVIDE(Profit, TotalSales)
RETURN
    MarginPercent
```"""
    
    def _help_calculated_column(self) -> str:
        """Provide help for calculated columns."""
        return """**📋 DAX Calculated Columns**

Calculated columns add new columns to tables with row-level calculations.

**Creating Calculated Column:**
```dax
Full Name = Customer[FirstName] & " " & Customer[LastName]

Profit = Sales[Revenue] - Sales[Cost]

Discount Amount = Sales[Quantity] * Sales[Price] * Sales[Discount%]
```

**With RELATED:**
```dax
Product Category = RELATED(Category[Name])

Extended Price = Sales[Quantity] * RELATED(Product[UnitPrice])
```

**With Conditional Logic:**
```dax
Customer Segment = 
IF(
    Customer[TotalPurchases] > 10000,
    "Premium",
    IF(
        Customer[TotalPurchases] > 5000,
        "Standard",
        "Basic"
    )
)
```

**When to Use:**
✅ Row-level calculations
✅ Filtering/slicing by result
✅ Values that rarely change

**When to Avoid:**
❌ Aggregations (use measures)
❌ Large tables (increases model size)
❌ Frequently changing calculations

**Performance Impact:**
- Calculated at refresh time
- Uses memory (increases model size)
- Can slow down refresh
- Consider impact on large tables"""
    
    def _help_context(self) -> str:
        """Provide help for DAX context."""
        return """**🎯 DAX Context (Row vs Filter)**

Understanding context is crucial for mastering DAX.

**Row Context:**
Exists when DAX evaluates a formula row-by-row.

**Present in:**
- Calculated columns
- Iterator functions (SUMX, FILTER)

**Example:**
```dax
-- Calculated Column (has row context)
Total Price = Sales[Quantity] * Sales[UnitPrice]

-- Measure with iterator (creates row context)
Total Revenue = 
SUMX(
    Sales,
    Sales[Quantity] * Sales[UnitPrice]  -- Row context here
)
```

**Filter Context:**
The set of filters applied to the data model.

**Sources:**
- Slicers
- Report filters
- Row/column fields in visuals
- CALCULATE function

**Example:**
```dax
Total Sales = SUM(Sales[Amount])

-- When you slice by Year=2023:
-- Filter context = Year[Year] = 2023
-- Result = Sum of sales for 2023 only
```

**Context Transition:**
When row context becomes filter context.

```dax
-- Without context transition (wrong!)
Customer Sales Wrong = 
SUM(Sales[Amount])  -- Gives total, not per customer

-- With context transition (correct!)
Customer Sales Correct = 
CALCULATE(SUM(Sales[Amount]))  -- CALCULATE transitions context
```

**Key Takeaways:**
- Row context: One row at a time
- Filter context: Set of filters
- CALCULATE transitions row → filter context
- Understanding context prevents errors"""
    
    def _general_help(self) -> str:
        """Provide general DAX help."""
        return """**📊 Power BI DAX Helper**

I can help you with DAX formulas and Power BI calculations!

**Topics I cover:**
- `CALCULATE` - Modify filter context
- `SUM / SUMX` - Aggregation functions
- `FILTER` - Filter tables
- `ALL` - Remove filters
- `RELATED` - Access related tables
- `EARLIER` - Nested iterations
- `Time Intelligence` - Date calculations
- `Measures` - Dynamic calculations
- `Calculated Columns` - Row-level formulas
- `Context` - Row vs Filter context

**Examples:**
"Explain CALCULATE function"
"How do I create a measure?"
"What is time intelligence?"

Ask me anything about DAX!"""


# TODO: Future enhancements
# - DAX formula validation
# - Performance optimization suggestions
# - Data model recommendations
# - Interactive formula builder
# - Common pattern library
# - DAX formatter
# - Query plan analysis
