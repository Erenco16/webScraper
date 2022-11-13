from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
import re

# reading the excel file using pandas by the column stockCode
def excel_read(fname):
    excel_data = pd.read_excel(fname)
    data = pd.DataFrame(excel_data,columns=['stockCode'])
    stock_code_list=list()
    for code in data.values:
        stock_code_list.append(str(code[0]))
    return stock_code_list

# logging the website and then returns the driver object if login is successful. If not, it returns 0.
def login(credentials):
    login_url = "https://online.hafele.com.tr/login?logout=true"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(login_url)
    driver.find_element(By.ID, "input-text-username").send_keys(credentials["username"])
    driver.find_element(By.ID, "input-text-password").send_keys(credentials["password"])
    driver.find_element(By.CLASS_NAME, "btnGiris").click()
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    if soup.find("div",class_="error") != None:
        return 0
    else:
        return driver

# creates the soup object of a product page.
def product_soup_extractor(driver,code):
    driver.find_element(By.CLASS_NAME,"search").send_keys(code)
    driver.find_element(By.ID,"button-search-submit").click()
    driver.find_element(By.CLASS_NAME,"product-link ").click()
    html = driver.page_source
    return BeautifulSoup(html,'html.parser')

# extracting the price info of a product
def product_price(soup):
    price = str(soup.find('span', class_="price").contents[0])
    price.replace(r"\xa0₺","")
    return price

# extracting the stock info of a product
def stock_finder(soup):
    content_panel = soup.find_all("div", class_="content panel")
    i = 1
    for panel in content_panel:
        div_list = panel.find_all("div")
        for div in div_list:
            legend_list = div.find_all("legend")
            for legend in legend_list:
                if ("Almanya Stok Bilgileri" not in legend.contents):
                    tds = div.find_all("td")
                    stock_list = list()
                    for i in range(len(tds)):
                        if (i % 2 != 0):
                            item = str(tds[i].find("span").contents[0]).strip()
                            item = item.replace(".", "")
                            stock_list.append(int(item))
                    return max(stock_list)

# extracting the product description table
def table_extractor(soup):
    return str(soup.find("table",class_="rtable table table-bordered mergeTable"))

# extracting all the photos of a product
def product_photo_extractor(soup):
    image_gallery = soup.find_all("div", class_="thumbnails")
    url_list = list()
    for image in image_gallery:
        image_url = image.find_all("div", class_="thumbnail-image")
        url = re.findall("background-image: url\('(.+?)'\)", str(image_url))
        url_list.append(url)
    return url_list[0]