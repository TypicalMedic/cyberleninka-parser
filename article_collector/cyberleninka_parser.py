import json
from dict2xml import dict2xml
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as selex
from datetime import datetime
import pandas as pd


DOMAIN_NAME = "https://cyberleninka.ru"
ARTICLES_PER_PAGE = 10

class Cyberleninka_parser:
    def __init__(self, browser: str):
        browser = browser.lower()
        if browser == "chrome":
            self.driver = webdriver.Chrome()
        elif browser == "edge":
            self.driver = webdriver.Edge()
        elif browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "internet explorer":
            self.driver = webdriver.Ie()
        elif browser == "safari":
            self.driver = webdriver.Safari()

    def __del__(self):
        self.driver.quit()

    def Get_article_list(self, request: str, user_limit: int):
        articles = []
        page = 1
        articles.extend(self.Get_articles_on_page(f'{DOMAIN_NAME}/search?q={request}&page={page}'))

        search_header = self.driver.find_element(By.XPATH, "//h1[@class = 'bigheader']")
        results_found = search_header.find_element(By.TAG_NAME, "span").text
        results_found = re.split('\s|\(|\)', results_found)
        limit = int(results_found[2])
        if limit > user_limit:
            limit = user_limit
        if len(articles) > limit:
            articles = articles[0:limit]

        for i in range(ARTICLES_PER_PAGE, limit, ARTICLES_PER_PAGE):
            page += 1
            articles.extend(self.Get_articles_on_page(f'{DOMAIN_NAME}/search?q={request}&page={page}'))
        if len(articles) > limit:
            articles = articles[0:limit]
        return articles
    
    def Get_articles_on_page(self, url: str):
        res = []
        self.driver.get(url)
        try:
            snippets = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@id = 'search-results']//li")))
            for snippet in snippets:
                header = snippet.find_element(By.TAG_NAME, "a")
                s_url = header.get_attribute("href")       
                title = ''.join(header.text)
                res.append({"url" : s_url, "title": title})
        finally:
            return res
        
    def Get_article_info(self, article: {}):
        res = {}
        res['url'] = article["url"]
        res['title'] = article["title"]
        self.driver.get(article["url"]) 
        authors = self.driver.find_elements(By.XPATH, "//ul[@class = 'author-list']//li//span")
        res['authors'] = [a.text for a in authors]
        keywords = self.driver.find_elements(By.XPATH, "//i[@itemprop = 'keywords']//span")
        res['keywords'] = [k.text for k in keywords]
        res['year'] = self.driver.find_element(By.XPATH, "//div[@class = 'label year']//time").text
        res['journal'] = self.driver.find_element(By.XPATH, "//div[@class = 'half']//span//a").text
        res['science_field'] = self.driver.find_element(By.XPATH, "//div[@class = 'half-right']//ul//li//a").text
        try:
            res['abstract'] = self.driver.find_element(By.XPATH, "//div[@class = 'full abstract']//p").text # из текста захавать?
        except selex.NoSuchElementException:
            res['abstract'] = "Не указано"
        res['liked'] = self.driver.find_element(By.XPATH, "//div[@class='likes']//button[@class='btn-reaction btn-reaction--like']").text
        res['disliked'] = self.driver.find_element(By.XPATH, "//div[@class='likes']//button[@class='btn-reaction btn-reaction--dislike']").text
        try:
            res['license'] = self.driver.find_element(By.XPATH, "//div[@class='statitem label-cc']").text
        except selex.NoSuchElementException:
            res['license'] = "Не указано"
        res['viewed'] = self.driver.find_element(By.XPATH, "//div[@class='statitem views']").text
        res['downloaded'] = self.driver.find_element(By.XPATH, "//div[@class='statitem downloads']").text
        self.driver.find_element(By.XPATH, "//button[@title='Цитировать']").click()
        try:
            res['gost_link'] = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//p[@id='quote-text']"))).text
        finally:
            return res

    def Get_articles(self, request: str, user_limit: int):
        articles = [] 
        article_list = self.Get_article_list(request, user_limit)
        for item in article_list:
            articles.append(self.Get_article_info(item))        
        self.driver.quit()
        return articles
    def Export(self, articles, request):
        name = f"{request}_{datetime.now().strftime('%m.%d.%Y, %H.%M.%S')}"
        fname = f"site/app/export/" + name
        with open(fname + ".json", 'w+', encoding="ascii") as file:
            json.dump({"articles": articles}, file, indent=4)
        xml = dict2xml({"article": articles}, indent ="   ", wrap ='root')
        with open(fname + ".xml", 'w+', encoding="utf-8") as file:
            file.write(xml)
        df = pd.DataFrame(articles)
        df.to_excel(fname + ".xlsx")
        df.to_csv(fname + ".csv")
        return name

