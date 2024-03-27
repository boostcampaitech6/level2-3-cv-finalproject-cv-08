from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

'''
YouTube crawling using Selenium

Saves information of approximately 162 videos including name, title, and URL to Youtube_search_df.csv.
'''

# Initialize WebDriver (executable_path not required as it's added to PATH)
browser = webdriver.Chrome()

# URL to access
url = "https://youtube.com/"

# Search keyword
keyword = "Solo Travel"

# Scroll until the specified line
# finish_line = 40000 (about 162 videos)
finish_line = 10000

browser.maximize_window()
browser.get(url)
time.sleep(2)
search = browser.find_element(By.NAME, "search_query")
time.sleep(2)
search.send_keys(keyword)
search.send_keys(Keys.ENTER)

# Switch to search result page for parsing
present_url = browser.current_url
browser.get(present_url)
last_page_height = browser.execute_script("return document.documentElement.scrollHeight")

# Scroll 100 times
scroll_count = 0
while scroll_count < 100:
    # Scroll down
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2.0)       # Waiting for data to load when scrolling down
    new_page_height = browser.execute_script("return document.documentElement.scrollHeight")
    
    # Increase scroll count
    scroll_count += 1

html_source = browser.page_source
soup = BeautifulSoup(html_source, 'html.parser')

# Retrieve all search results up to the finish line
# Extract all content-related sections
elem = soup.find_all("ytd-video-renderer", class_="style-scope ytd-item-section-renderer")

# Retrieve necessary information
df = []
for t in elem[:100]:  # Retrieve only the first 100 video information
    title = t.find("yt-formatted-string", class_="style-scope ytd-video-renderer").get_text()
    name = t.find("a", class_="yt-simple-endpoint style-scope yt-formatted-string").get_text()
    content_url = t.find("a", class_="yt-simple-endpoint style-scope ytd-video-renderer")["href"]
    df.append([name, title , 'https://www.youtube.com/'+content_url])

## Save data
# Create DataFrame
new = pd.DataFrame(columns=['name', 'title' , 'url_link'])

# Insert data
for i in range(len(df)):
    new.loc[i] = df[i]

# Create directory to save data
df_dir = "./data/"
if not os.path.exists(df_dir):
    os.makedirs(df_dir)

# Save data
new.to_csv(os.path.join(df_dir, "Youtube_search_df.csv"), index=True, encoding='utf8')  # Save with index

## Save column information
# Column description table
col_names = ['name', 'title' ,'url_link']
col_exp = ['Channel name', 'Video title', 'URL link']

new_exp = pd.DataFrame({'col_names':col_names,
                        'col_explanation':col_exp})

# Save
new_exp.to_csv(os.path.join(df_dir, "Youtube_col_exp.csv"), index=False, encoding='utf8')

# Close the browser
browser.close()
