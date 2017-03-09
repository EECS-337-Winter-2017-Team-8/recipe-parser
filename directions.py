#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set-up: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import nltk, string, os, re
# os.chdir("documents/eecs/eecs337/recipe-parser")
#execfile('/Users/Omar/Desktop/Code/recipe-parser/directions.py')

#for list of all possible NLTK P.O.S.s
#nltk.help.upenn_tagset()

#if(os.getcwd() != '/Users/Omar/Desktop/Code/recipe-parser'):
#	os.chdir("../Desktop/Code/recipe-parser")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Vocabulary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dirn_descriptors = ["baking", "cold", "covered", "deep", "dutch", "foil", "glass", "greased", "heavy", "large", "loaf", "medium", "medium-size", "mixing", "nylon", "oiled", "paper", "plastic", "roasting", "shallow", "small","soup", "steak", "towel-lined", "well", "zipper"]

dirn_measurements = ["inch"]

dirn_methods = ["add", "adjust", "air", "allow", "arrange", "assemble", "bake", "baste", "be","beat", "begin", "blanch", "blend", "boil", "bone", "braise", "bread", "break", "bring",
"broil", "brown", "bronze", "brush", "butter", "caramelize", "carve", "check", "chill", "chop", "coat", "combine", "continue", "cook", "cool", "cover", 
"crack", "crisp", "cube", "cut", "deglaze", "dice", "dip", "discard", "dissolve", "dig", "divide", "do", "drain", "dredge", "drizzle", "drop", "dry", "dust", "fill", "flip", "fluff", "freeze", "fry", 
"fold", "form", "garnish", "gather", "glaze", "grate", "grease", "grill", "heat", "increase", "julienne", "keep", "knead", "ladle", "lay", "layer", "leave", "let", "lift", "line", "lower", "make", "marinate", 
"mash", "massage", "measure", "melt", "microwave", "mince", "mix", "moisten", "note", "oil", "pat", "place", "peel", "plate", "plunge", "pinch", "pink", "poach", "poke", "pound", "pour", "preheat", "press", "prevent", "prick", "process", 
"punch", "puree", "put", "raise", "read", "record", "reduce", "refrigerate", "reheat", "remember", "remove", "repeat", "replace", "reserve", "return", "rinse", "roast", "roll", "rub", "run", "salt", "saute", "scale", 
"scatter", "scoop", "scramble", "scrape", "seal", "sear", "season", "seed", "select", "separate", "serve", "set", "shake", "shape", "shave", "shred", "sift", "simmer", "skewer", "skim", "skin", 
"slice", "smear", "smoke", "soak", "soften", "soup", "spear", "spice", "split", "spoon", "spray", "spread", "sprinkle", "spritz", "squeeze", "squirt", "stand", "steam", "stir", "stirfry", "stir-fry","store", "strain", "stuff", "suspend", "sweeten", 
"swirl", "tap", "taste", "thread", "tie", "tilt", "time", "toast", "top", "toss", "transfer", "turn", "unroll", "use","wait", "wash", "warm", "weigh", "wet", "whip", "whisk", "wipe", "wrap"]

dirn_tools = ["barbeque", "bowl", "coal", "cooker", "colander", "cover", "deep-fryer", "dish", "fork", "grate", "grill", "knife", "oven", "pan", "pot","saucepan", "set", "skillet", "spatula",
	"thongs", "toaster", "water", "wok"]

dirn_time_units = ["seconds", "minutes", "hours", "days", "second", "minute", "hour", "day"]

dirn_bad_adverbs = ["then", "there", "meanwhile", "once"]

#Maybe check if it starts with "do not"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utility Functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def removeNextRecipeTag(ing_lst):
	while("NEXT RECIPE\n" in ing_lst):
		ing_lst.remove("NEXT RECIPE\n")
	return ing_lst

