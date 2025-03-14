# Milestone 3 - User Feedback Report

## 1. Questions Asked & Aspects Evaluated

To improve our dashboard, we sought feedback from our peers. The key aspects we assessed included:

*1. Ease of Navigation*

*2. Interactivity & Usability*

*3. Data Visualization & Clarity*

*4. Performance & Layout*

*5. Additional Features & Accessibility*

---

## 2. List of Received Feedback & Changes Implemented

### Positive Feedback
- **Diverse Data Representations**: The mix of charts, maps, and tables was well received for its ability to present different aspects of the data.
- **Logical Structure**: Users appreciated the structured flow from broad overviews (world map, trends) to specific details (industry, top cities, education, etc.).
- **Interactivity**: The clickable map, filtering options, and other interactive features were engaging.
- **Clear Labels & Color Coding**: Most users found the visualizations easy to read, with effective color choices for data representation.

### Constructive Feedback & Implemented Fixes

| Feedback | Change Implemented |
|----------|--------------------|
| **Dataset path issue**: The initial dataset path caused errors. |✔️ Fixed pathing issue, ensuring correct dataset directory. |
| **Map shrinking when selecting "gdp_country" and "state"** | ✔️ Investigated and fixed layout resizing bug. |
| **Tab 1 layout could be improved** |✔️  Rearranged elements: Increased map size, centered the bottom chart. |
| **Rank variable appears as "ï>>?rank" (encoding issue)** | ✔️ Fixed encoding issue, ensuring proper display. |
| **Too much scrolling needed in Tab 2** | ✔️ Resized and rearranged elements for better readability. |
| **Unnecessary variable "parent" in Tab 4** | ✔️ Removed unnecessary variables to improve clarity. |
| **Top 10 Counties (Billionaire Wealth as % of GDP) chart color contrast issue** | ✔️ Adjusted colors to improve visibility, removing unnecessary color variations. |
| **Add tooltips for context** | ✔️ Implemented hover tooltips to give users additional insights on charts. |
| **Lack of short explanations for each tab** | ✔️ Added a brief description for each tab to guide users. |

---

## 3. Plan for Further Refinements

Although we have addressed most of the major feedback points, we plan to continue refining the dashboard in the following ways:

### 1. Enhance Accessibility
- Ensure all text is readable on different screen sizes.
- Conduct further tests for contrast adjustments.

### 2. Optimize Performance
- Review large datasets to improve loading times.
- Test on different devices to check responsiveness.

### 3. Fine-Tune Data Interactivity
- Expand tooltips to provide more granular insights.
- Consider adding additional filtering options for a better exploratory experience.

---

## Conclusion

Through feedback collection and iteration, we have improved the usability, clarity, and performance of our dashboard. The applied changes—such as fixing layout issues, enhancing tooltips, and refining visualizations—have created a more engaging user experience.

Moving forward, we will focus on performance optimizations and further refining accessibility features to ensure the dashboard remains an effective tool for data exploration.

---
## 4. Questions We Asked
### From Jieyi
* Can not understand what is Canine on the top right conner, and after clicking nothing happened.

* The scale of department plot is strange, as well as the other plot. The only normal plot is mapping.

* If ‘Select All’ selects everything, I suggest adding an option to deselect everything.
### From Mingyue
The dashboard is well-designed with a clean layout and strong data visualization. The Global section effectively presents affordability ratios and food price trends, making it easy to compare different countries. The interactivity is a great feature, allowing users to filter by country, commodity, and year. The comparison functionality is useful for analyzing trends over time.

Here are some suggestions:

* For the global section, it would be helpful to clarify the difference between All Commodities and Essential Commodities. When selecting different commodity types, the trend lines change, but it’s unclear why the patterns differ. Providing a brief explanation or a list of essential commodities could enhance user understanding.

* For the country section, I'll suggest add a legend to explain what the colors represent (e.g., higher vs. lower prices) would make the insights clearer.
### From Wenjun
This dashboard is well-structured and visually appealing. The layout is clear, and the interactive features make it easy to explore the data. The variety of charts helps users understand different aspects of tech salaries. To further enhance usability, consider improving these two areas:

1. The salary distribution map could be refined by adjusting the color scale or adding a zoom function. Currently, some points have similar colors and overlap, making them hard to read.

2. In the Education Salary Analysis tab, the company selector only allows users to select one company at a time. Adding a multi-company selection feature would enable users to compare salaries across different companies, making the dashboard more insightful for analysis.