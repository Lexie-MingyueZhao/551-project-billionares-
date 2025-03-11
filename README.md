# Billionaire Insights Dashboard

## **Objective**

The **Billionaire Insights Dashboard** provides an **interactive and data-driven visualization** of global billionaires. It enables users to explore **where billionaires are located, which industries dominate wealth creation, and demographic insights such as age, gender, and wealth origins**.

By integrating **Plotly Dash**, the dashboard offers **real-time filtering and interactive visualizations**, making it a powerful tool for **economic, social, and business analysis**.

------------------------------------------------------------------------

## **Key Features & Structure**

### **Tab 1: Global Billionaire Distribution (World Map)**

1.  **Visualizing billionaire distribution worldwide**

    **Three different display modes**:

    \- **Billionaire Count** – Number of billionaires in each country (**default view**)

    \- **Total Billionaire Wealth** – Highlights wealth concentration across nations

    \- **Billionaires per Population Ratio** – Shows "billionaire density" by country

2.  **Interactive Feature**: Clicking on a country reveals:

    \-**GDP**

    \-**Total Population**

    \-**Education Level** (e.g., tertiary enrollment)

    \-**Tax Revenue & Tax Rate**

3.  **Visualizations Used**:

    **Choropleth Map** for billionaire distribution

    **Radar Chart** for country-specific economic factors

------------------------------------------------------------------------

### **Tab 2: Industry & City Distribution**

**Understanding where billionaires are concentrated by industry and location**

**Treemap for industry breakdown**

**Clicking an industry reveals the top 5 cities where billionaires in that sector are based**

**Visualizations Used**:

**Treemap** for billionaire industries

**Bar Chart** or **City-Level Heatmap** for urban concentration

------------------------------------------------------------------------

### **Tab 3: Billionaire Demographics & Wealth Sources**

-   **Analyzing billionaire characteristics**

    **Age Distribution** – Billionaire age trends (**histogram + density curve**)

    **Gender Ratio** – Male vs. Female billionaires (**donut chart**)

    **Wealth Source** – Self-made vs. Inherited billionaires (**donut chart**)

-   **Visualizations Used**:

    **Histogram Plots** for age trends

    **Donut Charts** for gender and wealth sources

------------------------------------------------------------------------

## **Data Sources**

This dashboard is powered by a **comprehensive dataset from Kaggle**, which includes:

-   **wealth rankings**

-   **Industry classifications**

-   **Country & city distribution**

-   **Demographic attributes (age, gender, wealth source, etc.)**

-   **Macroeconomic indicators (GDP, population, education, taxation, etc.)**

🔗 **Data Source:** [Kaggle Billionaire Dataset](https://www.kaggle.com/datasets/nelgiriyewithana/billionaires-statistics-dataset)

------------------------------------------------------------------------

## **Running the Dashboard**

To start the dashboard, run the following commands in your terminal:

``` bash
git clone <https://github.com/Lexie-MingyueZhao/551-project-billionares-.git> 
cd 551-project-billionares-/src 
python app.py
```

The dashboard will be accessible at:

```         
http://127.0.0.1:8051/
```

## Usage Scenarios

Here are some practical ways this dashboard can be used:

1\. Economic & Business Research

• Identify which countries are home to the most billionaires

• Analyze which industries generate the highest billionaire count

• Understand how economic policies (taxation, education, etc.) impact wealth accumulation

2\. Government & Policy Analysis

• Compare billionaire distribution with GDP & tax policies

• Study the impact of education levels on billionaire creation

• Evaluate whether self-made billionaires are increasing or declining

3\. Investment & Market Strategy

• Discover which cities are becoming billionaire hubs

• Analyze wealth concentration in specific industries

• Identify growth trends in self-made vs. inherited billionaires

4\. Media & Academic Studies

• Track the rise of billionaire entrepreneurs

• Investigate gender inequality in wealth accumulation

• Examine historical billionaire trends and shifts over time

## Dashboard Output

![Tab1](https://github.com/Lexie-MingyueZhao/551-project-billionares-/tab1.png?raw=true) ![Tab2](https://github.com/Lexie-MingyueZhao/551-project-billionares-/tab2.png?raw=true) ![Tab3](https://github.com/Lexie-MingyueZhao/551-project-billionares-/tab3.png?raw=true)

## Contributors

-   Mingyue Zhao
-   Wenjun Cheng
-   Jieyi Yao

For any questions or collaborations, feel free to reach out!
