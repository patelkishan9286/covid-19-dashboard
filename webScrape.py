# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:38:09 2020

@author: Kishan
"""
import requests
from bs4 import BeautifulSoup

# You can also get data for specific countries by changing the URL
# For example
# for US: https://www.worldometers.info/coronavirus/country/us/
# for India: https://www.worldometers.info/coronavirus/country/india/

url1 = "https://www.mygov.in/corona-data/covid19-statewise-status/"
req1 = requests.get(url1)
bsObj1 = BeautifulSoup(req1.text, "html.parser")
totConf = bsObj1.find_all("div",class_ = "field field-name-field-total-confirmed-indians field-type-number-integer field-label-above")
state= bsObj1.find_all("div",class_="field field-name-field-select-state field-type-list-text field-label-above")
cured= bsObj1.find_all("div",class_="field field-name-field-cured field-type-number-integer field-label-above")
death= bsObj1.find_all("div",class_="field field-name-field-deaths field-type-number-integer field-label-above")

conList= list()
for i in totConf:
    conList.append(i.text.replace("Total Confirmed:","").strip())
    
sList= list()
for i in state:
    sList.append(i.text.replace("State Name:","").strip())    
    
curList= list()
for i in cured:
    curList.append(i.text.replace("Cured/ Discharged/ Migrated:","").strip())

dList= list()
for i in death:
    dList.append(i.text.replace("Death:","").strip())
    

    
    
    
    
    
    
    
    
    