#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set-up: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import nltk, string, os
# os.chdir("documents/eecs/eecs337/recipe-parser")
#execfile('/Users/Omar/Desktop/Code/recipe-parser/directions.py')

#for list of all possible NLTK P.O.S.s
#nltk.help.upenn_tagset()

if(os.getcwd() != '/Users/Omar/Desktop/Code/recipe-parser'):
	os.chdir("../Desktop/Code/recipe-parser")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Vocabulary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
descriptors = ["baking", "dutch", "heavy", "large", "loaf", "medium", "small"]

measurements = ["inch"]

methods = ["add", "adjust", "air", "arrange", "assemble", "bake", "baste", "beat", "begin", "blanch", "blend", "boil", "bone", "braise", "bread", "bring",
"broil", "brown", "bronze", "brush", "butter", "caramelize", "carve", "check", "chill", "chop", "coat", "combine", "continue", "cook", "cool", "cover", 
"crack", "crisp", "cut", "deglaze", "dice", "dip", "discard", "dissolve", "dig", "drain", "dredge", "drizzle", "dry", "fill", "flip", "freeze", "fry", 
"fold", "form", "garnish", "glaze", "grate", "grease", "grill", "heat", "increase", "julienne", "knead", "layer", "leave", "let", "line", "lower", "make", "marinate", 
"mash", "massage", "measure", "melt", "mince", "mix", "moisten", "oil", "pat", "place", "peel", "plate", "pink", "poach", "pound", "pour", "preheat", "press", "prevent", 
"puree", "read", "reduce", "refrigerate", "reheat", "remove", "repeat", "replace", "reserve", "return", "rinse", "roast", "roll", "rub", "salt", "saute", "scale", 
"scatter", "scramble", "scrape", "sear", "season", "seed", "select", "separate", "serve", "set", "shake", "shave", "sift", "simmer", "skewer", "skim", "skin", 
"slice", "smear", "smoke",  "soak", "soften", "spice", "spoon", "spread", "sprinkle", "steam", "stir", "stirfry", "strain", "stuff", "swirl", "taste", "tie", "tilt",
 "toast", "top", "toss", "transfer", "turn", "unroll", "wait", "wash", "warm", "weigh", "whip", "whisk", "wrap"]

tools = ["barbeque", "bowl", "coal", "cooker", "dish", "fork", "grate", "grill", "knife", "oven", "pan","saucepan", "skillet", "spatula",
	"thongs", "toaster"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utility Functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def removeNextRecipeTag(ing_lst):
	while("NEXT RECIPE\n" in ing_lst):
		ing_lst.remove("NEXT RECIPE\n")
	return ing_lst

def clear():
	print "\n"*70

def formatDirn(dirn):
	#remove initial number; split by sentences; remove \n
	return dirn[dirn.index('. ')+2:].replace('  ',' ').replace('.\n','').replace('\n','').split('. ')

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
		if( (lower_step_pos[0][1]=="RB") and (lower_step_tokens[0] not in methods)):	
			special.append(lower_step)
	return special

def getSteps_MethFirst(directions):
	special = []
	steps = getSteps(directions)
	lower_steps = map(str.lower, steps)
	for lower_step in lower_steps:
		lower_step_tokens = nltk.word_tokenize(lower_step)
		if (lower_step_tokens[0] in methods):	
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
		if( (lower_step_pos[0][1]!="RB") and (lower_step_tokens[0] not in methods)):	
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
	while ((lower_step_tokens[iterator] in measurements) or (lower_step_tokens[iterator] in descriptors) 
	  or (bool(filter(lambda(x): x.isdigit(), lower_step_tokens[iterator])))):
		iterator+=1

	#To ensure accuraccy some more
	if(lower_step_tokens[iterator] in tools):
		#In event we have "grill grate" or something.
		while((iterator<len(lower_step_tokens)) and (lower_step_tokens[iterator] in tools)):
			iterator+=1
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
	if(lower_step_tokens[1] in methods): 
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
	return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Work Space ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def firstWordAnalysis(lower_step):
	lower_step_tokens = nltk.word_tokenize(lower_step)
	lower_step_pos = nltk.pos_tag(lower_step_tokens)
	method, tool = None, None
	fw = lower_step_tokens[0]
	if (fw in methods):
		# If it is a verb
		method = fw

	elif (fw == "in"):
		#Functionality works! 
		iterator = 1
		tool, iterator = getAdjacentTool(iterator, lower_step_tokens, lower_step_pos, retIterator=True)
		print ("lower_step_tokens[iterator] is: ", lower_step_tokens[iterator])
		# #Get the tool name
		# iterator = 1
		# while(lower_step_pos[iterator][1]=='DT'):
		# 	iterator+=1
		# t_start = iterator
		# while(lower_step_tokens[iterator] not in tools) or (lower_step_tokens[iterator+1]=="or"):
		# 	iterator+=1
		# tool = lower_step_tokens[t_start:iterator+1]

		# Check for "over ____ heat"
		if((lower_step_tokens[iterator] == "over") and (lower_step_tokens[iterator+2] == "heat")):
			iterator+=3
			
		#Get the method name. Checks for commas mainly.
		while(lower_step_tokens[iterator] not in methods):
			iterator+=1

		method = lower_step_tokens[iterator]
		
	elif (lower_step_pos[0][1]=="RB"):
		# if slowly, lightly, generously, lightly
		method, tool = firstWordAdverb(lower_step, lower_step_tokens, lower_step_pos)

	return method, tool





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interface ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

directions = removeNextRecipeTag(list(open("directions.txt", "r")))



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



