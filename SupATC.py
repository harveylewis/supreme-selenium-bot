# SUPREME AUTO CHECKOUT
#
#
#
#

import requests
from bs4 import BeautifulSoup



#Collect links from 'new' page
pageRequest = requests.get('http://www.supremenewyork.com/shop/all/shirts')
soup = BeautifulSoup(pageRequest.content, "html.parser")
links = soup.select("div.turbolink_scroller a")

allProductInfo = soup.find_all("a", class_="name-link")
# print allProductInfo

hrefLinks = []
for href in allProductInfo:
    hrefLinks.append(href.get('href'))

itemLinks = set(hrefLinks)
print itemLinks

#Follow links and parse info
for url in itemLinks:
	print ('http://www.supremenewyork.com' + url)
	pageRequest2 = requests.get('http://www.supremenewyork.com' + url)
	soup2 = BeautifulSoup(pageRequest2.content, "html.parser")
	itemName = soup2.find_all(itemprop="name")
	print(itemName)
	itemColour = soup2.find_all(class_="style")
	print(itemColour)








#hrefLinks = []
#for link in 
#hrefLinks.append([productInfo])
#print hrefLinks

#refresh until new links are added
#open the new links page
