from RecipeClass import *
from StepClass import *
from RecipeUtilities import *

def run():
    ''' Final Run Function '''
    url = ""
    while "allrecipes.com/recipe" not in url:
        url = raw_input("""Please enter a recipe URL from "allrecipes.com":  """)
        title, ingredients, directions = get_title_ingredients_and_directions(url)

if __name__ == "__main__":
    run()
