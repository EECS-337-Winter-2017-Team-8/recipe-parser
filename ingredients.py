#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set-up: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import nltk, string, os
# os.chdir("documents/eecs/eecs337/recipe-parser")
# execfile('/Users/Omar/Desktop/Code/recipe-parser/ingredients.py')

#for list of all possible NLTK P.O.S.s
#nltk.help.upenn_tagset()

if(os.getcwd() != '/Users/Omar/Desktop/Code/recipe-parser'):
	os.chdir("../Desktop/Code/recipe-parser")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Vocabulary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# List of measurement words
ing_measurements = [ "tablespoons", "tablespoon", "cup", "cups", "rib", "teaspoon", "teaspoons", "pound", "pounds", 
"cloves", "clove", "slice", "slices", "pinch", "can", "cans", "ounce", "ounces", "package", "packages", "rack",
"bottle", "bottles", "fluid", "head", "heads", "containter", "sprig", "sprigs", "stalk", 
"stalks", "jar", "jars", "dash", "fluid ounce", "fluid ounces", "inch", "inches", "foot", "feet", "halves",
"half", "dollop", "dollops" ]

# List of descriptors
ing_descriptors = [ "bone-in", "frozen", "fresh", "extra", "very", "lean", "fatty", "virgin", "extra-virgin", "small",
"large", "tiny", "big", "giant", "long", "short", "whole", "wheat", "grain", "hot", "cold", "ground", "sweet",
"seasoned", "italian-seasoned", "extra-extra-virgin" ]

# List of containers
ing_containers = [ "can", "cans", "bottle", "bottles", "jar", "jars", "package", "packages", "container", "containers" ]

# List of conjunctions
conjunctions = [ "for", "and", "nor", "but", "or", "yet", "so" ]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utility Functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def removeNextRecipeTag(ing_lst):
	while("NEXT RECIPE\n" in ing_lst):
		ing_lst.remove("NEXT RECIPE\n")
	return ing_lst

def clear():
	print "\n"*70

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Parse Functions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Exceptions/Improvements?:
#
#	"1 pinch cayenne pepper, or to taste"
#		Do we want to include the ", or to taste"?
#		i.e. Quantity: 2, or to taste
#
#	"1/4 cup all-purpose flour for coating"
#		Ingredient: all-purpose flour for coating
#
# To check meaning of tags use nltk.help.upenn_tagset()

