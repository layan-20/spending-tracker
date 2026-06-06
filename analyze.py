# analyze.py
# A simple spending tracker: reads transactions, categorizes them,
# totals each category, and draws a chart.

# ---- Toolboxes we borrow (imports go at the top) ----
import pandas as pd
import matplotlib.pyplot as plt


# ---- Block 1: open the file and look at what's inside ----
df = pd.read_csv("sample_transactions.csv")
print(df)


# ---- Block 2: tidy the data so it's easy to search ----
# A lowercase copy of the description, so "SHELL" and "shell" match.
df["clean_desc"] = df["description"].str.lower()
# Tell pandas the date column is a real date, not just text.
df["date"] = pd.to_datetime(df["date"])
print(df)


# ---- Block 3: give each transaction a category ----
# Each category points to keywords that signal it.
rules = {
    "Groceries": ["harris teeter", "amazon mktpl"],
    "Gas": ["shell", "exxon"],
    "Coffee": ["starbucks"],
    "Dining": ["chick-fil-a"],
    "Subscriptions": ["netflix", "spotify"],
    "Rent": ["rent"],
}

# A mini-machine: takes one description, returns its category.
def categorize(desc):
    for category, keywords in rules.items():
        for word in keywords:
            if word in desc:          # keyword found in the text?
                return category       # label it and stop looking
    return "Other"                    # nothing matched

# Run that machine on every row; save answers in a new column.
df["category"] = df["clean_desc"].apply(categorize)
print(df[["description", "amount", "category"]])


# ---- Block 4: total up the spending in each category ----
totals = df.groupby("category")["amount"].sum()
totals = totals.sort_values(ascending=False)   # biggest first
print(totals)


# ---- Block 5: draw a bar chart and save it ----
totals.plot(kind="bar")
plt.title("Spending by Category")
plt.ylabel("Dollars")
plt.tight_layout()                              # stop labels cutting off
plt.savefig("spending_by_category.png")         # save image for README
plt.show()                                      # pop it on screen