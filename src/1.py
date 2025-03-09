from data import df_cleaned
print("🚀 df_cleaned sample:\n", df_cleaned.head())


import pandas as pd
import numpy as np
import altair as alt

# loading the data 
df = pd.read_csv('../data/Billionaires Statistics Dataset.csv', encoding="ISO-8859-1")

# preprocessing data
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

# cleaning data
df_cleaned = df[['finalWorth', 'category', 'personName', 'age', 'country',
       'city','source', 'industries', 'countryOfCitizenship', 'organization',
       'selfMade', 'status', 'gender', 'birthDate', 'lastName', 'firstName',
       'title', 'date', 'state', 'residenceStateRegion', 'birthYear',
       'birthMonth', 'birthDay', 'cpi_country', 'cpi_change_country',
       'gdp_country', 'gross_tertiary_education_enrollment',
       'gross_primary_education_enrollment_country', 'life_expectancy_country',
       'tax_revenue_country_country', 'total_tax_rate_country',
       'population_country']].copy()

df_cleaned["finalWorth"] = df_cleaned["finalWorth"].fillna(0).astype(float)
df_cleaned["birthYear"] = df_cleaned["birthYear"].fillna(0).astype(int)
df_cleaned["category"] = df_cleaned["category"].fillna("Unknown")
df_cleaned["country"] = df_cleaned["country"].fillna("Unknown")
df_cleaned["city"] = df_cleaned["city"].fillna("Unknown")
df_cleaned["industries"] = df_cleaned["industries"].fillna("Unknown")
df_cleaned["source"] = df_cleaned["source"].fillna("Unknown")

df_cleaned = df_cleaned[df_cleaned['finalWorth'] < 20000]
df_cleaned["finalWorth"] = df_cleaned["finalWorth"].astype(float)
df_cleaned["birthYear"] = df_cleaned["birthYear"].fillna(0).astype(int)

# the number of billionares(countries and cities)
def get_top_countries(df, n=10):
    top_countries = df.groupby('country').size().reset_index(name='count')
    return top_countries.nlargest(n, 'count')

def get_top_cities(df, n=10):
    top_cities = df.groupby('city').size().reset_index(name='count')
    return top_cities.nlargest(n, 'count')

# calculating industries distribution
def get_industry_wealth(df):
    return df.groupby("industries")["finalWorth"].sum().reset_index()

#calculating GDP proportion
def calculate_gdp_ratio(df):
    df["gdp_country"] = df["gdp_country"].replace(r"[\$,]", '', regex=True).astype(float)
    df["population_country"] = df["population_country"].astype(float)
    df["gdp_per_capita"] = df["gdp_country"] / df["population_country"]
    df["wealth_factor"] = (df["finalWorth"] * 1e6) / df["gdp_per_capita"]
    return df




# top 3 sources
def get_top_sources(df):
    df_grouped = df.groupby('category', as_index=False)['finalWorth'].sum()
    df_top_sources = df.groupby(['category', 'source'])['finalWorth'].sum().reset_index()
    df_top_sources = df_top_sources.sort_values(['category', 'finalWorth'], ascending=[True, False]) 
    df_top_sources = df_top_sources.groupby('category').head(3)
    df_top_sources = df_top_sources.groupby('category')['source'].apply(lambda x: ', '.join(x)).reset_index()
    df_grouped = df_grouped.merge(df_top_sources, on='category', how='left')

    return df_grouped

# define cities coordinates
city_coordinates = {
    "New York": (40.7128, -74.0060),
    "Beijing": (39.9042, 116.4074),
    "Hong Kong": (22.3193, 114.1694),
    "Shanghai": (31.2304, 121.4737),
    "London": (51.5074, -0.1278),
    "Moscow": (55.7558, 37.6173),
    "Mumbai": (19.0760, 72.8777),
    "Shenzhen": (22.5431, 114.0579),
    "Singapore": (1.3521, 103.8198),
    "Delhi": (28.7041, 77.1025)
}

# add `top_cities'
def add_city_coordinates(df):
    df["latitude_country"] = df["city"].map(lambda x: city_coordinates.get(x, (None, None))[0])
    df["longitude_country"] = df["city"].map(lambda x: city_coordinates.get(x, (None, None))[1])
    return df



df_cleaned = add_city_coordinates(df_cleaned)
df_cleaned= calculate_gdp_ratio(df_cleaned)
top_countries = get_top_countries(df_cleaned)
top_cities = get_top_cities(df_cleaned)
industry_wealth = get_industry_wealth(df_cleaned)
top_sources = get_top_sources(df_cleaned)


__all__ = ['df_cleaned', 'top_countries', 'top_cities', 'industry_wealth', 'top_sources']