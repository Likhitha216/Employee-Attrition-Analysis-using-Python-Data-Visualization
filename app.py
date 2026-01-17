import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/HR_Analytics.csv")

# Select relevant columns
df = df[[
    "EmployeeNumber",
    "Department",
    "JobRole",
    "MonthlyIncome",
    "YearsAtCompany",
    "PerformanceRating",
    "WorkLifeBalance",
    "Attrition"
]]

# Create SQLite database
conn = sqlite3.connect("hr_database.db")
df.to_sql("employees", conn, if_exists="replace", index=False)

# SQL Queries
attrition_query = """
SELECT Department,
       COUNT(*) AS TotalEmployees,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS AttritionCount
FROM employees
GROUP BY Department;
"""
attrition_df = pd.read_sql(attrition_query, conn)

salary_query = """
SELECT JobRole, AVG(MonthlyIncome) AS AvgSalary
FROM employees
GROUP BY JobRole
ORDER BY AvgSalary DESC;
"""
salary_df = pd.read_sql(salary_query, conn)

experience_query = """
SELECT YearsAtCompany, AVG(MonthlyIncome) AS AvgIncome
FROM employees
GROUP BY YearsAtCompany;
"""
experience_df = pd.read_sql(experience_query, conn)

# Visualization
plt.figure(figsize=(15,10))

plt.subplot(2,2,1)
sns.barplot(x="Department", y="AttritionCount", data=attrition_df)
plt.title("Attrition by Department")

plt.subplot(2,2,2)
sns.barplot(y="JobRole", x="AvgSalary", data=salary_df.head(8))
plt.title("Top Paid Roles")

plt.subplot(2,2,3)
sns.lineplot(x="YearsAtCompany", y="AvgIncome", data=experience_df, marker="o")
plt.title("Experience vs Salary")

plt.subplot(2,2,4)
sns.countplot(x="Attrition", data=df)
plt.title("Overall Attrition")

plt.tight_layout()
plt.show()

conn.close()
