import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database (replace with your actual database connection)
try:
    conn = sqlite3.connect('hr_database.db')  # Replace with your actual database connection
    print("Database connection successful!")
except sqlite3.Error as e:
    print(f"Error connecting to SQLite database: {e}")
    exit()

# Example 1: The average age of employees in each department and gender group
query_1 = """
SELECT department, gender, ROUND(AVG(age), 2) AS average_age
FROM employee
GROUP BY department, gender;
"""
try:
    df_avg_age = pd.read_sql_query(query_1, conn)
    print("Average Age by Department and Gender:")
    print(df_avg_age)
except Exception as e:
    print(f"Error executing query 1: {e}")

# Example 2: The top 3 departments with the highest average training scores
query_2 = """
SELECT department, ROUND(AVG(avg_training_score), 2) AS average_training_score
FROM employee
GROUP BY department
ORDER BY average_training_score DESC
LIMIT 3;
"""
try:
    df_top_3_departments = pd.read_sql_query(query_2, conn)
    print("Top 3 Departments by Average Training Score:")
    print(df_top_3_departments)
except Exception as e:
    print(f"Error executing query 2: {e}")

# Example 3: The percentage of employees who have won awards in each region
query_3 = """
SELECT region, ROUND((SUM(awards_won) / COUNT(*) * 100), 2) AS percentage_award_winning
FROM employee
GROUP BY region;
"""
try:
    df_awards_percentage = pd.read_sql_query(query_3, conn)
    print("Percentage of Employees Who Have Won Awards by Region:")
    print(df_awards_percentage)
except Exception as e:
    print(f"Error executing query 3: {e}")

# Example 4: The number of employees who have met more than 80% of KPIs for each recruitment channel and education level
query_4 = """
SELECT recruitment_channel, education, COUNT(*) AS num_employees
FROM employee
WHERE KPIs_met_more_than_80 = 1
GROUP BY recruitment_channel, education;
"""
try:
    df_kpis_met = pd.read_sql_query(query_4, conn)
    print("Employees who met more than 80% of KPIs by Recruitment Channel and Education Level:")
    print(df_kpis_met)
except Exception as e:
    print(f"Error executing query 4: {e}")

# Example 5: The average length of service for employees in each department, considering only employees with previous year ratings >= 4
query_5 = """
SELECT department, ROUND(AVG(length_of_service), 2) AS average_length_of_service
FROM employee
WHERE previous_year_rating >= 4
GROUP BY department;
"""
try:
    df_avg_length_of_service = pd.read_sql_query(query_5, conn)
    print("Average Length of Service by Department (Previous Year Rating >= 4):")
    print(df_avg_length_of_service)
except Exception as e:
    print(f"Error executing query 5: {e}")

# Example 6: The top 5 regions with the highest average previous year ratings
query_6 = """
SELECT region, ROUND(AVG(previous_year_rating), 2) AS average_previous_year_rating
FROM employee
GROUP BY region
ORDER BY average_previous_year_rating DESC
LIMIT 5;
"""
try:
    df_top_5_regions = pd.read_sql_query(query_6, conn)
    print("Top 5 Regions by Average Previous Year Ratings:")
    print(df_top_5_regions)
except Exception as e:
    print(f"Error executing query 6: {e}")

# Example 7: The departments with more than 100 employees having a length of service greater than 5 years
query_7 = """
SELECT department
FROM employee
WHERE department IN (
    SELECT department
    FROM employee
    WHERE length_of_service > 5
    GROUP BY department
    HAVING COUNT(*) > 100
);
"""
try:
    df_departments_100 = pd.read_sql_query(query_7, conn)
    print("Departments with More Than 100 Employees and Length of Service > 5 years:")
    print(df_departments_100)
except Exception as e:
    print(f"Error executing query 7: {e}")

# Example 8: The average length of service for employees who have attended more than 3 trainings, grouped by department and gender
query_8 = """
SELECT department, gender, ROUND(AVG(length_of_service), 2) AS average_length_of_service
FROM employee
WHERE no_of_trainings > 3
GROUP BY department, gender;
"""
try:
    df_avg_length_training = pd.read_sql_query(query_8, conn)
    print("Average Length of Service by Department and Gender (Attended more than 3 Trainings):")
    print(df_avg_length_training)
except Exception as e:
    print(f"Error executing query 8: {e}")

