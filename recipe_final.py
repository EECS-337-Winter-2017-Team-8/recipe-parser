import os
from RecipeClass import *
from StepClass import *
from UnparsedRecipe import *
from directions import *
from ingredients import *
import pattern
import copy

transforms = ["VEGAN ", "MODIFIED SERVING SIZE ", "LOW FAT ", "HIGH FAT ", "LOW CARB ", "HIGH CARB ", "VEGETARIAN "]

def run():
    ''' Final Run Function - This function prompts the user for a URL,
        then creates a Recipe Object. User then enters desired transformation.
        The function prints formatted ingredients and the list of directions
        for both the original and transformed recipes for the sake of comparison.
        Function also creates 2 Recipe objects, "old" and "new," that you can 
        play with on the python command line to see all of the properties of 
        recipe and step objects.'''


    url = ""
    while "allrecipes.com/recipe" not in url:
        url = raw_input("""Please enter a recipe URL from "allrecipes.com":  """)

    # Create Recipe Object from URL
    unparsed_recipe = UnparsedRecipe(url)
    recipe = Recipe(unparsed_recipe)

    # Initialize individual step objects
    for step in recipe.Steps:
    	step.ExtractFromTxt()

    # Print original recipe
    recipe.print_formatted_recipe()
    print "\n ~~~~~TRANSFORMATIONS~~~~~\n"
    transformation = 0
    while int(transformation) not in range(1, 8):
    	transformation = raw_input("Please enter a number for one of the following transformations:\n1: Vegan\n2: Serving Size\n3: Low Fat\n4: High Fat\n5: Low Carb\n6: High Carb\n7: Vegetarian\n")

    # Serving Size modification requires 1 more input for number of servings
    if int(transformation) == 2:
        serving = raw_input("Please enter the number of servings you want:\n")
        transformed_recipe = recipe.transform(int(transformation), serving)
    else:
        transformed_recipe = recipe.transform(int(transformation))

    # Change the title of the recipe to include the new modification
    transformed_recipe.unparsed_recipe.title = transforms[int(transformation)] + transformed_recipe.unparsed_recipe.title

    # Pretty print
    transformed_recipe.print_formatted_recipe()

    return recipe, transformed_recipe


if __name__ == "__main__":
	old, new = run()
