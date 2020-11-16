def scrape():
    # Importing dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import requests
    import time

    # Using the Chrome Web driver and creating a browser object
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visiting the Mars news website to scrape
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Waiting to ensure page has fully loaded
    time.sleep(1)

    # Scraping the page using BeautifulSoup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Searching through the HTML for the title and first paragraph
    results = soup.find_all("ul", class_ = "item_list")

    news_title = results[0].find("div", class_ = "content_title").get_text()
    news_p = results[0].find("div", class_ = "article_teaser_body").get_text()

    # Visiting the NASA space images website to scrape
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Waiting to ensure page has fully loaded
    time.sleep(1)

    # Scraping the page using BeautifulSoup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Searching through the HTML for the image URL
    results = soup.find("article")

    img_url = "https://www.jpl.nasa.gov"

    featured_image_url = img_url + results["style"].split("'")[1]

    # Storing the space facts URL so that Pandas can read the table
    url = "https://space-facts.com/mars/"

    mars_df = pd.read_html(url)[0]
    mars_df.columns = [" ", "Mars"]

    mars_df.to_html("templates/mars_table.html", index = False)

    # Visiting the Astrogeology website to scrape images
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Waiting to ensure page has fully loaded
    time.sleep(1)

    # Scraping the page using BeautifulSoup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Finding the title of each page we want to visit
    results = soup.find_all("div", class_ = "item")

    page_titles = []

    for i in range(0, 4):
        page_titles.append(results[i].find("h3").get_text())


    # Using Splinter to visit each page and collect the image URL
    img_url = []

    for i in range(0, 4):
        try:
            browser.click_link_by_partial_text(page_titles[i])
            
            html = browser.html
            soup = bs(html, 'html.parser')
            
            results = soup.find_all("div", class_ = "downloads")[0]
            img_url.append(results.find("a")["href"])
            
            browser.back()
        except:
            print("Error, page not found")

    # Merging the two previous lists into a list of dictionaries
    hemisphere_image_urls = []

    for i in range(0, 4):
        hemisphere_image_urls.append({"title": page_titles[i], "img_url": img_url[i]})

    # Closing the browser now that scraping is complete
    browser.quit()

    scraped_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return scraped_data