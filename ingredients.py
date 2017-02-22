import nltk, string, os

# Vocabulary
# List of measurement words
measurements = ["tablespoons", "tablespoon", "cup", "cups", "rib", "teaspoon", "teaspoons", "pound", "pounds", "cloves", "cloves", "slice", "slices", "pinch", "can", "cans", "ounce", "ounces", "package", "packages", "rack"]

# Exceptions/Improvements?:
#
#	"1 pinch cayenne pepper, or to taste"
#		Do we want to include the ", or to taste"?
#		i.e. Quantity: 2, or to taste ?
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
			# Reset quantity to empty string
			quantity = ""
			# Find new quantity
			while ((increment < word_list_len) and (any(char.isdigit() for char in lower_word_list[increment]))):
				if (quantity != ""):
					quantity += " "
				quantity += lower_word_list[increment]
				increment += 1
			# Find measurement
			while ((increment < word_list_len) and (lower_word_list[increment] in measurements)):
				if (measurement != ""):
					measurement += " "
				measurement += lower_word_list[increment]
				increment += 1
		increment += 1
		# Increment past the measurement word after the brackets
		while ((increment < word_list_len) and (lower_word_list[increment] in measurements)):
			increment += 1

	# If a measurement was not found within a bracketed statement, find measurement
	if (measurement == ""):
		while ((increment < word_list_len) and (lower_word_list[increment] in measurements)):
			if (measurement != ""):
				measurement += " "
			measurement += lower_word_list[increment]
			increment += 1

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
		while ((increment < word_list_len) and (lower_word_list[increment] != ",")):
			if (preperation != ""):
				preperation += " "
			preperation += lower_word_list[increment]
			increment += 1

	# Assigns parsed string values to appropriate dictionary keys.
	# Leaves dictionary value as None if still an empty string
	# we may want to change that interaction depending on how we plan to use the output of this parser.
	if ((preperation != "") and (preperation != "or as needed") and (preperation != "or to taste")):
		ingredient_dictionary['Preperation'] = preperation

	if (ingredient_name != ""):
		ingredient_dictionary['Ingredient'] = ingredient_name

	if (measurement != ""):
		ingredient_dictionary['Measurement'] = measurement

	if (quantity != ""):
		ingredient_dictionary['Quantity'] = quantity

	return ingredient_dictionary

def test_ingredient_parser():
	print " "
	for ingredient in list_of_ingredients:
		print ingredient
		ing_dict = parse_ingredient(ingredient)
		for key in ing_dict.keys():
			if (ing_dict[key] != None):
				print key + ": " + ing_dict[key]
		print " "

list_of_ingredients = ["2 chipotle chilies in adobo sauce, minced, or to taste", 
"1 1/2 pounds ground beef", 
"1 1/2 pounds ground beef", 
"salt and pepper to taste", 
"1 (1 ounce) package dry onion soup mix",
"1 (8 ounce) can tomato sauce",
"1/2 cup barbecue sauce, or as needed",
"1 pinch cayenne pepper, or to taste"]