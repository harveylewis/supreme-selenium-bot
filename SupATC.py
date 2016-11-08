# SUPREME AUTO CHECKOUT
#
#
#
#

import requests
from bs4 import BeautifulSoup


targetItemCategoryUrl = ('http://www.supremenewyork.com/shop/all/shirts')



#Collect links from 'new' page
pageRequest = requests.get('http://www.supremenewyork.com/shop/all/shirts')
soup = BeautifulSoup(pageRequest.content, "html.parser")
links = soup.select("div.turbolink_scroller a")

# Gets all divs with class of inner-article then search for a with name-link class that is inside an h1 tag
allProductInfo = soup.select("div.inner-article h1 a.name-link")
# print (allProductInfo)
linksList1 = []
for href in allProductInfo:
    linksList1.append(href.get('href'))



#Follow links and parse info
for url in linksList1:
	# print ('http://www.supremenewyork.com' + url)
	pageRequest2 = requests.get('http://www.supremenewyork.com' + url)
	soup2 = BeautifulSoup(pageRequest2.content, "html.parser")
	itemName = soup2.find_all(itemprop="name")
	itemColour = soup2.find_all(class_="style")
	# print(itemName[0].text)
	# print(itemColour[0].text)
	linkDict = {}
	linkDict[url] = [itemName[0].text, itemColour[0].text]
	print linkDict







## TODO
#refresh until new links are added
#open the new links page
