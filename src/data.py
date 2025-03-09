import pandas as pd
import numpy as np

# ignore warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# load the data 
df = pd.read_csv('../data/Billionaires Statistics Dataset.csv', encoding="ISO-8859-1")

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

# data cleaning
df['finalWorth'] = df['finalWorth'].fillna(0)  
df['gdp_country'] = df['gdp_country'].replace(r"[\$,]", '', regex=True).astype(float)
df['gdp_country'] = df['gdp_country'].fillna(df['gdp_country'].median())
df['population_country'] = df['population_country'].replace(r",", '', regex=True).astype(float)
df['population_country'] = df['population_country'].fillna(df['population_country'].median())  
df['gross_tertiary_education_enrollment'] = df['gross_tertiary_education_enrollment'].fillna(df['gross_tertiary_education_enrollment'].median())
df['total_tax_rate_country'] = df['total_tax_rate_country'].fillna(df['total_tax_rate_country'].median())

# ✅ 计算每个国家的亿万富翁数量
df['billionaire_count'] = df.groupby('country')['finalWorth'].transform('count')

# ✅ 计算每个国家的亿万富翁总财富
df['total_wealth'] = df.groupby('country')['finalWorth'].transform('sum')

# ✅ 计算每个国家的亿万富翁密度（富豪数量 / 总人口）
df['billionaire_density'] = df['billionaire_count'] / df['population_country']
df['billionaire_density'] = df['billionaire_density'].fillna(0)
df_cleaned = df[['age', 'finalWorth']].dropna()
df_cleaned = df[df['finalWorth'] < 20000]

# top 10 countries and cities
top_countries = df.groupby('country').size().reset_index(name='count')
top_countries = top_countries.nlargest(10, 'count')

top_cities = df.groupby('city').size().reset_index(name='count')
top_cities = top_cities.nlargest(10, 'count')

# city_coordinates
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

top_cities["latitude_country"] = top_cities["city"].map(lambda x: city_coordinates.get(x, (None, None))[0])
top_cities["longitude_country"] = top_cities["city"].map(lambda x: city_coordinates.get(x, (None, None))[1])