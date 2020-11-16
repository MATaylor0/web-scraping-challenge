# web-scraping-challenge

A web scraping application which extracts data from the following URLs;

1. https://mars.nasa.gov/news/

2. https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

3. https://space-facts.com/mars/

4. https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

It then saves the results into a MongoDB database and displays the results using a Flask application.

The Flask application has a route which calls the scraping function which enables the data on the page to be updated at any time