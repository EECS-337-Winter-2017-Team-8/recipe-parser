# encoding: utf-8
from bs4 import BeautifulSoup
import urllib

# Base URL to start from, only change this one
r = urllib.urlopen('http://allrecipes.com/recipes/80/main-dish/?internalSource=hub%20nav&referringId=256&referringContentType=recipe%20hub&referringPosition=3&linkName=hub%20nav%20exposed&clickId=hub%20nav%203').read()
soup = BeautifulSoup(r)

# Find all of the links on the main url specified above
links = []
for link in soup.find_all("a", href=True):
	print link
	if link.get("href").startswith("/recipe"):
		links.append("http://allrecipes.com" + link.get("href"))
	elif link.get("href").startswith("http://allrecipes.com/recipe"):
		links.append(link.get("href"))

all_ingredients = []

# Find as many recipe links as possible. Not all of them lead to 
# recipes, so it's not 100% robust, it only follows links once, 
# DOES NOT keep scraping until it finds a recipe.

for link in links:
	r = urllib.urlopen(link)
	soup = BeautifulSoup(r)
	ingredients = soup.find_all("span", class_="recipe-ingred_txt added")

	for ing in ingredients:
 		all_ingredients.append(ing.get_text())

 	all_ingredients.append("NEXT RECIPE")

# Get rid of bullshit unicode characters. Copyright character was causing problems
for ing in all_ingredients[:]:
	for letter in ing:
		try:
			letter.encode("ascii")
		except UnicodeEncodeError:
			newing = ing.replace(letter, "")
			all_ingredients[all_ingredients.index(ing)] = newing

# Write Ingredients to file
ing_file = open("ingredients.txt", "w")

for ing in all_ingredients:
	ing_file.write(ing + "\n")

ing_file.close()