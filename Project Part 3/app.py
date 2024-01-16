import pandas as pd

def find_top_confirmed(n = 15):
  corona_df=pd.read_csv("covid-19-dataset-3.csv")
  by_country = corona_df.groupby('Province_State').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
  cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
  return cdf


cdf=find_top_confirmed()
pairs=[(province_state,confirmed) for province_state,confirmed in zip(cdf.index,cdf['Confirmed'])]


import folium
import pandas as pd
corona_df = pd.read_csv("covid-19-dataset-3.csv")
corona_df=corona_df[['Lat','Long_','Confirmed']]
corona_df=corona_df.dropna()

m=folium.Map(location=[34.223334,-82.461707],
            tiles='Stamen toner',
            zoom_start=8)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2]),
                 color="red",
                 popup='confirmed cases:{}'.format(x[2])).add_to(m)
corona_df.apply(lambda x:circle_maker(x),axis=1)

html_map=m._repr_html_()

import requests
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus/"
req = requests.get(url)
bsObj = BeautifulSoup(req.text, "html.parser")
data = bsObj.find_all("div",class_ = "maincounter-number")
data1=bsObj.find_all("span",class_="number-table")

lst = []

datalst = ['Confirmed Cases', 'Deaths','Recovered','Critical','Death Rate','Recovery Rate','Mild Condition','Active Cases']

for i in data:
    lst.append(i.text.strip())

lst.append(data1[1].text.strip())
#lst.append(data[2].text.strip())
lst.append(float(data[1].text.strip().replace(",",""))/float(data[0].text.strip().replace(",",""))*100)
lst.append(float(data[2].text.strip().replace(",",""))/float(data[0].text.strip().replace(",",""))*100)
lst.append(data1[0].text.strip())
lst.append(int(data1[0].text.strip().replace(",",""))+int(data1[1].text.strip().replace(",","")))

corona_dict = {}

for i in range(len(lst)):
    corona_dict[datalst[i]]=lst[i]

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



from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs,data=corona_dict,conf=conList,state=sList,cur=curList,death=dList)

if __name__=="__main__":
    app.run(debug=True)