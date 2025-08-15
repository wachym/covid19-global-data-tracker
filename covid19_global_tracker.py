import pandas as pd

# Load dataset from local file
print("Loading COVID-19 data from local file...")
df = pd.read_csv("data/owid-covid-latest.csv")

# Preliminary checks
print("\nPreview of data:")
print(df.head())

print("\nColumns in dataset:")
print(df.columns)

print("\nMissing values per column:")
print(df.isnull().sum())

#  Data Cleaning

# 1. Pick the countries we want to focus on
countries = ['Kenya', 'United States', 'India']
df = df[df['location'].isin(countries)]

# 2. Drop rows with missing total_cases
df = df.dropna(subset=[ 'total_cases'])

# 3. Fill missing numbers with 0
df = df.fillna(0)

# Calculate death rate and percent vaccinated
df['death_rate'] = (df['total_deaths'] / df['total_cases']) * 100
df['percent_vaccinated'] = (df['people_fully_vaccinated'] / df['population']) * 100

print("\nCleaned Data Preview:")
print(df.head())
print("\nData types after cleaning:")
print(df.dtypes)


import matplotlib.pyplot as plt

# Make charts look nicer
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (8, 5)

# 1. Total cases per country
plt.bar(df['location'], df['total_cases'], color='blue')
plt.title('Total COVID-19 Cases (Latest Data)')
plt.ylabel('Total Cases')
plt.xlabel('Country')
plt.show()

# 2. Death rate per country
plt.bar(df['location'], df['death_rate'], color='red')
plt.title('COVID-19 Death Rate (%)')
plt.ylabel('Death Rate (%)')
plt.xlabel('Country')
plt.show()

# 3. Percent vaccinated per country
plt.bar(df['location'], df['percent_vaccinated'], color='green')
plt.title('Percent of Population Vaccinated')
plt.ylabel('% Vaccinated')
plt.xlabel('Country')
plt.show()

# Visualizing Vaccination Progress (Latest Data)

# Calculate unvaccinated percentage
df['percent_unvaccinated'] = 100 - df['percent_vaccinated']

# Plot vaccinated vs unvaccinated as stacked bar chart
fig, ax = plt.subplots()

# Vaccinated bars
ax.bar(df['location'], df['percent_vaccinated'], label='% Vaccinated', color='green')

# Unvaccinated bars stacked on top
ax.bar(df['location'], df['percent_unvaccinated'], bottom=df['percent_vaccinated'], label='% Unvaccinated', color='orange')

ax.set_ylabel('Percentage of Population')
ax.set_title('Vaccinated vs Unvaccinated Population')
ax.legend()

plt.show()

import plotly.express as px

# Choropleth Map for % Vaccinated
fig = px.choropleth(
    df,
    locations='location',
    locationmode='country names',
    color='percent_vaccinated',
    hover_name='location',
    color_continuous_scale='Greens',
    title='COVID-19 Vaccination Percentage by Country'
)

fig.show()

# Insights

print("\n--- Insights ---")
top_cases = df.sort_values(by='total_cases', ascending=False).iloc[0]
print(f"Highest total cases: {top_cases['location']} with {int(top_cases['total_cases']):,} cases")

top_death_rate = df.sort_values(by='death_rate', ascending=False).iloc[0]
print(f"Highest death rate: {top_death_rate['location']} at {top_death_rate['death_rate']:.2f}%")

top_vaccinated = df.sort_values(by='percent_vaccinated', ascending=False).iloc[0]
print(f"Highest vaccination rate: {top_vaccinated['location']} at {top_vaccinated['percent_vaccinated']:.2f}% of population vaccinated")


