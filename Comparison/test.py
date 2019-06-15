import requests, csv
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains



##############################
### Extracting Source code ###
##############################
URL = 'https://www.faa.gov'

options = Options()
profile = webdriver.FirefoxProfile('/Users/waleed/Library/Application Support/Firefox/Profiles/dmopb59z.default-release')
driver = webdriver.Firefox(profile, options=options, executable_path="/Users/waleed/Desktop/JS-Reseach/Comparison/driver/geckodriver")
driver.get(URL)

soup = bs(driver.page_source.encode("utf-8"),"lxml")

output = open('unedited.txt', mode='w')
# output = csv.writer(restaurant_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

output.write(str(soup))

IDs = []
classes = []

for tag in ["div","p","span","h1","h2","h3","h4","h5","h6","p","button"]:

    tags = soup.findAll (tag)


    for t in tags:
        # storing all div's IDs
        try:
            id = t.get('id')
            # print (id)
            if id != None and (not id in IDs) and (type(id)==type('str') or (type(id)==type(['list']) and len(id)==1)):
                if type(id) == type([]):id = id[0]
                IDs.append([tag,id])
        except:
            pass

        # storing all div's classes
        try:
            cl = t.get('class')
            # print (cl,type(cl))
            if cl != None and (not cl in classes) and (type(cl)==type('str') or (type(cl)==type(['list']) and len(cl)==1)) :
                if type(cl) == type([]):cl = cl[0]
                classes.append([tag,cl])
        except:
            pass

    # print (len(IDs))
    # print (len(classes))

for a in (IDs + classes):
    print (a)

########################
### Selenium Scoring ###
########################
i=0
for id in IDs:
    try:
        elem = driver.find_element_by_id(id[1])
        actions = ActionChains(driver)
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        actions.move_to_element(elem)
        actions.perform()
    except:
        i+=1


print (i,len(IDs))
