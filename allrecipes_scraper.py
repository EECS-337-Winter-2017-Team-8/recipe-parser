# encoding: utf-8
from bs4 import BeautifulSoup
import urllib

cuisines = ["http://allrecipes.com/recipes/739/healthy-recipes/diabetic",
			"http://allrecipes.com/recipes/741/healthy-recipes/gluten-free",
			"http://allrecipes.com/recipes/84/healthy-recipes",
			"http://allrecipes.com/recipes/1232/healthy-recipes/low-calorie",
			"http://allrecipes.com/recipes/1231/healthy-recipes/low-fat"]

for c in cuisines:

	# Base URL to start from, only change this one
	r = urllib.urlopen('http://allrecipes.com/recipes/80/main-dish/?internalSource=hub%20nav&referringId=256&referringContentType=recipe%20hub&referringPosition=3&linkName=hub%20nav%20exposed&clickId=hub%20nav%203').read()
	soup = BeautifulSoup(r)

	# Find all of the links on the main url specified above
	links = []
	for link in soup.find_all("a", href=True):
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
		ingredients = soup.find_all("span", class_="recipe-directions__list--item")

		count = 1
		for ing in ingredients:
	 		all_ingredients.append(str(count) + ". " + ing.get_text())
	 		count += 1

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
	word = ""
	idx = -1
	while c[idx] != "/":
		word += c[idx]
		idx -= 1
	word = word[::-1]

	print word

	ing_file = open("allDirections.txt", "a")
	ing_file2 = open("dietHealthDirections.txt", "a")
	ing_file3 = open(word + "Directions.txt", "w")

	for ing in all_ingredients:
		ing_file.write(ing + "\n")
		ing_file2.write(ing + "\n")
		ing_file3.write(ing + "\n")

	ing_file.close()
	ing_file2.close()
	ing_file3.close()