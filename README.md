# Project-A---Visualizing-Air-Pollution-Data

***Names: Nice Teta Hirwa*** <br />
***Instructor: Professor Mike Ryu*** <br />
***Class: CS-150*** <br />


## Thesis Statement
Visually analysing the cost of living wage in NewYork City 

## Context of my data visualization
As a city that is highly known for its expensive way of living in terms of housing, transportation, etc., I was very curious to know how 
its cost of living wage in relation to one's income and expenses. Therefore, in this visualization, I display how income and expenses increase
and decrease in each county across NewYork. 

## Data I will be visualizing
I will visualize the cost of living wage in relation to one's income and expenses in NewYork City. In the dashboard, a user will be able to interact with four tabs namely - About, where I explain what the project is all about.
The second is - Cost of living explorer, in this tab, a user will be able to select the NYC county that you want to see portrayed and its
average income and housing price. The housing price varies with the house's sqr feet, in the dashboard, you will get enough flexibility to 
change the area of the square feet. Not only do I have a bar chart, but I also have a line graph that plots transportation expenses, 
durable goods and one's average income. The third tab is Results - displays the dataset. And the last which is among my favorite one's is 
county predictor. 

## Call to Action
I personally learnt that if I want to live a solid life and have a pretty good living wage, I should invest in houses pay a hundred times more. It was seen in my bar chart when people 
bought houses years back but after 2 years, the hprice of that house skyrocketed in an imaginable way. So as young people, lets invested in houses.
This dashboard also served as a good remainder that where you live is highly determined with how much you earn, and your expenses. 

## Strategies employed from SWD
1.  Articulating my unique point of view of the project
2. Specifically conveying what’s at stake
3. Displaying what is happening, what should be the audiences response, and how is the data being displayed correctly

## Explaining the coding part of the project
Living_Wage_Dashboard.py has three main parts that makes the visual display effective. 
1. Load_data: Merging datasets, I merged all four datasets together and calculate the averages of their income 
2. Create: In creating part, I Create_data table that will go into the results tab, create dropdowns for NYC counties in the cost of living explorer
tab, sqft slider for square feet, create filter cards, and create tabs and app_layout that put all cards into shape.
3. Call back: In my call back function, I have two call backs, one is for predicting results it predicts the county and finds the closest match 
according to the user's income, expenses and durable goods. Another one is for updating the whole dashboard. This one adds updates the 
bar chart and the line graph as a user changes the dropdowns and sliders. 

## Source of the Data
1. FRED: https://fred.stlouisfed.org/series/DTRSRC1A027NBEA, https://fred.stlouisfed.org/series/BOGZ1LM155111005Q
2. Kaggle: https://www.kaggle.com/datasets/nelgiriyewithana/new-york-housing-market/data

## Changes I have implemented per the feedback 

1. For the speed, I changed/rearranged callbacks, and changed my code for the line chart so that it can reduce the time it takes to run. 
2. Told me to space out the years on my historical trend, and I did that! I implemented a 5-year gap between graphs

And I finally called the main() function to run the code.

