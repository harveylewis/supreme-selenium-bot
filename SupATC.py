"""
Supreme ATC script

"""

import requests
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser


parser = SafeConfigParser()
parser.read('Config.cfg')
targetItemCategoryUrl = parser.get('user', 'targetItemCategoryUrl')


#gets all HTML info from targetItemCategoryUrl
def getLinks():
	#Collect links from 'new' page
	pageRequest = requests.get(targetItemCategoryUrl)
	soup = BeautifulSoup(pageRequest.content, "html.parser")
	links = soup.select("div.turbolink_scroller a")
	# Gets all divs with class of inner-article then search for a with name-link class that is inside an h1 tag
	pageOfHtml = soup.select("div.inner-article h1 a.name-link")
	print ("saved HTML")
	return pageOfHtml

#Extracts the href values (URLS) from the HTML
def extractLinks(list):
	linksList1 = []
	for href in list:
	    linksList1.append(href.get('href'))

	print ("Extracted Links from HTML")
	return linksList1


#Follows href values (links) and parses data, then adds items to dictionary
def followPageLinks(links):
	dictionary = {}
	for url in links:
		# print ('http://www.supremenewyork.com' + url)
		pageRequest2 = requests.get('http://www.supremenewyork.com' + url)
		soup2 = BeautifulSoup(pageRequest2.content, "html.parser")
		itemName = soup2.find_all(itemprop="name")
		itemColour = soup2.find_all(class_="style")
		nameOfProduct = (itemName[0].text)
		colourOfProduct = (itemColour[0].text)
		dictionary[url] = [nameOfProduct, colourOfProduct]
	print ("Created dictionary to lookup your item")
	return dictionary


#Best matched link function




#################
#Main Code
#################

allProductInfo = getLinks()
itemLinks = extractLinks(allProductInfo)
itemDict = followPageLinks(itemLinks)
# print itemDict

# targetProduct = ("u'Printed Stripe Shirt', u'Red'")
# for url, nameOfProduct in itemDict.items():
#     if nameOfProduct == targetProduct:
#         print url


















#jncaiucb
# while True:
#     time.sleep(3) #Waits 5 minutes between requests
# 	pageRequest = requests.get('http://www.supremenewyork.com/shop/all/shirts')
# 	soup = BeautifulSoup(pageRequest.content, "html.parser")
# 	links = soup.select("div.turbolink_scroller a")
# 	allProductInfo = soup.select("div.inner-article h1 a.name-link")
# 	linksList2 = []
# 	for href in allProductInfo:
# 	    linksList2.append(href.get('href'))

#     if set(Links1) != set(Links2):
#         NewLinks = set(Links2) - set(Links1)
#         print("New links since first request:")
#         for item in NewLinks:
#             print item #Or do whatever you do to match keywords to links and break to continue
#         break
# #DoMoreStuff

"""
TODO
Sort out dictionary 
Function for finding best matched link

"""
