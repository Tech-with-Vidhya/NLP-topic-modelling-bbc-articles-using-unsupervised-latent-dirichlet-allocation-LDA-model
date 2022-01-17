import os
import bs4
import pandas as pd
from selenium import webdriver

PATH = os.path.join('/','Users','benmorris','documents','testdir')

def table_to_df(table):
    return pd.DataFrame([[td.text for td in row.find_all('td')] for row in soup.find_all('tr')])

def next_page(soup):
    return "http:" + soup.find('a', attrs={'rel':'next'}).get('href')

res = pd.DataFrame()
url = "http://bank-code.net/country/FRANCE-%28FR%29/"
counter = 0
driver = webdriver.Chrome(executable_path='/Users/vidhyalakshmiparthasarathy/.CMVolumes/Google-Drive-pbvidhya/~~~VP_Data_Science/DS_Real_Time_Projects/NLP_Topic_Modelling_of_BBC_Articles_using_Unsupervised_Latent Dirichlet Allocation_LDA_Model/source_code/chromedriver')
#driver = webdriver.Chrome()
driver.get(url)

while True:
    print(counter)
    page = driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    table = driver.find_element_by_xpath('//*[@id="tableID"]')
    if table is None:
        print("no table 'tableID' found for url {}".format(url))
        print("html content:\n{}\n".format( page.content))
        continue
    res = res.append(table_to_df(table))
    res.to_csv(os.path.join(PATH,"BIC","table.csv"), index=False, sep=',', encoding='iso-8859-1')
    url = next_page(soup)
    counter += 1