def segmentByNextRecipeTag(ing_lst):
	new_ing_lst = map(lambda(x): x.replace("NEXT RECIPE", "__SPLIT__"), ing_lst)
	return new_ing_lst

def clear():
	print "\n"*70

def formatDirn(dirn):
	#remove initial number; split by sentences; remove \n
	try:
		test =  dirn[dirn.index('. ')+2:].replace('  ',' ').replace('.\n','').replace('\n','').replace("; ", ". ").split('. ')
		return test
	except:
		print "dirn is", dirn, "."

def findConsecutiveWords(lower_arr_words, lower_arr_tokens):
	#returns the index of the first of the consecutive word block, or None if it is absent
	length_words = len(lower_arr_words)
	for i in range(len(lower_arr_tokens)-length_words):
		if(lower_arr_tokens[i:i+length_words] == lower_arr_words):
			return i
	return None

def getSteps(directions):
	steps = []
	for dirn in directions:
		formatted = formatDirn(dirn) 
		if formatted!=[""]:
			steps+=formatted
	return steps

def getSteps_AdvFirst(directions):
	special = []
	steps = getSteps(directions)
	lower_steps = map(str.lower, steps)
	for lower_step in lower_steps:
		lower_step_tokens = nltk.word_tokenize(lower_step)
		lower_step_pos = nltk.pos_tag(lower_step_tokens)
		if( (lower_step_pos[0][1]=="RB") and (lower_step_tokens[0] not in dirn_methods)):	
			special.append(lower_step)
	return special

def getSteps_MethFirst(directions):
	special = []
	steps = getSteps(directions)
	lower_steps = map(str.lower, steps)
	for lower_step in lower_steps:
		lower_step_tokens = nltk.word_tokenize(lower_step)
		if (lower_step_tokens[0] in dirn_methods):	
			special.append(lower_step)
	return special

def getSteps_InFirst(directions):
	special = []
	steps = getSteps(directions)
	lower_steps = map(str.lower, steps)
	for lower_step in lower_steps:
		lower_step_tokens = nltk.word_tokenize(lower_step)
		if (lower_step_tokens[0]=="in"):	
			special.append(lower_step)
	return special

def getSteps_AllElseFirst(directions):
	special = []
	steps = getSteps(directions)
	lower_steps = map(str.lower, steps)
	for lower_step in lower_steps:
		lower_step_tokens = nltk.word_tokenize(lower_step)
		lower_step_pos = nltk.pos_tag(lower_step_tokens)
		if( (lower_step_pos[0][1]!="RB") and (lower_step_tokens[0] not in dirn_methods)):	
			special.append(lower_step)
	return special

def getFirstWord_AllElseSteps(directions):
	#Just to get each first word that is neither Method nor Adjective
	steps = getSteps_AllElseFirst(directions)
	first_words = set()
	for step in steps:
		step_toks = nltk.word_tokenize(step)
		first_words.add(step_toks[0])
	return first_words

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Work Space ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAdjacentTool(index, lower_step_tokens, lower_step_pos, retIterator=False):
	#checks if there is a tool starting from that index
	iterator, tool = index, None

	#remove "determiners" such as 'a'
	while(lower_step_pos[iterator][1]=='DT'):
		iterator+=1

	start = iterator

	#While the next_word is compatible but not a tool, we continue onwards.
	while ((lower_step_tokens[iterator] in dirn_measurements) or (lower_step_tokens[iterator] in dirn_descriptors) 
	  or (bool(filter(lambda(x): x.isdigit(), lower_step_tokens[iterator])))):
		iterator+=1

	#To ensure accuraccy some more
	if(lower_step_tokens[iterator] in dirn_tools):
		#In event we have "grill grate" or something.
		while((iterator<len(lower_step_tokens)) and (lower_step_tokens[iterator] in dirn_tools)):
			iterator+=1

		next_tool, next_iterator = None, None

		if((iterator<len(lower_step_tokens)) and (lower_step_tokens[iterator]=="or")):
			next_tool, next_iterator = getAdjacentTool(iterator+1, lower_step_tokens, lower_step_pos, retIterator=True)

		if(next_iterator!=None):
			iterator = next_iterator
			tool = lower_step_tokens[start:iterator]
		else:
			tool = lower_step_tokens[start:iterator]

		if(retIterator):
			return tool, iterator
		else:
			return tool

	if(retIterator):
		return None, None
	else:
		return None

