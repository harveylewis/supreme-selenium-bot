"""
Supreme ATC script

"""

import requests
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
from termcolor import colored, cprint
import time
from time import sleep

def GMT():
    return (time.strftime("%H:%M:%S"))


parser = SafeConfigParser()
parser.read('Config.cfg')
targetItemCategoryUrl = ('http://www.supremenewyork.com/shop/all/shirts')
keywords = ['Printed', 'Stripe', 'Navy']


#gets all HTML info from targetItemCategoryUrl
def getLinks():
	#Collect links from 'new' page
	pageRequest = requests.get(targetItemCategoryUrl)
	soup = BeautifulSoup(pageRequest.content, "html.parser")
	links = soup.select("div.turbolink_scroller a")
	# Gets all divs with class of inner-article then search for a with name-link class that is inside an h1 tag
	pageOfHtml = soup.select("div.inner-article h1 a.name-link")
	print (GMT() +  " :: saved HTML from target page")
	return pageOfHtml

#Extracts the href values (URLS) from the HTML
def extractLinks(list):
	linksList1 = []
	for href in list:
	    linksList1.append(href.get('href'))
	print (GMT() + " :: Extracted Links from the HTML")
	linksList1 = [x.encode('ascii') for x in linksList1]
	return linksList1


#Follows href values (links) and parses data, then adds items to dictionary
def followPageLinks(links):
	dictionary = {}
	list1= []
	for url in links:
		pageRequest2 = requests.get('http://www.supremenewyork.com' + url)
		soup2 = BeautifulSoup(pageRequest2.content, "html.parser")
		itemName = soup2.find_all(itemprop="name")
		itemColour = soup2.find_all(class_="style")
		list1.append(itemName[0].text + ' ' + itemColour[0].text)
		nameOfProduct = (itemName[0].text)
		colourOfProduct = (itemColour[0].text)
		dictionary[nameOfProduct + ' ' + colourOfProduct] = url
	list1 = [x.encode('ascii') for x in list1]
	print (GMT() + " :: Created a dictionary to lookup your target item")
	return dictionary, list1


def findBestMatched():
	MatchDic={}
	for name in itemNameList:
	    matches=0
	    for item in keywords:
	        if item in name:
	            matches=matches+1
	    MatchDic[name]=matches
	return max(MatchDic, key=MatchDic.get)

#################
#Main Code
#################

allProductInfo = getLinks()
itemLinks = extractLinks(allProductInfo)
itemDict, itemNameList = followPageLinks(itemLinks)
sleep(0.3)
print (GMT() + ' :: Searching dictionary for best match')
bestMatch = findBestMatched()
sleep(0.3)
print ' '
print (GMT() + ' :: The best matched item is: ' + bestMatch)
sleep(0.3)
bestMatchedLink = itemDict.get(bestMatch)
print (GMT() + ' :: The link is for the item is: ')
sleep(0.3)
print bestMatchedLink
















#jncaiucb
# while True:
#     time.sleep(3) #sleeps 5 minutes between requests
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

Find new links function

"""
