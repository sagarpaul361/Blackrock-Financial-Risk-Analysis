import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("blackrock.csv")
#TASK 1: DATA CLEANING AND FORMATTING
print("\nOriginal Data:")
print(df.head())

print("\nData Types Before Cleaning:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

# 1. Remove special characters from financial fields
financial_columns = [
    "TransactionAmount",
    "AccountBalance",
    "RiskScore",
    "CreditRating"]

for col in financial_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(r"[^\d.-]", "", regex=True)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 2. Convert TransactionDate into datetime
df["TransactionDate"] = pd.to_datetime(
    df["TransactionDate"],
    errors="coerce"
)

print("\nInvalid Transaction Dates:")
print(df["TransactionDate"].isna().sum())
# 3. Standardize Account Type
if "AccountType" in df.columns:
    df["AccountType"] = (
        df["AccountType"]
        .astype(str)
        .str.strip()
        .str.title()
    )
print("\nColumn Names:")
print(df.columns.tolist())
# 4. Standardize Transaction Category
if "TransactionCategory" in df.columns:
    df["TransactionCategory"] = (
        df["TransactionCategory"]
        .astype(str)
        .str.strip()
        .str.title()
    )
df["TransactionType"] = (
    df["TransactionType"]
    .astype(str)
    .str.strip()
    .str.title()
)
# 6. Remove duplicate records
duplicate_count = df.duplicated().sum()

print("\nDuplicate Records:")
print(duplicate_count)

df = df.drop_duplicates()
print("\nData Types After Cleaning:")
print(df.dtypes)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nCleaned Data:")
print(df.head())


# ------------------------------------------
# 8. Save cleaned dataset
# ------------------------------------------

df.to_csv(
    "blackrock_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully.")
print("\nActual Column Names:")
print(df.columns.tolist())
#Task2 DESCRIPTIVE TRANSACTIONAL ANALYSIS
monthly_summary = df.groupby(
    df["TransactionDate"].dt.to_period("M")
)["TransactionAmount"].agg(
    TotalTransactionAmount="sum",
    TransactionCount="count"
)

print("\nMonthly Transaction Summary:")
print(monthly_summary)


# Yearly Transaction Summary
yearly_summary = df.groupby(
    df["TransactionDate"].dt.year
)["TransactionAmount"].agg(
    TotalTransactionAmount="sum",
    TransactionCount="count"
)

print("\nYearly Transaction Summary:")
print(yearly_summary)

df["TransactionCategory"] = np.select(
    [
        df["TransactionType"] == "Deposit",
        df["TransactionType"].isin(["Withdrawal", "Payment"]),
        df["TransactionType"] == "Transfer"
    ],
    [
        "Credit",
        "Debit",
        "Transfer"
    ],
    default="Other"
)

credit_amount = df.loc[
    df["TransactionCategory"] == "Credit",
    "TransactionAmount"
].sum()

debit_amount = df.loc[
    df["TransactionCategory"] == "Debit",
    "TransactionAmount"
].sum()

net_transaction_volume = credit_amount - debit_amount

print("\nTransaction Category Distribution:")
print(df["TransactionCategory"].value_counts())

print("\nCredit Transaction Volume:")
print(credit_amount)

print("\nDebit Transaction Volume:")
print(debit_amount)

print("\nNet Transaction Volume:")
print(net_transaction_volume)

credit_by_account = df[
    df["TransactionCategory"] == "Credit"
].groupby("AccountID")["TransactionAmount"].sum()

debit_by_account = df[
    df["TransactionCategory"] == "Debit"
].groupby("AccountID")["TransactionAmount"].sum()

# Net Inflow = Total Credit - Total Debit
account_net_inflow = (
    credit_by_account
    .subtract(debit_by_account, fill_value=0)
    .sort_values(ascending=False)
)

print("\nTop 10 Accounts by Net Inflow:")
print(account_net_inflow.head(10))

print("\nBottom 10 Accounts by Net Inflow:")
print(account_net_inflow.tail(10))

df_sorted = df.sort_values(
    ["AccountID", "TransactionDate"]
).copy()

# Previous transaction date for each account
df_sorted["PreviousTransactionDate"] = (
    df_sorted.groupby("AccountID")["TransactionDate"].shift(1)
)

# Calculate gap in days
df_sorted["TransactionGapDays"] = (
    df_sorted["TransactionDate"]
    - df_sorted["PreviousTransactionDate"]
).dt.days

# Flag transactions with a gap of 60 days or more
dormant_transactions = df_sorted[
    df_sorted["TransactionGapDays"] >= 60
]

print("\nDormant Transaction Records:")
print(
    dormant_transactions[
        [
            "AccountID",
            "TransactionDate",
            "PreviousTransactionDate",
            "TransactionGapDays"
        ]
    ]
)

# Get unique dormant accounts
dormant_accounts = dormant_transactions[
    "AccountID"
].unique()

print("\nNumber of Dormant Accounts:")
print(len(dormant_accounts))

print("\nDormant Account IDs:")
print(dormant_accounts)

# TASK 3.1: CUSTOMER ACTIVITY PROFILE
customer_profile = df.groupby("CustomerID").agg(
    TransactionFrequency=("TransactionID", "count")
).reset_index()

# Activity Level
customer_profile["ActivityLevel"] = customer_profile[
    "TransactionFrequency"
].apply(
    lambda x: "Low" if x <= 3
    else ("Medium" if x <= 6 else "High")
)

print("\nCustomer Activity Profile:")
print(customer_profile.head(10))

print("\nActivity Level Counts:")
print(customer_profile["ActivityLevel"].value_counts())

# Average balance for each customer
average_balance = df.groupby("CustomerID")[
    "AccountBalance"
].mean()

# Add AverageBalance to customer profile
customer_profile["AverageBalance"] = (
    customer_profile["CustomerID"]
    .map(average_balance)
)

# Transaction volume based on frequency
customer_profile["TransactionVolume"] = customer_profile[
    "TransactionFrequency"
].apply(
    lambda x: "Low Volume" if x <= 4
    else "High Volume"
)

print("\nCustomer Profile with Balance & Transaction Volume:")
print(customer_profile.head(10))

print("\nTransaction Volume Counts:")
print(customer_profile["TransactionVolume"].value_counts())

print("\nAverage Balance by Transaction Volume:")
print(
    customer_profile.groupby("TransactionVolume")[
        "AverageBalance"
    ].mean()
)

final_customer_profile = customer_profile[
    [
        "CustomerID",
        "TransactionFrequency",
        "ActivityLevel",
        "AverageBalance",
        "TransactionVolume"
    ]
].copy()

print("\nFinal Customer Profile:")
print(final_customer_profile.head(10))

# Save customer profile
final_customer_profile.to_csv(
    "customer_profile.csv",
    index=False
)

print("\nCustomer profile saved successfully.")

# TASK 4.1: LARGE WITHDRAWALS
withdrawals = df[
    df["TransactionType"] == "Withdrawal"
]

large_withdrawal_threshold = withdrawals[
    "TransactionAmount"
].quantile(0.75)

large_withdrawals = withdrawals[
    withdrawals["TransactionAmount"]
    >= large_withdrawal_threshold
]

print("\nLarge Withdrawal Threshold:")
print(large_withdrawal_threshold)

print("\nNumber of Large Withdrawal Records:")
print(len(large_withdrawals))

print("\nLarge Withdrawal Records:")
print(
    large_withdrawals[
        [
            "AccountID",
            "TransactionDate",
            "TransactionAmount",
            "AccountBalance"
        ]
    ].head(20)
)

# Frequency by account
large_withdrawal_frequency = (
    large_withdrawals
    .groupby("AccountID")
    .size()
    .sort_values(ascending=False)
)

print("\nLarge Withdrawal Frequency by Account:")
print(large_withdrawal_frequency)

print("\nAccounts with Multiple Large Withdrawals:")
print(
    large_withdrawal_frequency[
        large_withdrawal_frequency > 1
    ]
)
balance_volatility = (
    df.groupby("AccountID")["AccountBalance"]
    .std()
    .sort_values(ascending=False)
)

print("\nBalance Volatility Statistics:")
print(balance_volatility.describe())

print("\nTop 10 Accounts by Balance Volatility:")
print(balance_volatility.head(10))

Q1 = df["TransactionAmount"].quantile(0.25)
Q3 = df["TransactionAmount"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - (1.5 * IQR)
upper_bound = Q3 + (1.5 * IQR)

anomalies = df[
    (df["TransactionAmount"] < lower_bound) |
    (df["TransactionAmount"] > upper_bound)
]

print("\nIQR Anomaly Detection:")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Bound:", lower_bound)
print("Upper Bound:", upper_bound)

print("\nNumber of Anomalous Transactions:")
print(len(anomalies))

print("\nAnomalous Transactions:")
print(
    anomalies[
        [
            "TransactionID",
            "AccountID",
            "TransactionType",
            "TransactionAmount",
            "AccountBalance"
        ]
    ]
)
risk_flags = pd.DataFrame(
    index=df["AccountID"].unique()
)

# Large withdrawal count
risk_flags["LargeWithdrawalCount"] = (
    large_withdrawals
    .groupby("AccountID")
    .size()
)

# Negative balance count
risk_flags["NegativeBalanceCount"] = (
    df[df["AccountBalance"] < 0]
    .groupby("AccountID")
    .size()
)

# Near-zero balance count
low_balance_threshold = (
    df["AccountBalance"].quantile(0.25)
)

risk_flags["NearZeroBalanceCount"] = (
    df[
        df["AccountBalance"] <= low_balance_threshold
    ]
    .groupby("AccountID")
    .size()
)

risk_flags = risk_flags.fillna(0)

# Count different risk indicators
risk_flags["RiskFlagCount"] = (
    (risk_flags["LargeWithdrawalCount"] > 1).astype(int)
    +
    (risk_flags["NegativeBalanceCount"] > 0).astype(int)
    +
    (risk_flags["NearZeroBalanceCount"] > 0).astype(int)
)

print("\nCombined Risk Indicators:")
print(
    risk_flags
    .sort_values(
        "RiskFlagCount",
        ascending=False
    )
    .head(20)
)
# TASK 5.1: MONTHLY CREDIT VS DEBIT TREND
monthly_credit = (
    df[df["TransactionCategory"] == "Credit"]
    .groupby(df["TransactionDate"].dt.to_period("M"))
    ["TransactionAmount"]
    .sum()
)

monthly_debit = (
    df[df["TransactionCategory"] == "Debit"]
    .groupby(df["TransactionDate"].dt.to_period("M"))
    ["TransactionAmount"]
    .sum()
)

monthly_credit.index = monthly_credit.index.astype(str)
monthly_debit.index = monthly_debit.index.astype(str)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_credit.index,
    monthly_credit.values,
    marker="o",
    label="Credit"
)

plt.plot(
    monthly_debit.index,
    monthly_debit.values,
    marker="o",
    label="Debit"
)

plt.title("Monthly Credit vs Debit Transactions")
plt.xlabel("Month")
plt.ylabel("Transaction Amount")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

transaction_type_counts = df[
    "TransactionType"
].value_counts()

plt.figure(figsize=(8, 5))

transaction_type_counts.plot(
    kind="bar"
)

plt.title("Transaction Type Distribution")
plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

regional_amount = (
    df.groupby("Region")["TransactionAmount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

regional_amount.plot(
    kind="bar"
)

plt.title("Total Transaction Amount by Region")
plt.xlabel("Region")
plt.ylabel("Transaction Amount")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

product_amount = (
    df.groupby("Product")["TransactionAmount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))

product_amount.plot(
    kind="bar"
)

plt.title("Transaction Amount by Product")
plt.xlabel("Product")
plt.ylabel("Transaction Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))

plt.scatter(
    df["CreditRating"],
    df["RiskScore"],
    alpha=0.6
)

plt.title("Risk Score vs Credit Rating")
plt.xlabel("Credit Rating")
plt.ylabel("Risk Score")
plt.tight_layout()
plt.show()

# activity_risk = pd.crosstab(
#     df["ActivityLevel"],
#     df["RiskLevel"]
# )

# plt.figure(figsize=(9, 6))

# sns.heatmap(
#     activity_risk,
#     annot=True,
#     fmt="d"
# )

# plt.title("Activity Level vs Risk Level")
# plt.xlabel("Risk Level")
# plt.ylabel("Activity Level")
# plt.tight_layout()
# plt.show()

# TASK 6: HYPOTHESIS 

volume_threshold = customer_profile[
    "TransactionFrequency"
].median()

print("\nTransaction Volume Threshold:")
print(volume_threshold)

customer_profile["VolumeGroup"] = customer_profile[
    "TransactionFrequency"
].apply(
    lambda x: "High Volume"
    if x > volume_threshold
    else "Low Volume"
)

print("\nTransaction Volume Groups:")
print(
    customer_profile["VolumeGroup"].value_counts()
)

print("\nAverage Balance by Volume Group:")
print(
    customer_profile.groupby("VolumeGroup")[
        "AverageBalance"
    ].mean()
)

from scipy.stats import ttest_ind

high_volume_balances = customer_profile[
    customer_profile["VolumeGroup"] == "High Volume"
]["AverageBalance"]

low_volume_balances = customer_profile[
    customer_profile["VolumeGroup"] == "Low Volume"
]["AverageBalance"]

t_stat, p_value_two_tailed = ttest_ind(
    high_volume_balances,
    low_volume_balances,
    equal_var=False
)

if t_stat > 0:
    p_value = p_value_two_tailed / 2
else:
    p_value = 1 - (p_value_two_tailed / 2)

print("\nHypothesis Test Results:")
print("T-statistic:", t_stat)
print("One-tailed P-value:", p_value)

alpha = 0.05

print("\nHypothesis Test Conclusion:")

if p_value < alpha:
    print("Reject H0.")
    print(
        "There is sufficient evidence that high-volume "
        "accounts have higher average balances."
    )
else:
    print("Fail to reject H0.")
    print(
        "There is insufficient evidence that high-volume "
        "accounts have higher average balances."
    )