def firstWordAdverb(lower_step, lower_step_tokens, lower_step_pos):
	#Call this function when the firstWord is an Adverb.
	#It will extract METHOD & TOOL.
	#If it can't find either, it will return None in their place
	if(lower_step_tokens[1] in dirn_methods): 
		method = lower_step_tokens[1] #Should always be the case
		iterator = 2
		tool = getAdjacentTool(iterator, lower_step_tokens, lower_step_pos)
		print "lower_step is: ", lower_step
		print "method is: ", method
		print "tool is: ", tool
		return method, tool
	else:
		print "FAILED lower_step is: ", lower_step
		raise ValueError('Adverb wasnt followed by a method')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Work Space ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def firstWordAnalysis(lower_step, recipe_ingrs_extracted_tokens=None):
	lower_step_tokens = nltk.word_tokenize(lower_step)
	lower_step_pos = nltk.pos_tag(lower_step_tokens)
	method, tool, ingredient = None, None, None
	fw = lower_step_tokens[0]
	if(fw == "("):
		#In the event of this
		return firstWordAnalysis(lower_step[lower_step.index(")")+1:], recipe_ingrs_extracted_tokens)
	
	elif (fw in dirn_methods):
		# If it is a verb
		method = fw
		in_a_index = findConsecutiveWords(["in", "a"], lower_step_tokens)
		if(in_a_index):
			tool = getAdjacentTool(in_a_index+2, lower_step_tokens, lower_step_pos)
			ingr, iterator = None, 1
			while(iterator<in_a_index):
				ingr = getAdjacentIngredient(lower_step_tokens, iterator, recipe_ingrs_extracted_tokens)
				if(ingr!=None):
					iterator+=len(ingr)
			if(ingr!=None):
				ingredient = ingr
		else:
			iterator = 1
			if(recipe_ingrs_extracted_tokens!=None):
				ingr = getAdjacentIngredient(lower_step_tokens, 1, recipe_ingrs_extracted_tokens)
				if(ingr==None):
					tool = getAdjacentTool(iterator, lower_step_tokens, lower_step_pos)
				else:
					ingredient = ingr

	elif (fw == "in"):
		#Functionality works! 
		iterator = 1
		tool, iterator = getAdjacentTool(iterator, lower_step_tokens, lower_step_pos, retIterator=True)
		if( (tool==None) or (iterator==None) ): iterator = 1

		# Check for "over ____ heat"
		if((lower_step_tokens[iterator] == "over") and (lower_step_tokens[iterator+2] == "heat")):
			iterator+=3
			
		#Get the method name. Checks for commas mainly.
		while(lower_step_tokens[iterator] not in dirn_methods):
			iterator+=1

		method = lower_step_tokens[iterator]
		
	elif ( (lower_step_pos[0][1]=="RB") and (lower_step_tokens[0] not in dirn_bad_adverbs)) :
		# if slowly, lightly, generously, lightly
		method, tool = firstWordAdverb(lower_step, lower_step_tokens, lower_step_pos)

	return method, tool, ingredient

def understandDirections(directions):
	steps = getSteps(directions)
	for step in steps:
		tool, method, ingredient = firstWordAnalysis
		if(tool == None):
			tool = extractTool()
		time = getTime(step.lower())

