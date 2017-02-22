import nltk, string, os

# os.chdir("documents/eecs/eecs337/recipe-parser")

#---------------------------------------------------------------------------------------------------------------------------------------------
# Vocabulary
# List of measurement words
measurements = ["tablespoons", "tablespoon", "cup", "cups", "rib", "teaspoon", "teaspoons", "pound", "pounds", "cloves", "clove", "slice", 
"slices", "pinch", "can", "cans", "ounce", "ounces", "package", "packages", "rack", "fillet", "fillets", "bottle", "bottles", "fluid", "head",
"heads", "containter", "sprig", "sprigs", "stalk", "stalks", "jar", "jars", "dash", "fluid ounce", "fluid ounces"]
# List of containers
containers = ["can", "cans", "bottle", "bottles", "jar", "jars", "package", "packages"]
# List of conjunctions
conjunctions = ["for", "and", "nor", "but", "or", "yet", "so"]

# Exceptions/Improvements?:
#
#	"1 pinch cayenne pepper, or to taste"
#		Do we want to include the ", or to taste"?
#		i.e. Quantity: 2, or to taste
#
def parse_ingredient (ingredient):
	# Initialize list of tokens
	word_list = nltk.word_tokenize(ingredient)
	lower_word_list = map(str.lower, word_list)

	lower_ingredient = str.lower(ingredient)
	increment, word_list_len = 0, len(word_list)

	# Initialize dictionary
	ingredient_dictionary = {'Quantity': None, 'Measurement': None, 'Ingredient': None, 'Preperation': None}

	# Set empty strings
	quantity = ""
	measurement = ""
	ingredient_name = ""
	preperation = ""
	new_quantity = ""
	new_measurement = ""

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
			while ((increment < word_list_len) and (any(char.isdigit() for char in lower_word_list[increment]))):
				if (new_quantity != ""):
					new_quantity += " "
				new_quantity += lower_word_list[increment]
				increment += 1
			# Find measurement
			while ((increment < word_list_len) and (lower_word_list[increment] in measurements)):
				if (new_measurement != ""):
					new_measurement += " "
				new_measurement += lower_word_list[increment]
				increment += 1
			if (tmp_inc == increment):
				increment += 1
		increment += 1

	# If a measurement was not found within a bracketed statement, find measurement
	while ((increment < word_list_len) and (lower_word_list[increment] in measurements)):
		if (measurement != ""):
			measurement += " "
		measurement += lower_word_list[increment]
		increment += 1

	if (measurement in containers):
		measurement = new_measurement
		quantity = new_quantity

	elif ((new_measurement != "") and (measurement != "")):
		measurement = new_quantity + " " + new_measurement + " " + measurement

	# Find ingredient name
	# Currently needs work to find the descriptor
	while ((increment < word_list_len) and (lower_word_list[increment] != ",")):
		if (ingredient_name != ""):
			ingredient_name += " "
		ingredient_name += lower_word_list[increment]
		increment += 1

	# Find preperation
	if ((increment < word_list_len) and (lower_word_list[increment] == ",")):
		increment += 1
		while (increment < word_list_len):
			if ((preperation != "") and (lower_word_list[increment] != ",")):
				preperation += " "
			preperation += lower_word_list[increment]
			increment += 1

	ingredient_name = ingredient_name.replace(", or as needed", "")
	ingredient_name = ingredient_name.replace(", or to taste", "")
	ingredient_name = ingredient_name.replace("or as needed", "")
	ingredient_name = ingredient_name.replace("or to taste", "")
	ingredient_name = ingredient_name.replace(" as needed", "")
	ingredient_name = ingredient_name.replace(" to taste", "")
#                                                           )
#                                                          )
	preperation = preperation.replace(", or as needed", "")
	preperation = preperation.replace(", or to taste", "")
	preperation = preperation.replace("or as needed", "")
	preperation = preperation.replace("or to taste", "")

	# Assigns parsed string values to appropriate dictionary keys.
	# Leaves dictionary value as None if still an empty string
	# we may want to change that interaction depending on how we plan to use the output of this parser.
	if (preperation != ""):
		ingredient_dictionary['Preperation'] = preperation

	if (ingredient_name != ""):
		ingredient_dictionary['Ingredient'] = ingredient_name

	if (measurement != ""):
		ingredient_dictionary['Measurement'] = measurement

	if (quantity != ""):
		ingredient_dictionary['Quantity'] = quantity

	return ingredient_dictionary

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


ingredients = list(open("ingredients.txt", "r"))

# Used to find a potentially unlisted measurement from an ingredient string
def find_measurements():
	new_measurements = []
	for ingredient in ingredients:
		new_measurements.append(parse_measurement(ingredient))
	for possibility in new_measurements:
		new_measurements[:] = [item for item in new_measurements if item != possibility]
		new_measurements.append(possibility)
	for possibility in new_measurements:
		if (possibility not in measurements):
			print possibility

def run_all():
	for ingredient in ingredients:
		print ingredient
		ing_dict = parse_ingredient(ingredient)
		for key in ing_dict.keys():
			if (ing_dict[key] != None):
				print key + ": " + ing_dict[key]
		print " "

def run_tests():
	for ingredient in list_of_ingredients:
		print ingredient
		ing_dict = parse_ingredient(ingredient)
		for key in ing_dict.keys():
			if (ing_dict[key] != None):
				print key + ": " + ing_dict[key]
		print " "

list_of_ingredients = ["2 chipotle chilies in adobo sauce, minced, or to taste", 
"1 1/2 pounds ground beef",
"salt and pepper to taste", 
"1 (1 ounce) package dry onion soup mix",
"1 (8 ounce) can tomato sauce",
"1/2 cup barbecue sauce, or as needed",
"1 pinch cayenne pepper, or to taste",
"2 (6.5 ounce) cans canned tomato sauce",
"1 (10 ounce) package frozen chopped spinach , thawed, drained and squeezed dry",
"4 (6 ounce) fillets salmon"]