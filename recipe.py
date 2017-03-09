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
recipe_ingrs_extracted_toks = map(lambda(x): nltk.word_tokenize(x), recipe_ingrs_extracted)

def getAdjacentIngredient(lower_step_tokens, index, recipe_ingrs_extracted_tokens):
	#where recipe_ingrs_extracted_toks = map(lambda(x): nltk.word_tokenize(x), recipe_ingrs_extracted)
	#& recipe_ingrs_extracted=getRecipeIngredientsAttributes(recipe_ingrs_raw)
	#Basically, recipe_ingrs_extracted_toks is a TOKENIZED LIST OF ALL OF THE 'INGREDIENTS' - no descriptions, measurements, nothing
	susp_ingr  = lower_step_tokens[index]
	for ingr_token in recipe_ingrs_extracted_tokens:
		#The tokens of 1 ingredient 
		if(susp_ingr in ingr_token):
			len_ingr_token = len(ingr_token)

			if(len_ingr_token>1):
				iterator_fwd, iterator_bwd = None, None
				index = ingr_token.index(susp_ingr)
				len_step_tokens = len(lower_step_tokens)

				if(index==0): 
					#if suspected ingredient is found at the start of the token, check if there is a match w the next one
					iterator_fwd = 1
					while( (len_step_tokens > (index+iterator_fwd) ) and ( lower_step_tokens[index+iterator_fwd] in ingr_token) ):
						iterator_fwd+=1
					iterator_fwd-=1

				elif(index == (len_step_tokens-1) ): 
					#if suspected ingredient is found at the end of the token, check if there is a match w the previous one
					iterator_bwd = -1
					while( (len_step_tokens > (index+iterator_bwd) ) and ( lower_step_tokens[index+iterator_bwd] in ingr_token) ):
						iterator_bwd-=1
					iterator_bwd+=1

				else:
					#may be a chance that it is before OR after.
					iterator_fwd, iterator_bwd = 1, -1
					while( (len_step_tokens > (index+iterator_fwd) ) and ( lower_step_tokens[index+iterator_fwd] in ingr_token) ):
						iterator_fwd+=1
					
					while( (len_step_tokens > (index+iterator_bwd) ) and ( lower_step_tokens[index+iterator_bwd] in ingr_token) ):
						iterator_bwd-=1
					
					#Just to undo the offset
					iterator_fwd-=1
					iterator_bwd+=1

			if((iterator_fwd!=None) and (iterator_bwd!=None)):
				return lower_step_tokens[index+iterator_bwd : index+iterator_fwd+1]
			elif(iterator_fwd):
				return lower_step_tokens[index: index+iterator_fwd+1]
			elif(iterator_bwd):
				return lower_step_tokens[index+iterator_bwd : index]
			else:
				return lower_step_tokens[index]
		else:
			continue
	return None

#Get steps:
recipe_steps = getSteps(recipe_dirns_raw)
recipe_lower_steps = map(str.lower, recipe_steps)
lower_steps_toks = map(nltk.word_tokenize, recipe_lower_steps)
lower_step_toks = lower_steps_toks[1]

#Demo:
# for step in recipe_lower_steps:
# 	m,t,i = firstWordAnalysis(step, recipe_ingrs_extracted_toks)
# 	print "step is: ", step
# 	print "method is : ", m
# 	print "tool is : ", t
# 	print "ingr is : ", i, "\n"

# firstWordAnalysis(recipe_lower_steps[1], recipe_ingrs_extracted_toks)
