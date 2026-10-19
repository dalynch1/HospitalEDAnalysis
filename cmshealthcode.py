import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(
    "Timely_and_Effective_Care-Hospital.csv",
    dtype={"Facility ID": "string", "ZIP Code": "string"},
    low_memory=False
)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

df.head()


df.info()

print(df.describe(include="all").T)

missing_summary = pd.DataFrame({
    "Missing Count": df.isna().sum(),
    "Missing Percent": (df.isna().mean() * 100).round(2)
}).sort_values("Missing Percent", ascending=False)

print(missing_summary)

print("Unique hospitals:", df["Facility ID"].nunique())
print("Unique states:", df["State"].nunique())
print("Unique conditions:", df["Condition"].nunique())
print("Unique measures:", df["Measure ID"].nunique())

# print("\nScore values:")
# print(sorted(df["Score"].dropna().astype(str).unique()))

# print("\nSample values:")
# print(sorted(df["Sample"].dropna().astype(str).unique()))


df.columns = df.columns.str.strip()

text_columns = [
    "Facility ID", "Facility Name", "Address", "City/Town",
    "State", "ZIP Code", "County/Parish", "Telephone Number",
    "Condition", "Measure ID", "Measure Name", "Score",
    "Sample", "Footnote"
]

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# Convert empty strings into actual missing values
df[text_columns] = df[text_columns].replace(
    r"^\s*$", pd.NA, regex=True
)

# Standardize state codes
df["State"] = df["State"].str.upper()

# Convert scores to numeric where possible
df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

# Convert sample size to numeric where possible
df["Sample"] = pd.to_numeric(df["Sample"], errors="coerce")

# Parse reporting dates
for col in ["Start Date", "End Date"]:
    df[col] = pd.to_datetime(
        df[col],
        format="%m/%d/%Y",
        errors="coerce"
    )

df[["Facility ID", "State", "Measure ID",
    "Score", "Start Date", "End Date"]].head()


exact_duplicates = df.duplicated().sum()

print("Exact duplicate rows:", exact_duplicates)

df = df.drop_duplicates().copy()

print("Shape after removing exact duplicates:", df.shape)


record_key = [
    "Facility ID",
    "Measure ID",
    "Start Date",
    "End Date"
]

duplicate_keys = df.duplicated(
    subset=record_key,
    keep=False
)

print("Rows sharing a hospital-measure-period key:",
      duplicate_keys.sum())

print(
    df.loc[duplicate_keys]
      .sort_values(record_key)
      .head(20)
)


df["Score Original"] = df["Score"]

df["Score Numeric"] = pd.to_numeric(
    df["Score"],
    errors="coerce"
)

print(
    df["Score"]
    .value_counts(dropna=False)
    .head(30)
)

# Values that could not be converted to numbers
nonnumeric_scores = df.loc[
    df["Score"].notna() &
    df["Score Numeric"].isna(),
    ["Measure ID", "Measure Name", "Score", "Footnote"]
]

print("Non-numeric score rows:", len(nonnumeric_scores))

print(nonnumeric_scores.head(20))


print(
    "Rows with missing or nonnumeric scores:",
    df["Score Numeric"].isna().sum()
)

print(
    "Percentage without numeric scores:",
    round(df["Score Numeric"].isna().mean() * 100, 2),
    "%"
)

print("Missing Sample:", df["Sample"].isna().sum())
print("Missing Footnote:", df["Footnote"].isna().sum())

print("\nFootnote codes:")
print(df["Footnote"].value_counts(dropna=False).head(20))

# Missing identifiers
print("Missing facility IDs:", df["Facility ID"].isna().sum())
print("Missing measure IDs:", df["Measure ID"].isna().sum())

# Invalid reporting periods
invalid_dates = df[
    df["Start Date"].isna() |
    df["End Date"].isna() |
    (df["Start Date"] > df["End Date"])
]

print("Invalid reporting periods:", len(invalid_dates))