def parse_ingredient (ingredient):
	# Initialize list of tokens
	word_list = nltk.word_tokenize(ingredient)
	lower_word_list = map(str.lower, word_list)

	lower_ingredient = str.lower(ingredient)
	increment, word_list_len = 0, len(word_list)

	# Initialize dictionary
	ingredient_dictionary = { 'Quantity': None, 'Measurement': None, 'Ingredient': None, 'Preparation': None, 'Descriptor': None }

	# Set empty strings
	quantity, measurement, ingredient_name, preparation, descriptor, new_quantity, new_measurement = "", "", "", "", "", "", ""

	# For parsing ingredient
	ingredient_name_tokens, ingredient_tokens, ingredient_pos = [], None, None

	# Find quantity
	while ((increment < word_list_len) and (any(char.isdigit() for char in lower_word_list[increment]))):
		if (quantity != ""):
			quantity += " "
		quantity += lower_word_list[increment]
		increment += 1

	# Some ingredients don't have a numeric quantity because they are added "to taste"
	# i.e. "salt and pepper to taste"
	# should produce Quantity: to taste
	if (quantity == ""):
		if (lower_ingredient.find("to taste") != -1):
			quantity = "to taste"

	# If quantity and measurement are actually in brackets
	# i.e. "1 (8 ounce) can tomato sauce"
	# should produce Quantity: 8, Measurement: Ounce
	if ((increment < word_list_len) and (lower_word_list[increment] == "(")):
		increment += 1
		while ((increment < word_list_len) and (lower_word_list[increment] != ")")):
			tmp_inc = increment
			# Find new quantity
			while ((increment < word_list_len) and ((any(char.isdigit() for char in lower_word_list[increment])) or (lower_word_list[increment] in ing_measurements))):
				if (new_measurement != ""):
					new_measurement += " "
				new_measurement += lower_word_list[increment]
				increment += 1
			if (tmp_inc == increment):
				increment += 1
		increment += 1

	# Find measurement in the rest of the ingredient
	while ((increment < word_list_len) and (lower_word_list[increment] in ing_measurements)):
		if (measurement != ""):
			measurement += " "
		measurement += lower_word_list[increment]
		increment += 1


	if (measurement in ing_containers):
		if(new_measurement!=""):
			measurement = new_measurement+" "+measurement

	elif ((new_measurement != "") and (measurement == "")):
		measurement = new_measurement

	elif ((new_measurement != "") and (measurement != "")):
		measurement = new_measurement + " " + measurement

	# Find ingredient name
	while ((increment < word_list_len) and (lower_word_list[increment] != ",") and (lower_word_list[increment] != "-")):
		if (lower_word_list[increment] not in ing_containers):
			if (ingredient_name != ""):
				ingredient_name += " "
			ingredient_name += lower_word_list[increment]
			ingredient_name_tokens.append(lower_word_list[increment])
		increment += 1
	# Find preparation
	if ((increment < word_list_len) and ((lower_word_list[increment] == ",") or (lower_word_list[increment] == "-"))):
		increment += 1
		while (increment < word_list_len):
			if ((preparation != "") and (lower_word_list[increment] != ",")):
				preparation += " "
			preparation += lower_word_list[increment]
			increment += 1

	ingred_repl = [", plus more for topping", " plus more for topping", "plus more for topping", ", or more to taste", " or more to taste", "or more to taste", "more to taste",
	", or as needed", ", or to taste", "or as needed", "or to taste", " as needed", " to taste"]
	prep_repl = [", or as needed", ", or to taste", "or as needed", "or to taste", ", plus more for topping", " plus more for topping", "plus more for topping", ", or more to taste",
	" or more to taste", "or more to taste", "more to taste"]

	if(ingredient_name != ""):
		for i_r in ingred_repl:
			ingredient_name = ingredient_name.replace(i_r, "")
	if(preparation!=""):
		for p_r in prep_repl:
			preparation = preparation.replace(p_r, "")

	# Parse ingredient to find descriptor
	newIngDescPrep = parse_ing_name(lower_word_list, ingredient_name, ingredient_name_tokens)
	ingredient_name = newIngDescPrep[1]
	if (descriptor != ""):
		descriptor += ", "
	descriptor += newIngDescPrep[2]
	if (preparation != ""):
		preparation += " "
	preparation += newIngDescPrep[3]
	if (measurement == ""):
		measurement = newIngDescPrep[4]
	# In case there was a comma in a weird place
	# i.e. "4 skinless, boneless chicken breast halves"
	#
	# Otherwise parser will think "skinless" is ingreadient
	# and "boneless chicken breast halves" is preparation
	if ((ingredient_name == "") and (preparation != "")):
		stopFlag = False
		while_inc = 0
		while ((ingredient_name == "") and (while_inc < 10)):
			ingredient_name = ""
			ingredient_name_tokens = []
			prep_tokens = nltk.word_tokenize(preparation)
			prep_token_len = len(prep_tokens)
			tmp_inc = 0
			while ((tmp_inc < prep_token_len) and (prep_tokens[tmp_inc] != ",")):
				if (preparation[tmp_inc] not in ing_containers):
					if (ingredient_name != ""):
						ingredient_name += " "
					ingredient_name += prep_tokens[tmp_inc]
					ingredient_name_tokens.append(prep_tokens[tmp_inc])
				tmp_inc += 1
			preparation = preparation.replace(ingredient_name + ", ", "")
			preparation = preparation.replace(ingredient_name, "")
			while_inc += 1
			if (while_inc < 10):
				newIngDescPrep = parse_ing_name(lower_word_list, ingredient_name, ingredient_name_tokens)
				ingredient_name = newIngDescPrep[1]
				if (descriptor != ""):
					descriptor += ", "
				descriptor += newIngDescPrep[2]
				if (preparation != ""):
					preparation += ", "
				preparation += newIngDescPrep[3]
				if (measurement == ""):
					measurement = newIngDescPrep[4]

	# Remove comma from the end of preparation
	if (preparation != ""):
		final_prep_tokens = nltk.word_tokenize(preparation)
		if (final_prep_tokens[len(final_prep_tokens) - 1] == ","):
			preparation = preparation.replace(" , ", "")
			preparation = preparation.replace(", ", "")
			preparation = preparation.replace(" ,", "")
			preparation = preparation.replace(",", "")
	# Remove comma from the end of descriptor
	if (descriptor != ""):
		final_prep_tokens = nltk.word_tokenize(descriptor)
		if (final_prep_tokens[len(final_prep_tokens) - 1] == ","):
			descriptor = descriptor.replace(" , ", "")
			descriptor = descriptor.replace(", ", "")
			descriptor = descriptor.replace(" ,", "")
			descriptor = descriptor.replace(",", "")
	# Assigns parsed string values to appropriate dictionary keys.
	# Leaves dictionary value as None if still an empty string
	# we may want to change that interaction depending on how we plan to use the output of this parser.
	if (descriptor != ""):
		ingredient_dictionary['Descriptor'] = descriptor

	if (preparation != ""):
		ingredient_dictionary['Preparation'] = preparation

	if (ingredient_name != ""):
		ingredient_dictionary['Ingredient'] = ingredient_name

	if (measurement != ""):
		ingredient_dictionary['Measurement'] = measurement

	if (quantity != ""):
		ingredient_dictionary['Quantity'] = quantity

	return ingredient_dictionary

