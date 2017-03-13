#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set-up: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import nltk, string, os, re
from nltk.tokenize import WhitespaceTokenizer
# os.chdir("documents/eecs/eecs337/recipe-parser")
#execfile('/Users/Omar/Desktop/Code/recipe-parser/directions.py')

#for list of all possible NLTK P.O.S.s
#nltk.help.upenn_tagset()

#if(os.getcwd() != '/Users/Omar/Desktop/Code/recipe-parser'):
#	os.chdir("../Desktop/Code/recipe-parser")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Vocabulary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dirn_descriptors = ["baking", "cold", "combined", "covered", "deep", "dutch", "foil", "glass", "greased", "heavy", "individual", "large", "loaf", "medium", "medium-size", "mixed", "mixing", "nylon", "oiled", "paper", "plastic", "preheated", "remaining", "reserved", "roasting", "rolled", "shallow", "small","soup", "steak", "towel-lined", "well", "zipper"]

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

dirn_primary_methods = ["bake", "baste", "blanch", "boil", "braise", "broil", "bronze", "caramelize", "cook", "fry", "glaze", "grill", "poach", "reduce", 
  "roast", "saute", "sear", "smoke", "steam", "stirfry", "stir-fry", "toast"]

dirn_tools = ["barbeque", "bowl","bowls", "coal", "cooker", "colander", "cover", "deep-fryer", "dish", "fork", "grate", "grill", "knife", "oven", "pan", "plate", "plates", "pot","saucepan", "set", "skillet", "spatula",
	"thongs", "toaster", "water", "wok"]

dirn_time_units = ["seconds", "minutes", "hours", "days", "second", "minute", "hour", "day"]

dirn_bad_adverbs = ["then", "there", "meanwhile", "once"]

dirn_split_toks = [",", ";", "of", "in", "to", "and", "with"]

#Maybe check if it starts with "do not"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utility Functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def removeNextRecipeTag(ing_lst):
	while("NEXT RECIPE\n" in ing_lst):
		ing_lst.remove("NEXT RECIPE\n")
	return ing_lst

def segmentByNextRecipeTag(ing_lst):
	new_ing_lst = map(lambda(x): x.replace("NEXT RECIPE", "__SPLIT__"), ing_lst)
	return new_ing_lst

def formatDirn(dirn):
	#remove initial number; split by sentences; remove \n
	test =  dirn[dirn.index('. ')+2:].replace('  ',' ').replace('.\n','').replace('\n','').replace("; ", ". ").split('. ')
	return test

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

def getSteps_BracketsFirst(directions):
	special = []
	steps = getSteps(directions)
	lower_steps = map(str.lower, steps)
	for lower_step in lower_steps:
		lower_step_tokens = nltk.word_tokenize(lower_step)
		if(lower_step_tokens[0]=="("):	
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

def splitForSplitAnalysis(lower_step):
	lower_step_list = [lower_step]
	for split_tok in dirn_split_toks:
		for i in lower_step_list:
			toks = nltk.word_tokenize(i)
			if split_tok in toks:
				lower_step_list+=map(str.strip, i.split(split_tok))
				lower_step_list.remove(i)
	return lower_step_list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interface ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# directions = removeNextRecipeTag(list(open("directions.txt", "r")))
# allDirections = removeNextRecipeTag(list(open("Directions/allDirections.txt", "r")))
# asianDirections = removeNextRecipeTag(list(open("Directions/asianDirections.txt", "r")))
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



