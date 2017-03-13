from RecipeClass import *
from StepClass import *
from UnparsedRecipe import *
from directions import *
from ingredients import *
import pattern
import copy

def run():
    ''' Final Run Function '''
    url = ""
    while "allrecipes.com/recipe" not in url:
        url = raw_input("""Please enter a recipe URL from "allrecipes.com":  """)

    unparsed_recipe = UnparsedRecipe(url)
    recipe = Recipe(unparsed_recipe)
    for step in recipe.Steps:
    	step.ExtractFromTxt()

    recipe.print_recipe()
    print "\n ~~~~~TRANSFORMATIONS~~~~~\n"
    transformation = 0
    while int(transformation) not in range(1, 8):
    	transformation = raw_input("Please enter a number for one of the following transformations:\n1: Vegan\n2: Serving Size\n3: Low Fat\n4: High Fat\n5: Low Carb\n6: High Carb\n7: Vegetarian\n")

    if int(transformation) == 2:
        serving = raw_input("Please enter the number of servings you want:\n")
        transformed_recipe = recipe.transform(int(transformation), serving)
    else:
        transformed_recipe = recipe.transform(int(transformation))

    if int(transformation) in [1, 2, 7]:
        transformed_recipe.print_formatted_recipe()
    else:
        transformed_recipe.print_recipe()

    return recipe, transformed_recipe


if __name__ == "__main__":
	old, new = run()
