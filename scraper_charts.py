#import packages
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException 

#function for requesting number of albums
def get_albums(num_albums, verbose):
    
    '''Gathers albums as a dataframe, scraped from rateyourmusic.com'''   
    
    #initialize chrome driver
    driver = webdriver.Chrome(executable_path="C:/Users/malex/Desktop/rateyourmusic/chromedriver.exe")
    driver.set_window_size(1120, 1000)

    #url to begin scraping from
    url = 'https://rateyourmusic.com/charts/top/album/all-time/exc:live,archival/#results'
    driver.get(url)
    
    #wait for browser to open
    time.sleep(10)
    
    #initialize albums array
    albums = []
    
    #for loop to go through ranked albums 
    for position in range(1,num_albums+1):
            
        #xpath to specify album ranking
        xpath = './/div[@id="pos'
        xpath += str(position)
        xpath += '"]'
        
        #initialize variable to break while loop
        collected_successfully = False
    
        #runs until collected_successfully = True
        while not collected_successfully:
            
            #try to find items for scraping
            try:
                ranking = driver.find_element_by_xpath('{}//div[@class="topcharts_position"]'.format(xpath)).text
                album_name = driver.find_element_by_xpath('{}//div[@class="topcharts_item_title"]'.format(xpath)).text
                artist_name = driver.find_element_by_xpath('{}//div[@class="topcharts_item_artist_newmusicpage topcharts_item_artist"]'.format(xpath)).text
                release_date = driver.find_element_by_xpath('{}//div[@class="topcharts_item_releasedate"]'.format(xpath)).text
                genres = driver.find_element_by_xpath('{}//div[@class="topcharts_item_genres_container"]'.format(xpath)).text
                descriptors = driver.find_element_by_xpath('{}//div[@class="topcharts_item_descriptors_container"]'.format(xpath)).text
                rating = driver.find_element_by_xpath('{}//span[@class="topcharts_stat topcharts_avg_rating_stat"]'.format(xpath)).text
                num_ratings = driver.find_element_by_xpath('{}//span[@class="topcharts_stat topcharts_ratings_stat"]'.format(xpath)).text
                
                #try to find number of reviews, but if no reviews exist then set num_reviews = 0
                try:
                    num_reviews = driver.find_element_by_xpath('{}//span[@class="topcharts_stat topcharts_reviews_stat"]'.format(xpath)).text
                except NoSuchElementException:
                    num_reviews = 0
                
                #set true to break while loop
                collected_successfully = True
            
            #if page hasn't loaded yet wait 5 seconds
            except:
                time.sleep(5)

        #append scraped information to albums array
        albums.append({"Ranking" : ranking,
                       "Album" : album_name,
                       "Artist Name": artist_name,
                       "Release Date" : release_date,
                       "Genres" : genres,
                       "Descriptors" : descriptors,
                       "Average Rating" : rating,
                       "Number of Ratings" : num_ratings,
                       "Number of Reviews" : num_reviews})
        
        #if at album ranking that is divisible by 40 (since there are 40 albums per page) then click on "next page" button
        if position%40 == 0:
            
            try:
                driver.find_element_by_xpath('.//a[@class="ui_pagination_btn ui_pagination_next"]').click()
            
                time.sleep(5)
            
            #if on last page then break from if condition
            except NoSuchElementException:
                
                break
        
    #return requested albums as a dataframe
    return pd.DataFrame(albums)
