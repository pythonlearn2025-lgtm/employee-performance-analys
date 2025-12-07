import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------
# Step 0 – Data Preparation
# -----------------------
np.random.seed(42)  # For reproducibility

# Create folder for images if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Employee names and departments
names = [f"Employee{i}" for i in range(1, 51)]
departments = ["Sales", "Marketing", "IT", "HR"]

# Create DataFrame
data = {
    "EmployeeID": range(1, 51),
    "Name": names,
    "Department": np.random.choice(departments, 50),
    "TasksCompleted": np.random.randint(10, 35, 50),
    "HoursWorked": np.random.randint(30, 50, 50),
    "SatisfactionScore": np.random.randint(5, 10, 50)
}

df = pd.DataFrame(data)

# Introduce missing values
nan_task = np.random.choice(df.index, 7, replace=False)
df.loc[nan_task, "TasksCompleted"] = np.nan
nan_satisfaction = np.random.choice(df.index, 3, replace=False)
df.loc[nan_satisfaction, "SatisfactionScore"] = np.nan

# Introduce negative HoursWorked
neg_hours = np.random.choice(df.index, 3, replace=False)
df.loc[neg_hours, "HoursWorked"] = -df.loc[neg_hours, "HoursWorked"]

# -----------------------
# Step 1 – Data Cleaning
# -----------------------
df["TasksCompleted"].fillna(df["TasksCompleted"].mean(), inplace=True)
df["SatisfactionScore"].fillna(df["SatisfactionScore"].mean(), inplace=True)
df["HoursWorked"] = df["HoursWorked"].abs()

# -----------------------
# Step 2 – KPI Calculation
# -----------------------
df["PerformanceKPI"] = (df["TasksCompleted"] /
                        df["HoursWorked"]) * df["SatisfactionScore"]

# Step 3 – KPI Normalization
df["KPI_normalized"] = (df["PerformanceKPI"] - df["PerformanceKPI"].min()) / \
    (df["PerformanceKPI"].max() - df["PerformanceKPI"].min())

# Step 4 – Best & Worst Employee
best_employeeid = df["PerformanceKPI"].idxmax()
namebest = df.loc[best_employeeid, "Name"]

worst_employeeid = df["PerformanceKPI"].idxmin()
nameworst = df.loc[worst_employeeid, "Name"]

print("Best Employee:", namebest)
print("Worst Employee:", nameworst)

# -----------------------
# Step 5 – Employee-wise Bar Chart
# -----------------------
df_sorted = df.sort_values(
    by="KPI_normalized", ascending=False).reset_index(drop=True)

plt.figure(figsize=(15, 6))
bars = plt.bar(df_sorted["Name"], df_sorted["KPI_normalized"], color="skyblue")
bars[df_sorted["KPI_normalized"].idxmax()].set_color("green")
bars[df_sorted["KPI_normalized"].idxmin()].set_color("red")
plt.title("Normalized Performance KPI per Employee", fontsize=16)
plt.xlabel("Employee Name", fontsize=12)
plt.ylabel("KPI Normalized", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/employee_kpi_bar.png")
plt.show()

# -----------------------
# Step 6 – Department-wise KPI
# -----------------------
dept_kpi = df.groupby("Department")[
    "KPI_normalized"].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
bars = plt.bar(dept_kpi.index, dept_kpi.values, color="lightcoral")
plt.title("Average Normalized KPI per Department", fontsize=14)
plt.xlabel("Department", fontsize=12)
plt.ylabel("Average KPI Normalized", fontsize=12)
plt.tight_layout()
plt.savefig("images/department_kpi_bar.png")
plt.show()

# -----------------------
# Step 7 – KPI Distribution (Histogram)
# -----------------------
plt.figure(figsize=(8, 5))
plt.hist(df["KPI_normalized"], bins=10, color="skyblue", edgecolor="black")
plt.title("Distribution of Normalized KPI", fontsize=14)
plt.xlabel("KPI Normalized", fontsize=12)
plt.ylabel("Number of Employees", fontsize=12)
plt.tight_layout()
plt.savefig("images/kpi_histogram.png")
plt.show()

# -----------------------
# Step 8 – Save final cleaned & KPI data
# -----------------------
df.to_csv("employee_performance_with_KPI.csv", index=False)
print("Final dataset saved to 'employee_performance_with_KPI.csv'")
