from RecipeClass import *
from StepClass import *
from UnparsedRecipe import *
from directions import *
from ingredients import *

def run():
    ''' Final Run Function '''
    url = ""
    while "allrecipes.com/recipe" not in url:
        url = raw_input("""Please enter a recipe URL from "allrecipes.com":  """)

    unparsed_recipe = UnparsedRecipe(url)
    recipe = Recipe(unparsed_recipe)

    recipe.print_recipe()
    print "\n ~~~~~TRANSFORMATIONS~~~~~\n"
    transformation = 0
    while int(transformation) not in range(1, 7):
    	transformation = raw_input("Please enter a number for one of the following transformations:\n1: Vegan\n2: Serving Size\n3: Low Fat\n4: High Fat\n5: Low Carb\n6: High Carb\n")

    recipe.transform(int(transformation))



if __name__ == "__main__":
    run()
