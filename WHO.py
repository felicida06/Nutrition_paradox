import streamlit as st
import pandas as pd
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt

st.title("World Health Organization")

myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='Alby@0308',database = "WHO")
cur = myconnection.cursor()

from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("W.H.O", ["Home","Filter criteria", 'Queries'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    

if selected == "Home":
                    
                    st.write("World Health Organization")

                    st.markdown("Upload JSON files for *Obesity* and *Malnutrition*")

# Upload JSON files
obesity_file = st.file_uploader("Upload Obesity JSON", type=["json"])
malnutrition_file = st.file_uploader("Upload Malnutrition JSON", type=["json"])

# Read and display data
if obesity_file is not None and malnutrition_file is not None:
    df_obesity = pd.read_json(obesity_file, lines=True)
    df_malnutrition = pd.read_json(malnutrition_file, lines=True)

    

    # Histogram
    st.subheader("🔸 Histogram (Obesity %)")
    selected_column = st.selectbox("Select column for histogram", df_obesity.columns)
    plt.figure(figsize=(8, 4))
    plt.hist(df_obesity[selected_column].dropna(), bins=20, color='skyblue', edgecolor='black')
    st.pyplot(plt)

    # Bar Chart
    st.subheader("🔸 Bar Chart (Malnutrition)")
    category_col = st.selectbox("Select category column", df_malnutrition.columns)
    value_col = st.selectbox("Select value column", df_malnutrition.select_dtypes(include='number').columns)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=category_col, y=value_col, data=df_malnutrition.head(10), ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Line Plot 
    st.subheader("Line Plot (Obesity)")
    x_col = st.selectbox("Select X-axis column for line plot:", df_obesity.columns)
    line_col = st.selectbox(
    "Select numeric column for line plot:", 
    df_obesity.select_dtypes(include='number').columns)
    yearly_avg = df_obesity.groupby('Year')['Mean_Estimate'].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.lineplot(x='Year', y='Mean_Estimate', data=yearly_avg, ax=ax2)
    plt.title('Mean Estimate Trend Over Years')
    plt.xlabel('Year')
    plt.ylabel('Mean Estimate')
    st.pyplot(fig2)

    # Box Plot
    st.subheader("🔸 Box Plot (Malnutrition)")
    box_col = st.selectbox("Select numeric column for box plot", df_malnutrition.select_dtypes(include='number').columns)
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.boxplot(y=df_malnutrition[box_col], ax=ax3)
    st.pyplot(fig3)

    
if selected == 'Queries':  

                    options = st.selectbox("Queries",[" 1.Top 5 regions with the highest average obesity levels in the most recent year(2022)",
                                                      "2.Top 5 countries with highest obesity estimates",
                                                      "3.Obesity trend in India over the years(Mean_estimate)",
                                                      "4.Average obesity by gender",
                                                      "5.Country count by obesity level category and age group",
                                                      "6.Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)",
                                                      "7.Average obesity by age group",
                                                      "8.Top 10 Countries with consistent low obesity (low average + low CI)over the years",
                                                      "9.Countries where female obesity exceeds male by large margin (same year)",
                                                      "10.Global average obesity percentage per year",
                                                      "11.Avg.malnutrition by age group",
                                                      "12.Top 5 countries with highest malnutrition(mean_estimate)",
                                                      "13.Malnutrition trend in African region over the years",
                                                      "14.Gender-based average malnutrition",
                                                      "15.Malnutrition level-wise (average CI_Width by age group)",
                                                      "16.Yearly malnutrition change in specific countries(India, Nigeria, Brazil)",
                                                      "17.Regions with lowest malnutrition averages",
                                                      "18.Countries with increasing malnutrition (💡 Hint: Use MIN() and MAX()   on Mean_Estimate per country to compare early vs. recent malnutrition levels, and filter where the difference is positive using HAVING.)",
                                                      "19. Min/Max malnutrition levels year-wise comparison",
                                                      "20.High CI_Width flags for monitoring(CI_width > 5)",
                                                      "21.Obesity vs malnutrition comparison by country(any 5 countries)",
                                                      "22.Gender-based disparity in both obesity and malnutrition",
                                                      "23.Region-wise avg estimates side-by-side(Africa and America)",
                                                      "24.Countries with obesity up & malnutrition down",
                                                      "25.Age-wise trend analysis"],placeholder='Choose an option..',index=None)

                    if options == " 1.Top 5 regions with the highest average obesity levels in the most recent year(2022)":
                                            cur.execute('SELECT Region, AVG(Mean_Estimate) AS Avg_Obesity FROM obesity WHERE Year = 2022 GROUP BY Region ORDER BY Avg_Obesity DESC LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description] 
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "2.Top 5 countries with highest obesity estimates":
                                            cur.execute('SELECT Country, MAX(Mean_Estimate) AS Max_Obesity FROM obesity GROUP BY Country ORDER BY Max_Obesity DESC LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "3.Obesity trend in India over the years(Mean_estimate)":
                                            cur.execute('SELECT Year, AVG(Mean_Estimate) AS Avg_Obesity FROM obesity WHERE Country = "India"GROUP BY Year ORDER BY Year')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "4.Average obesity by gender":
                                            cur.execute('SELECT Gender, AVG(Mean_Estimate) as avg_Obesity from obesity GROUP BY Gender')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "5.Country count by obesity level category and age group":
                                            cur.execute('SELECT obesity_level, age_group, COUNT(DISTINCT Country) AS Country_Count FROM obesity GROUP BY obesity_level, age_group')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "6.Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)":
                                            cur.execute('SELECT Country, AVG(CI_Width) AS Avg_CI FROM obesity GROUP BY Country ORDER BY Avg_CI DESC LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "7.Average obesity by age group":
                                            cur.execute('SELECT age_group, avg(Mean_Estimate) as avg_Obesity FROM obesity GROUP BY age_group')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "8.Top 10 Countries with consistent low obesity (low average + low CI)over the years":
                                            cur.execute('SELECT Country, AVG(Mean_Estimate) AS Avg_Obesity, AVG(CI_Width) AS Avg_CI FROM obesity GROUP BY Country HAVING Avg_Obesity < 20 AND Avg_CI < 5 ORDER BY Avg_Obesity ASC, Avg_CI ASC LIMIT 10')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "9.Countries where female obesity exceeds male by large margin (same year)":
                                            cur.execute('SELECT f.Country, f.Year, f.Mean_Estimate AS Female_Obesity, m.Mean_Estimate AS Male_Obesity,(f.Mean_Estimate - m.Mean_Estimate) AS Difference FROM obesity f JOIN obesity m ON f.Country = m.Country AND f.Year = m.Year WHERE f.Gender = "Female" AND m.Gender = "Male" AND (f.Mean_Estimate - m.Mean_Estimate) > 5 ORDER BY Difference DESC limit 10')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "10.Global average obesity percentage per year":
                                            cur.execute('SELECT Year, AVG(Mean_Estimate) AS Global_Avg_Obesity FROM obesity GROUP BY Year ORDER BY Year')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "11.Avg.malnutrition by age group":
                                            cur.execute('select age_group, AVG(Mean_Estimate) as avg_malnutrition from malnutrition group by age_group order by avg_malnutrition desc')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "12.Top 5 countries with highest malnutrition(mean_estimate)":
                                            cur.execute('SELECT country, AVG(mean_estimate) AS avg_malnutrition FROM malnutrition GROUP BY country ORDER BY avg_malnutrition DESC LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "13.Malnutrition trend in African region over the years":
                                            cur.execute('SELECT year, AVG(mean_estimate) AS avg_malnutrition FROM malnutrition WHERE region = "Africa" GROUP BY year ORDER BY year')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "14.Gender-based average malnutrition":
                                            cur.execute('SELECT gender, AVG(mean_estimate) AS avg_malnutrition FROM malnutrition GROUP BY gender')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "15.Malnutrition level-wise (average CI_Width by age group)":
                                            cur.execute('SELECT age_group, AVG(CI_Width) AS average_CI_width FROM malnutrition GROUP BY age_group ORDER BY average_CI_width DESC')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "16.Yearly malnutrition change in specific countries(India, Nigeria, Brazil)":
                                            cur.execute('SELECT country, year, AVG(mean_estimate) AS avg_malnutrition FROM malnutrition WHERE country IN ("India", "Nigeria", "Brazil") GROUP BY country, year ORDER BY country, year')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)

                    elif options == "17.Regions with lowest malnutrition averages":
                                            cur.execute('SELECT region, AVG(mean_estimate) AS avg_malnutrition FROM malnutrition GROUP BY region ORDER BY avg_malnutrition ASC')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "18.Countries with increasing malnutrition (💡 Hint: Use MIN() and MAX()   on Mean_Estimate per country to compare early vs. recent malnutrition levels, and filter where the difference is positive using HAVING.)":
                                            cur.execute('SELECT country, MAX(mean_estimate) - MIN(mean_estimate) AS increase_in_malnutrition FROM malnutrition GROUP BY country HAVING increase_in_malnutrition > 0 ORDER BY increase_in_malnutrition DESC')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "19. Min/Max malnutrition levels year-wise comparison":
                                            cur.execute('SELECT year, MIN(mean_estimate) AS min_malnutrition, MAX(mean_estimate) AS max_malnutrition FROM malnutrition GROUP BY year ORDER BY year')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "20.High CI_Width flags for monitoring(CI_width > 5)":
                                            cur.execute('SELECT * FROM malnutrition WHERE CI_Width > 5 ORDER BY CI_Width DESC limit 20')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "21.Obesity vs malnutrition comparison by country(any 5 countries)":
                                            cur.execute('SELECT o.country, AVG(o.mean_estimate) AS avg_obesity, AVG(m.mean_estimate) AS avg_malnutrition FROM obesity o JOIN malnutrition m ON o.country = m.country WHERE o.country IN ("India", "Brazil", "USA", "Nigeria", "Mexico") GROUP BY o.country')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)

                    elif options == "22.Gender-based disparity in both obesity and malnutrition":
                                            cur.execute('SELECT o.gender, AVG(o.mean_estimate) AS avg_obesity, AVG(m.mean_estimate) AS avg_malnutrition FROM obesity o JOIN malnutrition m ON o.gender = m.gender AND o.country = m.country AND o.year = m.year GROUP BY o.gender')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "23.Region-wise avg estimates side-by-side(Africa and America)":
                                            cur.execute('SELECT o.region, AVG(o.mean_estimate) AS avg_obesity, AVG(m.mean_estimate) AS avg_malnutrition FROM obesity o JOIN malnutrition m ON o.region = m.region AND o.country = m.country WHERE o.region IN ("Africa", "America") GROUP BY o.region')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "24.Countries with obesity up & malnutrition down":
                                            cur.execute('WITH obesity_trend AS (SELECT country, FIRST_VALUE(mean_estimate) OVER (PARTITION BY country ORDER BY year) AS first_obesity, LAST_VALUE(mean_estimate) OVER (PARTITION BY country ORDER BY year ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_obesity FROM obesity), malnutrition_trend AS (SELECT country, FIRST_VALUE(mean_estimate) OVER (PARTITION BY country ORDER BY year) AS first_malnutrition, LAST_VALUE(mean_estimate) OVER (PARTITION BY country ORDER BY year ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_malnutrition FROM malnutrition) SELECT o.country FROM (SELECT DISTINCT country FROM obesity_trend WHERE last_obesity > first_obesity) AS o INTERSECT SELECT m.country FROM (SELECT DISTINCT country FROM malnutrition_trend WHERE last_malnutrition < first_malnutrition) AS m')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "25.Age-wise trend analysis":
                                            cur.execute('SELECT o.age_group, AVG(o.mean_estimate) AS avg_obesity, AVG(m.mean_estimate) AS avg_malnutrition FROM obesity o JOIN malnutrition m ON o.age_group = m.age_group AND o.country = m.country GROUP BY o.age_group')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
myconnection.commit()





                                                     
































    