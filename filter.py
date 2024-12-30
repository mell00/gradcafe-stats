import pandas as pd

# Load your CSV into a DataFrame
df = pd.read_csv("gradcafe.csv")

# 1. Convert the existing string dates to actual datetime objects:
df["Date_Posted"] = pd.to_datetime(
    df["Date_Posted"],
    format="%B %d, %Y",     # <-- This is the matching format for "December 25, 2024"
    errors="coerce"         # If a date doesn't parse, it becomes NaT instead of erroring
)

df["DecisionDate"] = pd.to_datetime(
    df["DecisionDate"],
    format="%B %d, %Y",     # <-- This is the matching format for "December 25, 2024"
    errors="coerce"         # If a date doesn't parse, it becomes NaT instead of erroring
)

# 2. (Optional) Convert datetime objects to a uniform string format, e.g. YYYY-MM-DD:
df["Date_Posted"] = df["Date_Posted"].dt.strftime("%Y-%m-%d")
df["DecisionDate"] = df["DecisionDate"].dt.strftime("%Y-%m-%d")



# Just check if "UCLA" is anywhere in the School column
#mask_ucla = df["School"].str.contains("University of California-Los Angeles", na=False)
#print(df[mask_ucla].head())


# Build the boolean mask to remove:
to_filter = (
    # Condition A: Statistics PhD at UCLA or Stanford
    #((df["Program"] == "Statistics") &
     #(df["Degree_Type"] == "PhD") &
     #(df["School"].isin(["UCLA", "Columbia University"])))
    #|
    # Condition B: Statistical Science PhD at Duke
    #((df["Program"] == "Statistical Science") &
     #(df["Degree_Type"] == "PhD") &
     #(df["School"] == "Duke University"))

    ((df["Degree_Type"] == "PhD") &
     (df["School"] == "University of California-San Diego"))
)

# Filter out the rows matching those criteria
df_filtered = df[to_filter]
print(df_filtered.head(20))
print("Filtered out the specified rows. New CSV saved as gradcafe_filtered.csv.")