# Inspect numeric score ranges by measure
score_ranges = (
    df.dropna(subset=["Score Numeric"])
      .groupby(["Measure ID", "Measure Name"])["Score Numeric"]
      .agg(["count", "min", "median", "max"])
      .sort_values("count", ascending=False)
)

print(score_ranges.head(10))


plt.figure(figsize=(12, 6))

df["Condition"].value_counts().head(12).sort_values().plot(
    kind="barh",
    color="steelblue"
)

plt.title("Number of Records by Healthcare Condition")
plt.xlabel("Number of Records")
plt.ylabel("Condition")
plt.tight_layout()
plt.show()

measure_counts = (
    df.groupby(["Measure ID", "Measure Name"])
      .size()
      .sort_values(ascending=False)
)

print(measure_counts.head(15))


state_counts = df["State"].value_counts().head(15)

state_counts.sort_values().plot(
    kind="barh",
    figsize=(10, 6),
    color="teal"
)

plt.title("States with the Most Hospital Measure Records")
plt.xlabel("Record Count")
plt.ylabel("State")
plt.tight_layout()
plt.show()

hospitals_by_state = (
    df.groupby("State")["Facility ID"]
      .nunique()
      .sort_values(ascending=False)
)

print(hospitals_by_state.head(15))

plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="Score Numeric",
    bins=40,
    kde=True
)

plt.title("Distribution of Numeric Scores")
plt.xlabel("Reported score")
plt.ylabel("Number of records")
plt.tight_layout()
plt.show()

op18a = df[df["Measure ID"] == "OP_18a"].copy()

print("OP_18a records:", len(op18a))

print(
    op18a[
        ["Facility ID", "Facility Name", "State",
         "Measure Name", "Score", "Score Numeric",
         "Sample", "Footnote"]
    ].head(10)
)

op18a_numeric = op18a.dropna(
    subset=["Score Numeric"]
).copy()

print("Numeric OP_18a records:", len(op18a_numeric))

print(
    "Unique hospitals:",
    op18a_numeric["Facility ID"].nunique()
)

print(
    op18a_numeric["Score Numeric"].describe()
)

state_performance = (
    op18a_numeric.groupby("State")
    .agg(
        Hospital_Count=("Facility ID", "nunique"),
        Median_ED_Time=("Score Numeric", "median"),
        Mean_ED_Time=("Score Numeric", "mean")
    )
    .reset_index()
)

state_performance = state_performance.sort_values(
    "Median_ED_Time",
    ascending=True
)

print(state_performance.head(15))

plot_data = state_performance.nsmallest(
    15, "Median_ED_Time"
)

plt.figure(figsize=(10, 7))

sns.barplot(
    data=plot_data,
    x="Median_ED_Time",
    y="State",
    color="steelblue"
)

plt.title("States with the Lowest Median Reported ED Times")
plt.xlabel("Median time (minutes)")
plt.ylabel("State")
plt.tight_layout()
plt.show()

q1 = op18a_numeric["Score Numeric"].quantile(0.25)
q3 = op18a_numeric["Score Numeric"].quantile(0.75)

iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

op18a_numeric["Outlier"] = (
    (op18a_numeric["Score Numeric"] < lower_bound) |
    (op18a_numeric["Score Numeric"] > upper_bound)
)

print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)
print("Flagged records:", op18a_numeric["Outlier"].sum())

outliers = op18a_numeric.loc[
    op18a_numeric["Outlier"],
    [
        "Facility ID", "Facility Name", "State",
        "Score Numeric", "Sample", "Footnote"
    ]
].sort_values("Score Numeric", ascending=False)

print(outliers.head(20))

plt.figure(figsize=(10, 5))

sns.boxplot(
    data=op18a_numeric,
    x="Score Numeric",
    color="lightblue"
)

plt.title("Emergency Department Time: Outlier Detection")
plt.xlabel("Reported median time (minutes)")
plt.tight_layout()
plt.show()



df.to_csv(
    "cms_hospital_quality_cleaned.csv",
    index=False
)

state_performance.to_csv(
    "ed_time_by_state.csv",
    index=False
)

outliers.to_csv(
    "ed_time_potential_outliers.csv",
    index=False
)

