from RecipeClass import *
from StepClass import *
import nltk, string
from bs4 import BeautifulSoup

import urllib

def get_title_ingredients_and_directions(url):
    print urllib
    ingredients = []
    directions = []

    data = urllib.urlopen(url)
    soup = BeautifulSoup(data, "lxml")

    title_html = soup.find_all(itemprop="name")
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
