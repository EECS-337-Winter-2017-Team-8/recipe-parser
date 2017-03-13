from RecipeClass import *
from StepClass import *
import nltk, string
from bs4 import BeautifulSoup
import urllib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Final Run Function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run():
	url = ""
	while "allrecipes.com/recipe" not in url:
		url = raw_input("""Please enter a recipe URL from "allrecipes.com":  """)

	title, ingredients, directions = get_title_ingredients_and_directions(url)
	


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Behind the Scenes to Parse HTML ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_title_ingredients_and_directions(url):
	ingredients = []
	directions = []

	data = urllib.urlopen(url)
	soup = BeautifulSoup(data)

	title_html = soup.find_all("h1", class_="recipe-summary__h1")
	ingredients_html = soup.find_all("span", class_="recipe-ingred_txt added")
	directions_html = soup.find_all("span", class_="recipe-directions__list--item")

	title = title_html[0].get_text()

	for ing in ingredients_html:
		ingredients.append(ing.get_text())

	for direction in directions_html:
		tokens = nltk.sent_tokenize(str(direction.get_text()))
		for token in tokens:
			directions.append(token)

	count = 1
	for idx, item in enumerate(directions):
		directions[idx] = (str(count) + ". ") + item
		count += 1

	return title, ingredients, directions

if __name__ == "__main__":
	run()




#execfile('/Users/Omar/Desktop/Code/recipe-parser/recipe.py')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set up & Utility Functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# execfile('/Users/Omar/Desktop/Code/recipe-parser/ingredients.py')
# execfile('/Users/Omar/Desktop/Code/recipe-parser/directions.py')