# Example 9: The percentage of female employees who have won awards, per department
query_9 = """
SELECT department,
       COUNT(CASE WHEN gender = 'f' THEN 1 END) AS num_female_employees,
       COUNT(CASE WHEN gender ='f' AND awards_won = 1 THEN 1 END) AS num_female_employees_awarded,
       ROUND((COUNT(CASE WHEN gender = 'f' AND awards_won = 1 THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN gender = 'f' THEN 1 END), 0)), 2) AS percentage_female_awarded
FROM employee
GROUP BY department;
"""
try:
    df_female_awards = pd.read_sql_query(query_9, conn)
    print("Percentage of Female Employees Who Have Won Awards by Department:")
    print(df_female_awards)
except Exception as e:
    print(f"Error executing query 9: {e}")

# Example 10: The percentage of employees per department who have a length of service between 5 and 10 years
query_10 = """
SELECT department,
       ROUND((COUNT(CASE WHEN length_of_service >= 5 AND length_of_service <= 10 THEN 1 END) * 100.0 / COUNT(*)), 2) AS percentage
FROM employee
GROUP BY department;
"""
try:
    df_length_of_service_5_10 = pd.read_sql_query(query_10, conn)
    print("Percentage of Employees with Length of Service Between 5 and 10 Years by Department:")
    print(df_length_of_service_5_10)
except Exception as e:
    print(f"Error executing query 10: {e}")

# Example 11: The top 3 regions with the highest number of employees who have met more than 80% of their KPIs and received at least one award, grouped by department and region
query_11 = """
SELECT department, region, COUNT(*) AS num_employees
FROM employee
WHERE KPIs_met_more_than_80 = 1 AND awards_won > 0
GROUP BY department, region
ORDER BY num_employees DESC
LIMIT 3;
"""
try:
    df_top_3_kpi_awards = pd.read_sql_query(query_11, conn)
    print("Top 3 Regions with Employees Meeting KPIs and Receiving Awards:")
    print(df_top_3_kpi_awards)
except Exception as e:
    print(f"Error executing query 11: {e}")

# Example 12: The average length of service for employees per education level and gender, considering only those employees who have completed more than 2 trainings and have an average training score greater than 75
query_12 = """
SELECT education, gender, ROUND(AVG(length_of_service), 2) AS average_length_of_service
FROM employee
WHERE no_of_trainings > 2 AND avg_training_score > 75
GROUP BY education, gender;
"""
try:
    df_avg_length_education_gender = pd.read_sql_query(query_12, conn)
    print("Average Length of Service by Education and Gender (More than 2 Trainings and Avg Training Score > 75):")
    print(df_avg_length_education_gender)
except Exception as e:
    print(f"Error executing query 12: {e}")

# Example 13: For each department and recruitment channel, the total number of employees who have met more than 80% of their KPIs, have a previous_year_rating of 5, and have a length of service greater than 10 years
query_13 = """
SELECT department, recruitment_channel, COUNT(*) AS num_employees
FROM employee
WHERE KPIs_met_more_than_80 = 1 AND previous_year_rating = 5 AND length_of_service > 10
GROUP BY department, recruitment_channel;
"""
try:
    df_kpi_previous_year_rating = pd.read_sql_query(query_13, conn)
    print("Employees Meeting KPIs, Rating 5, and Length of Service > 10 by Department and Recruitment Channel:")
    print(df_kpi_previous_year_rating)
except Exception as e:
    print(f"Error executing query 13: {e}")

# Example 14: The percentage of employees in each department who have received awards, have a previous_year_rating of 4 or 5, and an average training score above 70, grouped by department and gender
query_14 = """
SELECT department, gender,
       ROUND((COUNT(CASE WHEN awards_won = 1 AND (previous_year_rating = 4 OR previous_year_rating = 5) AND avg_training_score > 70 THEN 1 END) * 100.0 / COUNT(*)), 2) AS percentage_awarded
FROM employee
GROUP BY department, gender;
"""
try:
    df_awards_percentage_previous_rating = pd.read_sql_query(query_14, conn)
    print("Percentage of Employees Awarded with Rating >= 4 and Avg Training Score > 70 by Department and Gender:")
    print(df_awards_percentage_previous_rating)
except Exception as e:
    print(f"Error executing query 14: {e}")

# Example of plotting data:
# For Example 5: Average Length of Service by Department
if not df_avg_length_of_service.empty:
    plt.figure(figsize=(10, 6))
    sns.barplot(x='department', y='average_length_of_service', data=df_avg_length_of_service)
    plt.title('Average Length of Service by Department')
    plt.xlabel('Department')
    plt.ylabel('Average Length of Service')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("DataFrame for average length of service by department is empty.")

# Always close the connection when you're done
conn.close()
