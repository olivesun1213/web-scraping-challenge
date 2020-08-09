import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import time
def init_browser():
    executable_path = {'executable_path': 'C:\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Create empty dict that can be imported into Mongo
mars_info = {}

#scrape NASA Mars News 
def scrape_News():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    Latest_article = soup.find("div", class_='list_text')
    news_title =Latest_article.find("div", class_="content_title").text
    news_paragraph = Latest_article.find("div", class_ ="article_teaser_body").text
#store result into mars_info
# Dictionary entry from MARS NEWS
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_paragraph

    return mars_info

    browser.quit()

#scrape  Mars Image
def scrape_Image():
    browser = init_browser()
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url=soup.find("figure", class_='lede').a['href']
    main_url="https://www.jpl.nasa.gov"
    featured_image_url=main_url+image_url
    #store in dictionary
    mars_info['featured_image_url'] = featured_image_url
        
    browser.quit()

    return mars_info

#scrape  Mars Facts
def scrape_Facts():
    browser = init_browser()
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]

# Rename columns
    mars_facts=df.drop(["Earth"],axis=1)
    mars_facts.columns=["Description","Value"]
    mars_facts.set_index('Description', inplace=True)
    mars_table=mars_facts.to_html(classes = 'table table-striped')
    mars_info['Fact table'] = mars_table

    browser.quit()
    return mars_info

#scrape Mars Hemisphere
def scrape_Hemisphere():
    browser = init_browser()
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = soup = BeautifulSoup(html, 'html.parser')


    info = soup.find("div", class_ = "result-list" )
    hemispheres = info.find_all("div", class_="item")


    hemisphere_image_urls = []

    for i in hemispheres:
    #find title
        title =i.find("h3").text
    #find partial link
        par_link = i.find("a")["href"]
    #full image link
        main_url = 'https://astrogeology.usgs.gov'
        image_link = main_url + par_link 
    #visit full image link
        browser.visit(image_link)
        html = browser.html
        soup = soup = BeautifulSoup(html, 'html.parser')
    #find image url
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
    #append result to empty list
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

        
    mars_info['hemisphere_image_urls'] = hemisphere_image_urls
        
       
    browser.quit()

    # Return mars_data dictionary 

    return mars_info

