"""
============================================================================
SPSS ASSISTANT SERVICE
============================================================================
Purpose: Provide SPSS statistical analysis guidance
Usage: Helps users with SPSS software and statistical methods
Expansion: Add syntax generation, interpretation guides, study design help
============================================================================
"""

# Standard Library Imports
import logging
from typing import Optional

# Internal Project Imports
from backend.exception_handler import handle_errors


# Configure logger
logger = logging.getLogger(__name__)


class SPSSService:
    """
    SPSS statistical analysis assistant.
    
    Why this exists:
        - Helps users learn SPSS software
        - Explains statistical tests and methods
        - Provides guidance on choosing appropriate tests
        - Assists with result interpretation
    
    Current Capabilities:
        - Statistical test explanations
        - Test selection guidance
        - SPSS procedure help
        - Interpretation tips
    
    Future Capabilities:
        - SPSS syntax generation
        - Automated test selection
        - Result interpretation
        - Study design recommendations
    """
    
    def __init__(self):
        """Initialize SPSS assistant service."""
        self.logger = logging.getLogger(__name__)
        
        # SPSS topic mappings
        self.topics = {
            't-test': self._help_ttest,
            't test': self._help_ttest,
            'anova': self._help_anova,
            'regression': self._help_regression,
            'correlation': self._help_correlation,
            'chi-square': self._help_chi_square,
            'chi square': self._help_chi_square,
            'crosstab': self._help_crosstabs,
            'descriptive': self._help_descriptives,
            'frequencies': self._help_frequencies,
            'reliability': self._help_reliability,
            'factor analysis': self._help_factor_analysis,
            'normality': self._help_normality,
        }
        
        self.logger.info("SPSSService initialized")
    
    @handle_errors("spss_service_process")
    def process(
        self,
        user_input: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Process SPSS assistance request.
        
        Args:
            user_input: User's SPSS question
            session_id: Optional session ID
            
        Returns:
            SPSS guidance response
        """
        if not user_input:
            return "Please ask an SPSS question."
        
        normalized_input = user_input.lower()
        
        self.logger.debug(f"Processing SPSS query: {normalized_input[:50]}...")
        
        # Find matching topic
        for topic, handler in self.topics.items():
            if topic in normalized_input:
                return handler()
        
        # Default general help
        return self._general_help()
    
    def _help_ttest(self) -> str:
        """Provide help for t-tests."""
        return """**📊 SPSS T-Test**

T-tests compare means between groups.

**Types of T-Tests:**

**1. Independent Samples T-Test**
Compares means of two independent groups.

**When to use:**
- Two separate groups (e.g., male vs female)
- One continuous dependent variable
- Normal distribution

**SPSS Steps:**
1. Analyze → Compare Means → Independent-Samples T Test
2. Select test variable (dependent)
3. Select grouping variable (independent)
4. Define groups
5. Click OK

**Example Research Question:**
"Is there a difference in test scores between students who studied vs didn't study?"

**2. Paired Samples T-Test**
Compares means of the same group at two time points.

**When to use:**
- Same participants measured twice
- Pre-test / Post-test designs
- Matched pairs

**SPSS Steps:**
1. Analyze → Compare Means → Paired-Samples T Test
2. Select Variable 1 (e.g., Pre-test)
3. Select Variable 2 (e.g., Post-test)
4. Click OK

**Example Research Question:**
"Did the training program improve employee performance?"

**3. One-Sample T-Test**
Compares sample mean to a known value.

**When to use:**
- Testing against a standard or norm

**Interpreting Results:**
- **p-value < 0.05**: Significant difference
- **p-value ≥ 0.05**: No significant difference
- Check **Levene's test** for equal variances
- Report **t-value, df, and p-value**

**Assumptions:**
✓ Continuous dependent variable
✓ Normal distribution
✓ Independence of observations
✓ Equal variances (for independent t-test)"""
    
    def _help_anova(self) -> str:
        """Provide help for ANOVA."""
        return """**📈 SPSS ANOVA (Analysis of Variance)**

ANOVA compares means across three or more groups.

**One-Way ANOVA:**
Tests one independent variable with 3+ levels.

**When to use:**
- 3+ independent groups
- One continuous dependent variable
- Normal distribution

**SPSS Steps:**
1. Analyze → Compare Means → One-Way ANOVA
2. Select dependent variable
3. Select factor (grouping variable)
4. Click Post Hoc (for pairwise comparisons)
5. Select LSD or Tukey
6. Click Options → Descriptive statistics, Homogeneity test
7. Click OK

**Example Research Question:**
"Do students in different majors (Engineering, Business, Arts) differ in GPA?"

**Two-Way ANOVA:**
Tests two independent variables and their interaction.

**SPSS Steps:**
1. Analyze → General Linear Model → Univariate
2. Select dependent variable
3. Select fixed factors (independent variables)
4. Click Plots for interaction effects
5. Click Options → Descriptive statistics, Homogeneity tests
6. Click OK

**Interpreting Results:**

**F-statistic:**
- Ratio of between-group to within-group variance
- Higher F = more difference between groups

**p-value:**
- p < 0.05: At least one group differs significantly
- p ≥ 0.05: No significant difference

**Post-Hoc Tests:**
- Determines which specific groups differ
- Only if main ANOVA is significant
- Common tests: Tukey, LSD, Bonferroni

**Assumptions:**
✓ Continuous dependent variable
✓ Independent observations
✓ Normal distribution in each group
✓ Homogeneity of variances (Levene's test)

**Report Format:**
"A one-way ANOVA revealed a significant effect of major on GPA, F(2, 147) = 5.23, p = .007."

**Repeated Measures ANOVA:**
Same participants measured at multiple time points.

**SPSS Steps:**
1. Analyze → General Linear Model → Repeated Measures
2. Define within-subject factors
3. Add measures
4. Click OK"""
    
    def _help_regression(self) -> str:
        """Provide help for regression analysis."""
        return """**📉 SPSS Regression Analysis**

Regression predicts a continuous outcome from one or more predictors.

**Simple Linear Regression:**
One predictor, one outcome.

**SPSS Steps:**
1. Analyze → Regression → Linear
2. Select dependent variable (outcome)
3. Select independent variable (predictor)
4. Click Statistics → Descriptives, Part and partial correlations
5. Click Plots → ZPRED vs ZRESID (check assumptions)
6. Click OK

**Example:**
Predicting salary from years of experience.

**Multiple Regression:**
Multiple predictors, one outcome.

**SPSS Steps:**
1. Analyze → Regression → Linear
2. Select dependent variable
3. Select multiple independent variables
4. Method: Enter (default) or Stepwise
5. Click Statistics → Check desired options
6. Click OK

**Example:**
Predicting GPA from study hours, attendance, and motivation.

**Interpreting Output:**

**R² (R Square):**
- Proportion of variance explained
- 0.25 = 25% of variance explained
- Higher is better

**Adjusted R²:**
- R² adjusted for number of predictors
- More reliable for multiple predictors

**F-test:**
- Tests overall model significance
- p < 0.05: Model is significant

**Coefficients Table:**
```
B (Unstandardized): Raw effect
Beta (Standardized): Standardized effect (compare predictors)
t: Test statistic
Sig.: p-value (< 0.05 = significant)
```

**Example Interpretation:**
"Study hours significantly predicted GPA (β = 0.45, t = 3.21, p = .002). For each additional hour of study, GPA increased by 0.15 points."

**Assumptions:**
✓ Linear relationship
✓ Independence of residuals
✓ Homoscedasticity (constant variance)
✓ Normality of residuals
✓ No multicollinearity (VIF < 10)

**Check Assumptions:**
1. Scatterplot (linearity)
2. Histogram of residuals (normality)
3. P-P plot (normality)
4. Scatterplot ZPRED vs ZRESID (homoscedasticity)
5. Collinearity diagnostics (VIF)"""
    
    def _help_correlation(self) -> str:
        """Provide help for correlation analysis."""
        return """**🔗 SPSS Correlation Analysis**

Correlation measures the relationship between two continuous variables.

**Types:**

**Pearson Correlation:**
Linear relationship between two continuous variables.

**SPSS Steps:**
1. Analyze → Correlate → Bivariate
2. Select variables (2 or more)
3. Ensure Pearson is checked
4. Check "Flag significant correlations"
5. Click OK

**When to use:**
✓ Both variables continuous
✓ Linear relationship
✓ Normal distribution
✓ No outliers

**Spearman's Rho:**
Monotonic relationship (non-linear OK).

**When to use:**
✓ Ordinal data
✓ Non-normal distribution
✓ Non-linear but monotonic relationship

**SPSS Steps:**
Same as Pearson, but check "Spearman"

**Interpreting Results:**

**Correlation Coefficient (r):**
```
 1.0 = Perfect positive correlation
 0.7 to 0.9 = Strong positive
 0.4 to 0.6 = Moderate positive
 0.1 to 0.3 = Weak positive
 0.0 = No correlation
-0.1 to -0.3 = Weak negative
-0.4 to -0.6 = Moderate negative
-0.7 to -0.9 = Strong negative
-1.0 = Perfect negative correlation
```

**Significance:**
- p < 0.05: Significant correlation
- p ≥ 0.05: Not significant

**Example:**
"There was a strong positive correlation between study hours and exam scores (r = 0.78, p < .001)."

**Important Notes:**
⚠️ Correlation ≠ Causation
⚠️ Can be affected by outliers
⚠️ Assumes linear relationship (for Pearson)

**Partial Correlation:**
Correlation while controlling for other variables.

**SPSS Steps:**
1. Analyze → Correlate → Partial
2. Select variables
3. Add controlling variables
4. Click OK"""
    
    def _help_chi_square(self) -> str:
        """Provide help for Chi-Square test."""
        return """**✖️ SPSS Chi-Square Test**

Chi-Square tests associations between categorical variables.

**When to use:**
✓ Two categorical (nominal or ordinal) variables
✓ Independent observations
✓ Expected frequency ≥ 5 in 80% of cells

**SPSS Steps:**
1. Analyze → Descriptive Statistics → Crosstabs
2. Select Row variable
3. Select Column variable
4. Click Statistics → Check "Chi-square"
5. Click Cells → Check "Observed", "Expected", "Row %"
6. Click OK

**Example Research Question:**
"Is there an association between gender and voting preference?"

**Interpreting Results:**

**Pearson Chi-Square:**
- Main test statistic
- p < 0.05: Significant association
- p ≥ 0.05: No significant association

**Cramer's V:**
- Effect size for association strength
```
0.1 = Small effect
0.3 = Medium effect
0.5 = Large effect
```

**Expected Counts:**
- Check that 80% of cells have expected count ≥ 5
- If violated, consider Fisher's Exact Test

**Example Interpretation:**
"There was a significant association between gender and voting preference, χ²(2) = 12.45, p = .002, Cramer's V = .28."

**Types:**

**Chi-Square Test of Independence:**
Tests association between two categorical variables.

**Chi-Square Goodness of Fit:**
Tests if observed frequencies match expected frequencies.

**SPSS Steps (Goodness of Fit):**
1. Analyze → Nonparametric Tests → Legacy Dialogs → Chi-square
2. Select test variable
3. Define expected values
4. Click OK

**Assumptions:**
✓ Categorical variables
✓ Independent observations
✓ Adequate sample size
✓ Expected frequency ≥ 5"""
    
    def _help_crosstabs(self) -> str:
        """Provide help for crosstabulations."""
        return """**📋 SPSS Crosstabs (Crosstabulation)**

Crosstabs display frequency distributions for categorical variables.

**SPSS Steps:**
1. Analyze → Descriptive Statistics → Crosstabs
2. Select Row variable
3. Select Column variable
4. Click Statistics → Select tests (Chi-square, Phi/Cramer's V)
5. Click Cells → Select percentages (Row, Column, Total)
6. Click OK

**Common Statistics to Request:**

**Chi-square:**
Tests association between variables

**Phi and Cramer's V:**
Measure strength of association

**Lambda:**
Proportional reduction in error

**Cell Display Options:**
- **Observed**: Actual counts
- **Expected**: Expected counts (for chi-square)
- **Row %**: Percentage within row
- **Column %**: Percentage within column
- **Total %**: Percentage of total

**Example Output Interpretation:**

```
            | Male  | Female | Total
------------|-------|--------|-------
Approve     | 45    | 65     | 110
            | 40.9% | 59.1%  | 55%
------------|-------|--------|-------
Disapprove  | 35    | 25     | 60
            | 58.3% | 41.7%  | 30%
------------|-------|--------|-------
Neutral     | 10    | 20     | 30
            | 33.3% | 66.7%  | 15%
```

**Reading the Table:**
"65 females approved (59.1% of those who approved, or 32.5% of all respondents)."

**When to Use:**
✓ Exploring relationships between categorical variables
✓ Creating frequency tables
✓ Visualizing proportions
✓ Preliminary data exploration

**Report Format:**
"A crosstabulation revealed that 59.1% of those who approved were female, compared to 41.7% of those who disapproved."
"""
    
    def _help_descriptives(self) -> str:
        """Provide help for descriptive statistics."""
        return """**📊 SPSS Descriptive Statistics**

Descriptive statistics summarize and describe your data.

**SPSS Steps (Descriptives):**
1. Analyze → Descriptive Statistics → Descriptives
2. Select variables
3. Click Options → Select desired statistics
4. Click OK

**SPSS Steps (Explore):**
1. Analyze → Descriptive Statistics → Explore
2. Select dependent variables
3. Optional: Select factor (grouping variable)
4. Click Statistics → Descriptives, Outliers
5. Click Plots → Histogram, Normality plots
6. Click OK

**Common Statistics:**

**Central Tendency:**
- **Mean**: Average value
- **Median**: Middle value (50th percentile)
- **Mode**: Most frequent value

**Variability:**
- **Std. Deviation**: Average distance from mean
- **Variance**: Squared standard deviation
- **Range**: Maximum - Minimum
- **IQR**: Interquartile range (25th to 75th percentile)

**Distribution:**
- **Skewness**: Symmetry of distribution
  - 0 = Symmetric
  - Positive = Right-skewed (tail to right)
  - Negative = Left-skewed (tail to left)
  
- **Kurtosis**: Peakedness of distribution
  - 0 = Normal distribution
  - Positive = More peaked
  - Negative = Flatter

**When to Report:**
✓ Sample characteristics
✓ Variable distributions
✓ Data exploration
✓ Preliminary analysis

**Example Report:**
"Participants' age ranged from 18 to 65 years (M = 34.2, SD = 12.5). The distribution was approximately normal (skewness = 0.12, kurtosis = -0.23)."

**Check Data Quality:**
- Minimum/Maximum (detect data entry errors)
- Missing values
- Outliers (values > 3 SD from mean)
- Distribution shape"""
    
    def _help_frequencies(self) -> str:
        """Provide help for frequency tables."""
        return """**📈 SPSS Frequencies**

Frequency tables show distribution of categorical or discrete variables.

**SPSS Steps:**
1. Analyze → Descriptive Statistics → Frequencies
2. Select variables
3. Click Statistics → Select desired statistics
4. Click Charts → Select chart type
5. Click OK

**What You Get:**

**Frequency Table:**
```
Value     | Frequency | Percent | Valid % | Cumulative %
----------|-----------|---------|---------|-------------
Male      | 45        | 45.0    | 45.0    | 45.0
Female    | 55        | 55.0    | 55.0    | 100.0
Total     | 100       | 100.0   | 100.0   |
```

**Columns:**
- **Frequency**: Count of cases
- **Percent**: Percentage including missing
- **Valid Percent**: Percentage excluding missing
- **Cumulative Percent**: Running total

**Statistics to Request:**
- Mean, Median, Mode
- Std. Deviation
- Minimum, Maximum
- Percentiles (quartiles)

**Charts:**
- Bar chart (categorical)
- Histogram (continuous)
- Pie chart (categorical, small # categories)

**When to Use:**
✓ Categorical variables
✓ Ordinal variables
✓ Checking data distribution
✓ Identifying missing values
✓ Detecting outliers

**Example Interpretation:**
"The sample consisted of 55% females and 45% males. The most common education level was Bachelor's degree (40%), followed by Master's (30%)."

**Tips:**
- Use for categorical data
- Use Descriptives for continuous data
- Check for data entry errors
- Identify missing patterns"""
    
    def _help_reliability(self) -> str:
        """Provide help for reliability analysis."""
        return """**🎯 SPSS Reliability Analysis (Cronbach's Alpha)**

Reliability analysis assesses internal consistency of a scale.

**When to Use:**
✓ Multiple items measuring same construct
✓ Creating a scale/index
✓ Survey development

**SPSS Steps:**
1. Analyze → Scale → Reliability Analysis
2. Select all scale items
3. Model: Alpha (Cronbach's Alpha)
4. Click Statistics → Check:
   - Item, Scale, Scale if item deleted
   - Correlations
5. Click OK

**Interpreting Cronbach's Alpha:**
```
α ≥ 0.90 = Excellent
α ≥ 0.80 = Good
α ≥ 0.70 = Acceptable
α ≥ 0.60 = Questionable
α < 0.60 = Poor
```

**Example:**
"The 5-item job satisfaction scale demonstrated good internal consistency (α = .82)."

**Item Analysis:**

**Corrected Item-Total Correlation:**
- Correlation between item and total score
- Should be > 0.30
- Low values = consider removing item

**Cronbach's Alpha if Item Deleted:**
- Alpha value if item is removed
- If higher than overall alpha = consider removing item
- Shows which items hurt reliability

**Example Output:**
```
Item                    | CITC  | Alpha if Deleted
------------------------|-------|------------------
Item 1: I like my job  | .65   | .78
Item 2: Job is fun     | .58   | .79
Item 3: Enjoy work     | .42   | .83  ← Consider removing
Item 4: Satisfied      | .71   | .76
```

**Improving Reliability:**
1. Remove items with low CITC (< .30)
2. Remove items that increase alpha when deleted
3. Ensure items measure same construct
4. Check for reverse-coded items
5. Increase number of items

**Report Format:**
"Internal consistency was assessed using Cronbach's alpha. The scale demonstrated good reliability (α = .82, 95% CI [.76, .87])."

**Minimum Requirements:**
- At least 3 items
- Sample size > 30
- Items on similar scale"""
    
    def _help_factor_analysis(self) -> str:
        """Provide help for factor analysis."""
        return """**🔍 SPSS Factor Analysis**

Factor Analysis identifies underlying factors from multiple variables.

**Types:**

**Exploratory Factor Analysis (EFA):**
Discovers underlying structure (no prior hypothesis).

**SPSS Steps:**
1. Analyze → Dimension Reduction → Factor
2. Select variables (items)
3. Click Descriptives → KMO and Bartlett's test
4. Click Extraction → Method: Principal Components
   - Check: Scree plot
   - Extract: Based on Eigenvalue > 1 (or specify #)
5. Click Rotation → Varimax (or Oblimin if factors correlated)
6. Click Options → Suppress small coefficients < .40
7. Click OK

**Confirmatory Factor Analysis (CFA):**
Tests a specific factor structure (use AMOS or structural equation modeling).

**Assessing Suitability:**

**KMO (Kaiser-Meyer-Olkin):**
```
≥ 0.90 = Marvelous
≥ 0.80 = Meritorious
≥ 0.70 = Middling
≥ 0.60 = Mediocre
< 0.60 = Unacceptable
```

**Bartlett's Test of Sphericity:**
- p < .05 = Good (items are correlated)
- p ≥ .05 = Bad (items not correlated enough)

**Determining Number of Factors:**

**Eigenvalues:**
- Factors with eigenvalue > 1.0
- Each factor should explain variance

**Scree Plot:**
- Look for "elbow" (where curve levels off)
- Keep factors before the elbow

**Interpreting Factor Loadings:**
```
≥ 0.70 = Excellent
≥ 0.60 = Very good
≥ 0.50 = Good
≥ 0.40 = Fair (minimum to keep)
< 0.40 = Poor (consider removing)
```

**Factor Rotation:**

**Varimax (Orthogonal):**
- Assumes factors are uncorrelated
- Easier to interpret
- More common

**Oblimin (Oblique):**
- Allows factors to correlate
- More realistic for psychology/social science

**Example Interpretation:**
"A principal components analysis with varimax rotation revealed 3 factors with eigenvalues > 1, explaining 67% of the variance. KMO = .85, indicating sampling adequacy."

**Report:**
1. KMO and Bartlett's test
2. Number of factors and extraction method
3. Rotation method
4. Total variance explained
5. Factor loadings table
6. Factor names/interpretations"""
    
    def _help_normality(self) -> str:
        """Provide help for normality tests."""
        return """**📊 SPSS Normality Tests**

Test whether data follows a normal distribution.

**Why Test Normality:**
- Many tests assume normal distribution
- Determines which test to use (parametric vs non-parametric)

**SPSS Steps:**
1. Analyze → Descriptive Statistics → Explore
2. Select dependent variable
3. Click Plots → Check:
   - Normality plots with tests
   - Histogram
4. Click OK

**Tests of Normality:**

**Kolmogorov-Smirnov Test:**
- For larger samples (n > 50)
- p > .05 = Normal distribution
- p ≤ .05 = Not normal

**Shapiro-Wilk Test:**
- For smaller samples (n < 50)
- More powerful than K-S
- p > .05 = Normal distribution
- p ≤ .05 = Not normal

**Visual Inspection:**

**Histogram:**
- Should look bell-shaped
- Symmetric around mean

**Q-Q Plot (Normal Q-Q Plot):**
- Points should follow diagonal line
- Deviations = non-normality
- S-shape = skewness
- Curved = kurtosis

**Detrended Q-Q Plot:**
- Points should cluster around zero line
- Pattern = non-normality

**Box Plot:**
- Check for outliers
- Assess symmetry

**Descriptive Statistics:**

**Skewness:**
```
Between -1 and +1 = Approximately normal
Between -2 and +2 = Acceptable
Outside ±2 = Non-normal
```

**Kurtosis:**
```
Between -1 and +1 = Approximately normal
Between -3 and +3 = Acceptable
Outside ±3 = Non-normal
```

**What to Do If Not Normal:**

1. **Transform Data:**
   - Log transformation
   - Square root transformation
   - Inverse transformation

2. **Use Non-Parametric Tests:**
   - Mann-Whitney U (instead of t-test)
   - Kruskal-Wallis (instead of ANOVA)
   - Spearman's rho (instead of Pearson)

3. **Increase Sample Size:**
   - Central Limit Theorem (n > 30)
   - Parametric tests more robust with larger n

4. **Remove Outliers:**
   - Check if legitimate data
   - Consider impact on results

**Example Report:**
"The Shapiro-Wilk test indicated that scores were approximately normally distributed (W = .98, p = .14). Visual inspection of the Q-Q plot confirmed normality."

**Tip:**
With large samples (n > 200), normality tests often show significance even for minor deviations. Rely more on visual inspection."""
    
    def _general_help(self) -> str:
        """Provide general SPSS help."""
        return """**📈 SPSS Statistical Assistant**

I can help you with SPSS and statistical analysis!

**Topics I cover:**

**Tests:**
- `T-Test` - Compare means (2 groups)
- `ANOVA` - Compare means (3+ groups)
- `Regression` - Predict outcomes
- `Correlation` - Measure relationships
- `Chi-Square` - Test associations (categorical)

**Descriptive Statistics:**
- `Descriptives` - Summarize data
- `Frequencies` - Distribution tables
- `Crosstabs` - Contingency tables

**Advanced:**
- `Reliability` - Cronbach's Alpha
- `Factor Analysis` - Identify factors
- `Normality Tests` - Check assumptions

**Examples:**
"How do I run a t-test?"
"Explain ANOVA"
"What is Cronbach's Alpha?"
"How to check normality?"

**Choosing the Right Test:**
- 2 groups, continuous DV → T-Test
- 3+ groups, continuous DV → ANOVA
- 2 categorical variables → Chi-Square
- Predict outcome → Regression
- Measure relationship → Correlation

Ask me anything about SPSS!"""


# TODO: Future enhancements
# - SPSS syntax generation
# - Automated test selection based on data type
# - Result interpretation assistance
# - Sample size calculators
# - Power analysis
# - Effect size calculators
# - Study design recommendations
# - Assumption checking guides
