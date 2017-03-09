import nltk, string
from bs4 import BeautifulSoup
import urllib


directions = []
ingredients = []

def run():
	url = ""
	while "allrecipes.com/recipe" not in url:
		url = raw_input("""Please enter a recipe URL from "allrecipes.com":  """)

	get_ingredients_and_directions(url)

def get_ingredients_and_directions(url):
	data = urllib.urlopen(url)
	soup = BeautifulSoup(data)

	ingredients_html = soup.find_all("span", class_="recipe-ingred_txt added")
	directions_html = soup.find_all("span", class_="recipe-directions__list--item")

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


if __name__ == "__main__":
	run()
	
