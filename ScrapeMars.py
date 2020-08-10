import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import time
def init_browser():
    executable_path = {'executable_path': 'C:\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



def scrape():
    browser = init_browser()
    #scrape news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    Latest_article = soup.find("div", class_='list_text')
    news_title =Latest_article.find("div", class_="content_title").text
    news_paragraph = Latest_article.find("div", class_ ="article_teaser_body").text


#scrape  Mars Image

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
    
#scrape  Mars Facts

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]

# Rename columns
    mars_facts=df.drop(["Earth"],axis=1)
    mars_facts.columns=["Description","Value"]
    mars_facts.set_index('Description', inplace=True)
    mars_table=mars_facts.to_html(classes = 'table table-striped')
   
#scrape Mars Hemisphere

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

        
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()


