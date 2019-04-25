# Dependencies
import pymongo
from bs4 import BeautifulSoup as bs
import requests
import logging
from pprint import pformat
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": 'chromedriver'}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser = init_browser()
    mars_data = {}

# Execute all of the scraping code from `mission_to_mars.ipynb` and return one Python dictionary containing all of the scraped data

    # 1. NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Browser visit
    browser.visit(url)
    print(f'visiting {url}')

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')

    # Collect the latest News Title and Paragraph Text
    # Assign the text to variables
    news_title = soup.find("div", class_='content_title').text
    mars_data['news_title'] = news_title

    # print(news_title)

#     news_p = soup.find("div", class_='rollover_description_inner').text
    news_p = soup.find("div", class_='article_teaser_body').text
    print(news_p)

    # 2. JPL Space Images - Featured Image
    # URL of page to be scraped
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Browser visit
    browser.visit(url2)
    print(f'visiting: {url2}')

    # Click lead image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    # Click again for full image
    browser.click_link_by_partial_text('more info')

    # Design an XPATH selector to grab the featured image
    xpath = '//figure//a'

    # Use splinter to click the featured image and bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    # Retrieve final image URL
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find("img")["src"]
    featured_image_url

    # 3. Mars Weather
    # URL of page to be scraped
    url3 = 'https://twitter.com/marswxreport?lang=en'

    # Browser visit
    browser.visit(url3)
    print(f'visiting {url3}')

    html = browser.html
    # Create soup object
    soups = bs(html, 'html.parser')

    # Scrape first tweet
    mars_weather = soups.find("li", class_="js-stream-item").find("p", class_="tweet-text").text
    print(mars_weather)

    # 4. Mars Facts
    # URL to scrape
    url4='http://space-facts.com/mars/'

    # Use read_html to read the data
    tables = pd.read_html(url4)

    # Slice off DataFrame using normal indexing
    df = tables[0]
    df.columns = ['0', '1']
    
    # Rename columns so that they make sense
    df.columns = ['Metric', 'Value']

    # Set columns to index
    table_html = df.set_index(['Metric', 'Value'], inplace=True)

    #UNNECESSARY CODE?
    table_html = df
    
    # Generate HTML tables from Pandas using to_html method
    table_html = df.to_html(classes="table table-striped")

    # Clean up table
    table_html = table_html.replace('\n', '')

    # Save to a file
    table_html = df.to_html('table.html')

    # 5. Mars Hemispheres
    # URL of page to be scraped
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Browser visit
    browser.visit(url5)
    print(f'visiting {url5}')

    # Create a Beautiful Soup object
    html = browser.html
    soup = bs(html, 'html.parser')

    # Child website links for each hemisphere
    base_url = "https://astrogeology.usgs.gov"
    links = [base_url + item.find(class_="description").a["href"] for item in soup.find_all("div", class_="item")]

    # Extract hemisphere title and web URL for each image
    hemisphere_image_urls = []

    for url in links:
        
        # from url to soup
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # Extract data
        title = soup.find("div", class_="content").find("h2", class_="title").text.replace(" Enhanced", "")
        img_url = base_url + soup.find("img", class_="wide-image")["src"]
        
        # Store in list
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    # Store in dictionary
    mars = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "table_html": table_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    print('getting mars data...')
    print(pformat(mars))


    # Return results
    return mars

    # Quit browser
    # browser.quit()



