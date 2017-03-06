#execfile('/Users/Omar/Desktop/Code/recipe-parser/recipe.py')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set up & Utility Functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
execfile('/Users/Omar/Desktop/Code/recipe-parser/ingredients.py')
execfile('/Users/Omar/Desktop/Code/recipe-parser/directions.py')

def matchDirnAndIngredientInput(directions, ingredients):
	#This will match each recipe in the directions & ingredients file
	#ASSUMING they have already been SegmentedByNextRecipeTag AND they have same # of recipes
	pairings = []
	while("__SPLIT__\n" in directions):
		dirn_end_index = directions.index("__SPLIT__\n")
		ingr_end_index = ingredients.index("__SPLIT__\n")
		recipe_dirns = directions[:dirn_end_index]
		recipe_ingrs = ingredients[:ingr_end_index]
		
		pairings.append([recipe_ingrs, recipe_dirns])
		directions = directions[dirn_end_index+1:]
	return pairings

def getRecipeIngredientsAttributes(recipe_ingrs_raw):
	recipe_ingrs_formatted = []
	for ingr in recipe_ingrs_raw:
		ingr_formatted = parse_ingredient(ingr)
		recipe_ingrs_formatted.append(ingr_formatted)
	recipe_ingrs_extracted = [recipe["Ingredient"] for recipe in recipe_ingrs_formatted]
	return recipe_ingrs_extracted
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ User Interface: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

directions = segmentByNextRecipeTag(list(open("directions.txt", "r")))
ingredients = segmentByNextRecipeTag(list(open("ingredients.txt", "r")))
recipe_pairings = matchDirnAndIngredientInput(directions, ingredients)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WorkSpace/Demo-code: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#This would eventually be parameterizable but just for now:

recipe_raw = recipe_pairings[0]
recipe_ingrs_raw, recipe_dirns_raw = recipe_raw

#Get ingredients:
recipe_ingrs_formatted = [parse_ingredient(ingr) for ingr in recipe_ingrs_raw]
recipe_ingrs_extracted = getRecipeIngredientsAttributes(recipe_ingrs_raw)

#Get steps:
recipe_steps = getSteps(recipe_dirns_raw)
recipe_lower_steps = map(str.lower, recipe_steps)

for i in recipe_lower_steps:
	c = firstWordAnalysis(i)
	print c


#To get time, use "for" & "until"
#I think "for" is almost always followed by measurement of time:
	#for .... MINUTES or MINUTES
	#for .... HOURS 
	#for .... DAYS 
	#but there is also.  :   Preheat grill for medium heat.