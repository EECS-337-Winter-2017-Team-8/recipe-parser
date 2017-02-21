from bs4 import BeautifulSoup
import urllib
r = urllib.urlopen('http://allrecipes.com/recipe/22230/slow-cooker-barbecue-ribs/?clickId=right%20rail%205&internalSource=rr_feed_recipe&referringId=22230&referringContentType=recipe').read()
soup = BeautifulSoup(r)

ingredients = soup.find_all("span", class_="recipe-ingred_txt added")

for ing in ingredients:
	print ing.get_text()