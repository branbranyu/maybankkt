1. esg_credit_rating_scatterplot.py

Data Loading and Preparation:
- Maps credit ratings (e.g., "AAA", "AA+") to numerical values using a predefined dictionary.
- Drops rows with missing values in relevant columns (ESG scores and numerical ratings).

Analysis:
- Defines ESG features (Total ESG Risk score, Environment Risk Score, Social Risk Score, Governance Risk Score) for analysis.
- Fits a linear regression model for each ESG feature to predict the numerical credit rating.
- Calculates the R-squared value for each regression, which measures how well the ESG feature explains the variation in credit ratings.

Visualisation:
- Creates scatter plots with regression lines for each ESG feature against the numerical credit rating.
- Displays the R-squared value on each plot.


2. esg_on_credit_banded.py

Data Loading and Preparation:
- Loads ESG and credit rating data from a CSV file.
- Groups credit ratings into bands (e.g., "Band 1", "Band 2") and adds a new column for these bands.
- Drops rows with missing values in relevant columns.
- Encodes the credit rating bands into numerical values for correlation analysis.

Analysis:
- Performs an ANOVA test to analyse the variance of ESG scores across different credit rating bands.
- Calculates Pearson and Spearman correlations between ESG scores and encoded credit rating bands.
Visualisation:
- Creates box plots to compare the distribution of ESG scores across credit rating bands (excluding "Very Low Grade").
- Generates scatter plots to visualise the relationship between ESG scores and credit rating bands.

3. esg_credit_distribution_binning.py

Binning ESG Scores:
- Divides the Total ESG Risk score into bins of size 5 (e.g., 0-5, 5-10, etc.).
- Assigns labels to these bins and creates a new column, ESG_bands, in the DataFrame.

Binning Credit Ratings:
- Divides the Numerical Rating into bins (e.g., 0-2, 2-4, etc.).
- Assigns labels to these bins and creates a new column, Credit_bands, in the DataFrame.

Cross-Tabulation:
- Creates a cross-tabulation (frequency table) of ESG_bands and Credit_bands.
- Generates a heat map to visualise the frequency distribution of ESG bands against credit bands.

4. esg_scores_to_financials.py

Defines Columns
Specifies two groups of columns:

- Financial metrics (e.g., "Current Ratio", "Gross Margin").
ESG scores (e.g., "Environment Risk Score", "Total ESG Risk score").
- Computes Correlation: Calculates the Spearman correlation matrix between the financial metrics and ESG scores.

Visualizes Correlation:
- Creates a heat map to display the correlation between ESG scores and financial metrics.

Identifies Strong Correlations:
- Filters pairs of ESG scores and financial metrics with a correlation (absolute value) above a threshold (0.3).
- Sorts these pairs by the strength of the correlation.

Plots Strong Correlations:
For each strongly correlated pair, it generates:
- A scatterplot to visualise the relationship.
- A binned heat map to show the density of data points.
