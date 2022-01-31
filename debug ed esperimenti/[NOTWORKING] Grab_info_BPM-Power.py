#they have anti scraping mechanisms :(

from urllib.request import urlopen
import requests
import json
import urllib
#do not modify this
url_base = "https://www.bpm-power.com/it/ricerca?orderby=1&sortby=0&d=Schede+Video&k="
#this is what you modify
search = "nvidia+geforce+rtx+3060"

#connect to site and get data
response = requests.get(url = url_base+search) 
#html file in string format
raw = response.json() 


data = json.load(urlopen(url_base+search),'jsonp')
print(data)


f = open("a.txt", "w")
#f.write(raw)
f.close()

#print(raw)