def parse_ing_name(ingredient, ingredient_name, ingredient_name_tokens):
	results = { 1: None, 2: None, 3: None, 4: None }
	descriptor, preparation, measurement = "", "",""
	
	ingredient_pos = nltk.pos_tag(ingredient)
	ing_pos_len = len(ingredient_pos)
	increment = 0

	while (increment < ing_pos_len):
		if (ingredient_pos[increment][0] in ingredient_name_tokens):
			if ((ingredient_pos[increment][1] == 'VBN') or (ingredient_pos[increment][0] in ing_descriptors) or (ingredient_pos[increment][0].find("less") != -1)):
				#verb, past participle. Used w/ Auxillary version of has
				#he HAS ridden. he HAS eaten. he HAS rowed the boat.
				if (descriptor != ""):
					descriptor += " "
				descriptor += ingredient_pos[increment][0]
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")

			elif ((ingredient_pos[increment][1] == 'VBD') or (ingredient_pos[increment][1] == 'RB')):
				#VBD past tense Verb: dipped, pleased, swiped, adopted, strode, wore
				#RB averb. occassionally, professionally, maddeningly, swiftly, quickly
				if (preparation != ""):
					preparation += " " + ingredient_pos[increment][0]
				else:
					preparation = ingredient_pos[increment][0]
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")

			elif (ingredient_pos[increment][0] in ing_measurements):
				measurement += ingredient_pos[increment][0]
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")

			elif (ingredient_pos[increment][0] == "("):
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")
				increment += 1
				if (descriptor != ""):
					descriptor += " ; "
				while ((increment < ing_pos_len) and (ingredient_pos[increment][0] != ")")):
					if (descriptor != ""):
						descriptor += " "
					descriptor += ingredient_pos[increment][0]
					ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0] + " ", "")
					ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
					ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
					ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")
					increment += 1
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")

			elif ((ingredient_pos[increment][0] == "CC") and (ingredient_pos[increment][0] != "and")):
				#CC: Conjunction, coordinating. 
				#and both but either et for less minus neither nor or plus so therefore times yet whether
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")

			elif (ingredient_pos[increment][0] == "-"):
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
				ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")
				increment += 1
				while (increment < ing_pos_len):
					if (preparation != ""):
						preparation += " "
					preparation += ingredient_pos[increment][0]
					ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0] + " ", "")
					ingredient_name = ingredient_name.replace(" " + ingredient_pos[increment][0], "")
					ingredient_name = ingredient_name.replace(ingredient_pos[increment][0] + " ", "")
					ingredient_name = ingredient_name.replace(ingredient_pos[increment][0], "")
					increment += 1

		increment += 1

	results[1] = ingredient_name
	results[2] = descriptor
	results[3] = preparation
	results[4] = measurement
	return results

