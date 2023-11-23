import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  # 에러 발생할 때 대비시키기 위해.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


# CSV 파일 읽기
df = pd.read_csv('./output/newest.csv')

# 'url' 열의 값만 추출하여 리스트에 담기
url_list = df['url'].tolist()

# 'title' 열의 값만 추출하여 리스트에 담기
title_list = df['title'].tolist()
new_title_list = []
length = len(url_list)
for i in range(20, 30):
    url = url_list[i]
    try: 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Headless 모드 활성화
        driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options = chrome_options)
        driver.get(url)
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
            # break
        
        try:
            driver.fine_element('#dismiss-button > yt-button-shape > button').click() # 유튜브 1달 무료 팝업닫기

        except:
            pass

        time.sleep(1.5)
        buttons = driver.find_elements(By.CSS_SELECTOR, "#more-replies > yt-button-shape > button")
        
        


        time.sleep(1.5)

        for button in buttons:
            time.sleep(1.5)
            button.send_keys(Keys.ENTER)

        time.sleep(20)




        comment_elements = driver.find_elements(By.CSS_SELECTOR, "#content-text")

        applied_time_list = []
        applied_like_list = []
        applied_comment_list = []
        new_title_list = []  # 추가: 누락된 변수

        length = len(comment_elements)
        times = driver.find_elements(By.CSS_SELECTOR, "#header-author > yt-formatted-string > a")
        likes = driver.find_elements(By.CSS_SELECTOR, "#vote-count-middle")
        # for j in range(length):
        #     new_title_list.append(title_list[i])
            

        #     try:
        #         temp_like_element = comment_elements[j].find_element(By.CSS_SELECTOR, "#vote-count-middle")
        #         temp_like = temp_like_element.text
        #     except NoSuchElementException:
        #         temp_like = "0"  # Set a default value if the element is not found
            
        #     applied_like_list.append(temp_like)  # 수정: 좋아요 수 업데이트
        #     if j == 4: 
        #         break
        # j = 0
        for like in likes:
            # j+=1
            like = like.text
            if like == '':
                like = 0
            applied_like_list.append(like)
            # if j == 5:  
            #     break  
        for comment in comment_elements:
            new_title_list.append(title_list[i])
            temp_comment = comment.text
            temp_comment = temp_comment.replace('\n', '')
            temp_comment = temp_comment.replace('\t', '')
            temp_comment = temp_comment.replace('    ', '')
                
            applied_comment_list.append(temp_comment)  # 댓글 내용
            # if comment == comment_elements[4]:  
            #     break  
        for element in times:
            temp_time = element.text
            if "(수정됨)" in temp_time:
                temp_time = temp_time[:-5]
            applied_time_list.append(temp_time)
            # if element == times[4]:
            #     break

        print(len(applied_comment_list))
        print(len(applied_like_list))
        print(len(applied_time_list))
        print(len(new_title_list))
        
        df = pd.DataFrame({"comment": applied_comment_list , "like": applied_like_list, "time" : applied_time_list, "title_list": new_title_list })
        df.to_csv("./output/"+str(i)+".csv", encoding= 'utf-8-sig') # utf-8로 할 경우, 파일이 깨짐.
    except Exception as e:
        print(f"An error occurred for URL {url}: {str(e)}")
        # 예외가 발생했더라도 계속 진행하도록 다음 반복으로 이동
        continue
    



