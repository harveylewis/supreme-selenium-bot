#!/usr/bin/python

"""
Supreme ATC script

"""

import requests
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
from termcolor import colored, cprint
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pause


def GMT():
    return (time.strftime("%H:%M:%S"))


parser = SafeConfigParser()
parser.read('Config.cfg')
targetItemCategoryUrl = ('http://www.supremenewyork.com/shop/all/shirts')
keywords = ['Black', 'Plaid', 'Multi']


#gets all HTML info from targetItemCategoryUrl
def getLinks():
	#Collect links from 'new' page
	pageRequest = requests.get(targetItemCategoryUrl)
	soup = BeautifulSoup(pageRequest.content, "html.parser")
	links = soup.select("div.turbolink_scroller a")
	# Gets all divs with class of inner-article then search for a with name-link class that is inside an h1 tag
	pageOfHtml = soup.select("div.inner-article h1 a.name-link")
	return pageOfHtml

#Extracts the href values (URLS) from the HTML
def extractLinks(list):
	linksList1 = []
	for href in list:
	    linksList1.append(href.get('href'))
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
	return dictionary, list1

#creates a dictionary to search for best matched item
def findBestMatched(listOfItemNames):
	MatchDic={}
	for name in listOfItemNames:
	    matches=0
	    for item in keywords:
	        if item in name:
	            matches=matches+1
	    MatchDic[name]=matches
	return max(MatchDic, key=MatchDic.get)

#Uses webdriver to add to basket and checkout
def driveTheWeb(link):
	driver.get(link)

	sizeDropDown = Select(driver.find_element_by_id('size'))
	sizeDropDown.select_by_visible_text('Large')
	sleep(0.5)

	addToBasketButton = driver.find_element_by_name("commit")
	addToBasketButton.click()
	sleep(0.6)

	checkoutButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/a[2]')
	checkoutButton.click()
	sleep(0.5)

	fullNameEntry = driver.find_element_by_id('order_billing_name')
	fullNameEntry.send_keys('Harvey Lewis')

	emailEntry = driver.find_element_by_id('order_email')
	emailEntry.send_keys('harvey.l@hotmail.co.uk')

	telNumberEntry = driver.find_element_by_id('order_tel')
	telNumberEntry.send_keys('07931248105')

	addressLineOneEntry = driver.find_element_by_id('bo')
	addressLineOneEntry.send_keys('37A West town lane')

	addressLineTwoEntry = driver.find_element_by_id('oba3')
	addressLineTwoEntry.send_keys('Brislington')

	cityEntry = driver.find_element_by_id('order_billing_city')
	cityEntry.send_keys('Bristol')

	postcodeEntry = driver.find_element_by_id('order_billing_zip')
	postcodeEntry.send_keys('BS4 5DD')

	CCtypeDropDown = Select(driver.find_element_by_id('credit_card_type'))
	CCtypeDropDown.select_by_visible_text('Visa')

	CCnumberEntry = driver.find_element_by_id('cnb')
	CCnumberEntry.send_keys('1234 5678 1234 1234')

	CCexpiryMonth = Select(driver.find_element_by_id('credit_card_month'))
	CCexpiryMonth.select_by_visible_text('01')

	CCexpiryYear = Select(driver.find_element_by_id('credit_card_year'))
	CCexpiryYear.select_by_visible_text('2018')

	CCsecurityNumberEntry = driver.find_element_by_id('vval')
	CCsecurityNumberEntry.send_keys('123')

	termsCheckbox = driver.find_element_by_id('order_terms')
	termsCheckbox.click()

	completeOrderButton = driver.find_element_by_xpath('/html/body/div[2]/div[1]/form/div[4]/div/input')
	completeOrderButton.click()

	print GMT() + ' :: You checked out BOI'


def main():

	print (GMT() + ' :: Opening Browser BOI')
	driver = webdriver.Firefox()
	driver.get(targetItemCategoryUrl)

	print GMT() + ' :: Your keywords are : ' + ', '.join(keywords)
	allProductInfo = getLinks()
	print (GMT() +  " :: saved HTML from target page")
	sleep(0.2)

	print GMT() + ' :: Extracted Links from the HTML'
	linksList1 = extractLinks(allProductInfo)
	sleep(0.2)

	print GMT() + ' :: Starting to try for new links'
	while True:
		time.sleep(2) #Waits 2 seconds between requests
		newHtml = getLinks()
		linksList2 = extractLinks(newHtml)
		print GMT() + ' :: Tried for new links'

		if linksList1 != linksList2:
			newLinks = linksList2 - linksList1
			print GMT() + " :: New links found BOI"
			break


	# print (GMT() + ' :: Created a dictionary to lookup your target item')
	itemDict, itemNameList = followPageLinks(linksList1)
	sleep(0.2)

	print (GMT() + ' :: Searching dictionary for best match')
	bestMatch = findBestMatched(itemNameList)
	sleep(0.2)

	print ' '
	print (GMT() + ' :: The best matched item is: ' + bestMatch)
	sleep(0.2)

	bestMatchedLink = itemDict.get(bestMatch)
	print (GMT() + ' :: The link is for the item is: ')
	sleep(0.2)

	targetItemLink = 'https://www.supremenewyork.com' + bestMatchedLink
	print targetItemLink
	sleep(0.2)

	print GMT() + ' :: Loading browser'
	driveTheWeb(targetItemLink)


  ####
# MAIN #
  ####
# pause.until(1479247440)
# main()
