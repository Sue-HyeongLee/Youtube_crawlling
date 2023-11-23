import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pyautogui # 이건 자동으로 엔터를 쳐줄 것임.
from selenium.common.exceptions import NoSuchElementException  # 에러 발생할 때 대비시키기 위해.
from selenium.webdriver.common.keys import Keys
import sys
from pytube import YouTube
import datetime

# sys.stdout의 인코딩을 UTF-8로 변경
sys.stdout.reconfigure(encoding='utf-8')

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options = chrome_options)

link_list = ['https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl', 'https://www.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D', 'https://www.youtube.com/feed/trending?bp=4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D','https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D']
# 최신, 음악, 게임, 영화 순으로 나열되어있다.


for link in link_list:
  driver.get(link)
  driver.implicitly_wait(3)
  time.sleep(1.5)

  driver.execute_script("window.scrollTo(0, 800)")
  time.sleep(3)

  last_height = driver.execute_script("return document.documentElement.scrollHeight")

  while True:
      driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
      time.sleep(1.5)

      new_height = driver.execute_script("return document.documentElement.scrollHeight")
      if new_height == last_height:
          break
      last_height = new_height
  time.sleep(1.5)
  title_list = []
  time_list =[]
  visit_list =[]
  href_list = []
  author_list = []
  title= driver.find_elements(By.CSS_SELECTOR, "#video-title > yt-formatted-string") # 제목
  visit = driver.find_elements(By.CSS_SELECTOR, "#metadata-line > span:nth-child(3)") # 조회수
  href = driver.find_elements(By.CSS_SELECTOR, "#thumbnail") # url
  author = driver.find_elements(By.CSS_SELECTOR, "#text > a") # 작성자
  
  for element in title:
    title_list.append(element.text)
  print(len(title_list))
  visit_num = 0
  for element in visit:
    visit_num +=1
    if 3 <= visit_num <= 8: continue
    visit_list.append(element.text[4:])
  print(len(visit_list))
  
  for element in href:
    href_value = element.get_attribute('href')
    if href_value == None or 'shorts' in href_value:
      continue 
    href_list.append(href_value)
  href_list = href_list[1:]
  print(len(href_list))
  
  
  for element in author:
    if element.text == '':
      continue
    author_list.append(element.text)
  author_list = author_list[4:]
  print(len(author_list))
  
  update_date_list=[]
  length_list =[]

  for url in href_list:
    tube = YouTube(url)
    update_dates = str(tube.publish_date)
    update_date = update_dates.split(" ")
    update_date= update_date[0]
    length_second = int(tube.length)
    length = str(datetime.timedelta(seconds=length_second))
    update_date_list.append(update_date)
    length_list.append(length)


  file_name = "newest"
  df = pd.DataFrame({"title": title_list , "url": href_list, "visit": visit_list, "author" : author_list, "update_date": update_date_list, "length": length_list})
  df.to_csv("./output/"+file_name+".csv", encoding= 'utf-8-sig') # utf-8로 할 경우, 파일이 깨짐.
  

  
  

  