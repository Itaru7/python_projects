Restaurants in the city of New York are inspected annually and a grade is assigned to them according to various factors. Inspection data for a period of 4 years is provided in a .txt format. The "description.csv" file contains the description of each of the columns.

# Questions
1) Return a list of tuples of the form:

        (zipcode, mean score, number of restaurants)
    for each of the 92 zipcodes in NYC with over 100 restaurants. If there are multiple inspection reports for one restaurant, use the latest inspection date only. Sort the list in descending order by mean score.

2) Sing up in ["CartoDB"](http://cartodb.com/) to plot a map of average score by zipcode.

    Here (https://carto.com/docs/carto-editor/managing-your-data/) is how you can upload your data on their website.

    After you produced the plot, use the "share" button to return a link of your plot in the format of "https://x.cartodb.com/ (Links to an external site.)Links to an external site....".

    Note: Check your link before upload your answer.

## Hints
* Read the .txt file into a pandas data frame.
* You may need data cleaning. There are some data missing.
* Check the range of valid zipcodes for NYC.
* Submission (Links to an external site.)Links to an external site.
* Submit a .zip file including your .py file, a .txt file contains a list of 92 sorted tuples and "CartoDB" link.

#### Checkpoints:

Total unique restaurants: 25,232

Total restaurants in valid zipcodes: 20,349

# Plotted Map After Data Cleaning
    https://itaru7.carto.com/builder/ec55eb51-aa24-4cfc-9e6b-8a1c171ecb47/embed