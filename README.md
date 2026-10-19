# Blackrock – Financial Risk Analysis

## Project Overview
This project analyzes customer financial behavior and transaction data using Python to identify transaction trends, account dormancy, financial risk indicators, and unusual transactions.

The analysis covers **800 transactions, 184 accounts, and 180 customers** from January 2023 to June 2024.

## Objectives
- Clean and preprocess financial transaction data.
- Analyze monthly credit and debit transaction trends.
- Evaluate account-level net inflows and outflows.
- Build customer profiles based on transaction frequency and average balance.
- Identify potential financial risks and anomalous transactions.
- Visualize financial patterns and perform statistical hypothesis testing.

## Tools & Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Jupyter Notebook

## Project Workflow

### 1. Data Cleaning
- Removed special characters from financial fields.
- Converted financial columns into numeric format.
- Standardized transaction dates and categorical fields.
- Checked for missing values and duplicate records.

### 2. Transaction Analysis
- Compared monthly credit and debit transaction volumes.
- Calculated account-level net inflows and outflows.
- Identified transaction gaps of 60 days or more.

### 3. Customer Profiling
- Grouped customers by transaction frequency.
- Classified customers into low, medium, and high activity levels.
- Examined average account balances and transaction volume.

### 4. Financial Risk Identification
- Identified large withdrawals using the 75th percentile threshold.
- Analyzed account balance volatility.
- Detected transaction anomalies using the Interquartile Range (IQR) method.
- Combined multiple risk indicators to flag accounts for further review.

### 5. Visualization & Hypothesis Testing
- Visualized credit-debit trends and transaction distributions.
- Examined the relationship between risk scores and credit ratings.
- Conducted a one-tailed Welch's t-test to compare average balances across transaction-volume groups.

## Key Findings
- **Net transaction outflow:** Approximately ₹1.17 crore, with total debits exceeding total credits.
- **Account dormancy:** 172 out of 184 accounts (approximately 93%) had at least one transaction gap of 60 days or more.
- **Anomaly detection:** 7 transactions were flagged as statistical outliers using the IQR method.
- **Risk indicators:** 20 accounts had a combined risk flag score of 2 or higher.
- **Hypothesis testing:** The test did not find statistically significant evidence that high-volume customers had higher average balances (one-tailed p-value = 0.5466).

## Recommendations
- Consider re-engagement campaigns for dormant accounts.
- Monitor accounts with repeated large withdrawals or multiple risk indicators.
- Manually review flagged transactions for possible data errors or suspicious activity.
- Evaluate customer value using account balances and net inflows alongside transaction frequency.

## Project Presentation
[Watch the project presentation on Loom](https://www.loom.com/share/6e7ec8f7ea974ce89e77f686d7c12a9c)

## Project Report
The detailed PDF report is available in this repository as `Blackrock_Financial_Risk_Analysis.pdf`.

## Disclaimer
This project demonstrates analytical techniques on the dataset used for the analysis. Identified anomalies and risk indicators require further investigation and do not, by themselves, establish fraud or financial misconduct.

## Author
Sagar

**Skills:** Python | Data Analysis | Pandas | NumPy | Data Visualization | Statistical Analysis | Financial Risk Analysis