def getConcreteTime(step):
	""" This function takes a step (as a string) and returns a string
		like '3 to 5 minutes' or '4 hours' or 'approximately 45 minutes'."""
	tokens = nltk.word_tokenize(step)
	pos = nltk.pos_tag(tokens)

	# Check if this step metions time at all, using list defined at top of file
	time_unit = ""
	for time in dirn_time_units:
		if time in tokens:
			time_unit = time

	# If there is no mention of time, exit function
	if not time_unit:
		return "none"

	# This pattern matches anything that looks like:
	# 3 to 5 minutes, 4 hours, etc.
	final_time = ""
	pattern = "[0-9]+ [a-z]* *[0-9]* *" + time_unit

	match = re.search(pattern, step)
	if match:
		final_time = step[match.start():match.end()]
		# Add extra detail to time, if it is an estimate like "about 5 minutes"
		if "about " + final_time in step:
			final_time = "about " + final_time
		elif "approximately " + final_time in step:
			final_time = "approximately " + final_time
		# Else this step unfortunately doesn't use digits for its numbers
	# First check for numbers using NLTK Part-Of-Speech Tagging, numbers
	# are "CD"
	else:
		for word in pos:
			if word[1] == "CD":
				pattern = word[0] + " (to)? ?[a-z]* ?" + time_unit
				match = re.search(pattern, step)
				if match:
					final_time = step[match.start():match.end()]
				break
		
		# Check for phrases like "for five minutes"
	 	if "for" in tokens:
			idx = tokens.index("for") + 1
			while tokens[idx] != time_unit:
				final_time += tokens[idx] + " "
				idx += 1
			final_time += time_unit
			
		# Check for phrases like "a minute", "an hour", "an hour or two", etc
		elif " a " + time_unit in step:
			if " or two" in step:
				final_time = "a " + time_unit + " or two"

		elif " an " + time_unit in step:
			if " or two" in step:
				final_time = "an " + time_unit + " or two"	

		elif " a few " + time_unit in step:
			final_time = "a few " + time_unit

	# A few steps specify "per side" or "per batch", this grabs them
	if "per" in tokens:
		final_time += " per " + tokens[tokens.index("per") + 1]

	return final_time

def getUntilTime(step):
	"""This function takes a step (as a string) that has the word 'until' in it,
	   and returns a string with the rest of the phrase, i.e. 'until golden brown'"""

	until_time = ""
	tokens = nltk.word_tokenize(step)
	idx = tokens.index("until")	
	while idx < len(tokens) and tokens[idx] not in ",./;:()[]{}\|":
		until_time += tokens[idx] + " "
		idx += 1

	return until_time.strip()
 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interface ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# directions = removeNextRecipeTag(list(open("directions.txt", "r")))
# allDirections = removeNextRecipeTag(list(open("Directions/allDirections.txt", "r")))
asianDirections = removeNextRecipeTag(list(open("Directions/asianDirections.txt", "r")))
# diabeticDirections = removeNextRecipeTag(list(open("Directions/diabeticDirections.txt", "r")))
# dietHealthDirections = removeNextRecipeTag(list(open("Directions/dietHealthDirections.txt", "r")))
# glutenfreeDirections = removeNextRecipeTag(list(open("Directions/gluten-freeDirections.txt", "r")))
# healthyrecipesDirections = removeNextRecipeTag(list(open("Directions/healthy-recipesDirections.txt", "r")))
# indianDirections = removeNextRecipeTag(list(open("Directions/indianDirections.txt", "r")))
# italianDirections = removeNextRecipeTag(list(open("Directions/italianDirections.txt", "r")))
# lowcalorieDirections = removeNextRecipeTag(list(open("Directions/low-calorieDirections.txt", "r")))
# lowfatDirections = removeNextRecipeTag(list(open("Directions/low-fatDirections.txt", "r")))
# mexicanDirections = removeNextRecipeTag(list(open("Directions/mexicanDirections.txt", "r")))
# southernDirections = removeNextRecipeTag(list(open("Directions/southernDirections.txt", "r")))
# worldDirections = removeNextRecipeTag(list(open("Directions/worldDirections.txt", "r")))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



