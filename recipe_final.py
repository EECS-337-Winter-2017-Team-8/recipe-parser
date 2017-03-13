from RecipeClass import *
from StepClass import *
from UnparsedRecipe import *

def run():
    ''' Final Run Function '''
    url = ""
    while "allrecipes.com/recipe" not in url:
        url = raw_input("""Please enter a recipe URL from "allrecipes.com":  """)
        unparsed_recipe = UnparsedRecipe(url)
        print unparsed_recipe.title

if __name__ == "__main__":
    run()