# Used to find a potentially unlisted measurement from an ingredient string
def parse_measurement(ingredient):
	word_list = nltk.word_tokenize(ingredient)
	lower_word_list = map(str.lower, word_list)

	lower_ingredient = str.lower(ingredient)
	increment, word_list_len = 0, len(word_list)

	measurement = ""

	while ((increment < word_list_len) and (any(char.isdigit() for char in lower_word_list[increment]))):
		increment += 1

	if ((increment < word_list_len) and (lower_word_list[increment] == "(")):
		increment += 1
		while ((increment < word_list_len) and (lower_word_list[increment] != ")")):
			while ((increment < word_list_len) and (any(char.isdigit() for char in lower_word_list[increment]))):
				increment += 1
			# Find measurement
			measurement += lower_word_list[increment] + " "
			increment += 1
		increment += 1

	measurement += lower_word_list[increment]

	return measurement

# Easier way to check part of speech
def easy_pos_tag(ingredient):
	return nltk.pos_tag(nltk.word_tokenize(ingredient))

# Used to find a potentially unlisted measurement from an ingredient string
def find_measurements():
	new_measurements = []
	for ingredient in ingredients:
		new_measurements.append(parse_measurement(ingredient))
	for possibility in new_measurements:
		new_measurements[:] = [item for item in new_measurements if item != possibility]
		new_measurements.append(possibility)
	for possibility in new_measurements:
		if (possibility not in ing_measurements):
			print possibility

def run_all():
	used_ingredients = []
	for ingredient in ingredients:
		if (ingredient not in used_ingredients):
			ing_dict = parse_ingredient(ingredient)
			print ingredient
			print " "
			ing_dict = parse_ingredient(ingredient)
			for key in ing_dict.keys():
				if (ing_dict[key] != None):
					print key + ": " + ing_dict[key]
			print " "
			print nltk.pos_tag(nltk.word_tokenize(ingredient))
			print " "
			print " "

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Used in directions.py ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAdjacentIngredient(index, lower_step_tokens, lower_step_pos, retIterator=False):
	#checks if there is an ingredient starting from that index
		# heat [4 cups vegetable oil] in a deep-fryer
		# beat the [egg] in a mixing bowl
		# add the [chicken cubes];

	iterator, ingredient = index, None

	#remove "determiners" such as 'a', 'the', 'an', 'these', 'those',
	while(lower_step_pos[iterator][1]=='DT'):
		iterator+=1

	#While the next_word is compatible, we continue onwards.
	while ((lower_step_pos[iterator][1]=="CD") (lower_step_tokens[iterator] in ing_measurements) | (lower_step_tokens[iterator] in ing_descriptors) | (lower_step_tokens[iterator] in ing_containers)):
		iterator+=1



	start = iterator



	#checks if there is a tool starting from that index
	iterator, tool = index, None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interface ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ingredients = removeNextRecipeTag(list(open("ingredients.txt", "r")))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def run_tests():
	for ingredient in list_of_ingredients:
		ingredient_words = None
		print ingredient
		ing_dict = parse_ingredient(ingredient)
		for key in ing_dict.keys():
			if (ing_dict[key] != None):
				print key + ": " + ing_dict[key]
		print " "
		ingredient_words = nltk.pos_tag(nltk.word_tokenize(ingredient))
		print ingredient_words
		print " "

def omar_tests(i):
	for i in ingredients[:i]:
		omar = parse_ingredient(i)
		print i
		print omar
		print "~~~~~~~~~~~~~~~~~"

list_of_ingredients = ["2 chipotle chilies in adobo sauce, minced, or to taste", 
"1 1/2 pounds ground beef",
"salt and pepper to taste", 
"1 (1 ounce) package dry onion soup mix",
"1 (8 ounce) can tomato sauce",
"1/2 cup barbecue sauce, or as needed",
"1 pinch cayenne pepper, or to taste",
"2 (6.5 ounce) cans canned tomato sauce",
"1 (10 ounce) package frozen chopped spinach , thawed, drained and squeezed dry",
"4 (6 ounce) fillets salmon",
"1 cup finely grated Parmigiano-Reggiano cheese, plus more for topping"]

