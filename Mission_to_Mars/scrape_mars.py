#Script to scrape Mission to Mars
#Dependecies
import webdriver_manager

import requests
import pymongo
import pandas as pd

import os

from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time

def extract_title(item):
    step_1=str(item).split('>')
    step_2=step_1[1]
    step_3=step_2.split('<')[0]
    
    return step_3



#Set up the executable path
def init_browser():
    executable_path={'executable_path':ChromeDriverManager(version="87.0.4280.88", path=os.path.join('Folder_with_executable')).install()}
    browser=Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    marsData={}
    ###################################
    # Nasa Mars New scrape
    ##################################
    marsImage_urls=[]

    news_url='https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)

    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    New_soup=BeautifulSoup(html,'html.parser')
    
    #find title
    result=New_soup.find('div', class_='list_text').find('div', class_='content_title')
    New_title=result.next_element.get_text()
    
    #find article
    result_article=New_soup.find('div', class_='list_text').find('div', class_='article_teaser_body')
    New_article=result_article.get_text()

    #Store the variables
    marsData['New_title']=New_title
    marsData['New_article']=New_article

    ###################################
    #JPL Mars Space Images - Featured Image
    ####################################
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(1)
    html=browser.html
    image_soup=BeautifulSoup(html, "html.parser")
    image=image_soup.find('div', class_='carousel_items')
    #Extract the url in the element <article></article>
    url_image=image.article['style'].split('(')[-1]
    url_image=url_image.split(')')[0]
    url_image=url_image.replace("'","")

    featured_image_url='https://www.jpl.nasa.gov'+url_image
    
    #Store the variables
    marsData['featured_image_url']=featured_image_url
    
    ###################################
    #Mars Facts
    ####################################

    url_facts='https://space-facts.com/mars/'
    table_facts=pd.read_html(url_facts)
    table_facts=pd.DataFrame(data=table_facts[0])
    table_facts.columns=['Descriptions','Value']

    # Add the info to marsData
    facts=table_facts.to_dict('records')
    table_to_marsData=[]

    for item in range(len(facts)):
        auxiliar=list(facts[item].values())
        table_to_marsData.append(auxiliar)
        
    #Store the variables
    marsData['mars_facts']=table_to_marsData

    ###################################
    #Mars Hemispheres
    ####################################
    url_hemispheres='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)
    time.sleep(1)

    html=browser.html
    hemispheres_soup=BeautifulSoup(html, "html.parser")


    hemispheres=hemispheres_soup.find_all('h3')
    titles_hemispheres=[extract_title(item) for item in hemispheres]

    img_url=[]
    for title in titles_hemispheres:
        browser.visit(url_hemispheres)
        browser.click_link_by_partial_text(title)
        
        html=browser.html
        soup=BeautifulSoup(html, "html.parser")
        
        
        img_url.append(soup.find("div", class_="downloads").find("a")["href"])

    hemisphere_image_urls=[]

    for title, img_url in zip(titles_hemispheres, img_url):
        hemisphere_image_urls.append(
                                {'title':title,
                                'url_img':img_url})
    
    #Store the variables
    marsData['hemisphere_image_urls']=hemisphere_image_urls

    #Close navegador
    browser.quit()

    return marsData





