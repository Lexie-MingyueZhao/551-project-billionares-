# Milestone 2 Reflection

## Completed Features
- **Data Cleaning and Preprocessing**  
  - Processed GDP and population data by removing `$` and `,`, converting them into numeric types.  
  - Computed `gdp_per_capita` for each country.  
  - Drop the people wtih no countries 

- **Interactive Dashboard**
  - **Tab 1:** Visualizes billionaire distribution on a world map (supports country filtering).  
  - **Tab 2:** Displays the relationship between education level, GDP, and the number of billionaires. 
  - **Tab 3:** Presents the top 10 cities with the most billionaires.  

- **GitHub Repository Management**
  - Organized project structure with `src/`, `data/`, `doc/` directories.  
  - Uploaded to GitHub.

##  Pending Implementation
- **Advanced Data Analysis**  
  - Trend analysis for GDP and wealth factor is not yet implemented.  
  - No predictive models or regression analysis have been added.  

- **Enhanced Interactivity**  
  - **Tab 1:** Enhances usability and interactivity with a more intuitive and visually appealing design.
  - **Tab 2:** Allows users to select different years from the dataset, making data exploration more flexible.

## Future Improvements
- **User Interface Enhancements**  
  - Currently, the UI is basic; plan to integrate `dash-bootstrap-components` for a better layout.  

- **Web Deployment**  
  - The application currently runs locally; the next step is to deploy it on Render.  

- **Expanded Data Analysis**  
  - Further analysis will explore how Gender influences the distribution of billionaires.
  - Future work will examine the role of Self-made or Not status in wealth accumulation.
  - The impact of Wealth Trend on billionaires’ financial growth will be analyzed.


## Current Issues
- **Strange layout in tab1**  
  - The layout of the scatter plot and the world map is strange, need to be adjusted in next time. 

- **Slow Chart Rendering**  
  - Some charts in `Tab 2`, particularly those involving lots of calculations, take longer to load.  
  - Optimization is needed to improve performance.  

## Summary & Next Steps
The primary objective of this milestone was to develop a basic Dash dashboard with data visualizations and interactivity. The current implementation successfully includes data cleaning, an interactive world map for billionaire distribution, and visualizations of the relationships between education level, GDP, and the number of billionaires.

While the core features have been implemented, several improvements are planned for the next phase. These include refining the user interface for a better layout, enhancing interactivity by allowing users to filter and customize calculations, and optimizing chart rendering speed to improve performance. Additionally, deploying the application on Render is a key priority to make the dashboard publicly accessible.

Moving forward, further analysis will be conducted to explore trends in billionaire wealth distribution, as well as potential predictive modeling using machine learning techniques. These enhancements will provide deeper insights and a more comprehensive user experience.