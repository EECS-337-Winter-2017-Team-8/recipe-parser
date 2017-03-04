#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set-up: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import nltk, string, os
# os.chdir("documents/eecs/eecs337/recipe-parser")
#execfile('/Users/Omar/Desktop/Code/recipe-parser/ingredient_helper.py')

if(os.getcwd() != '/Users/Omar/Desktop/Code/recipe-parser'):
	os.chdir("../Desktop/Code/recipe-parser")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Vocabulary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# List of measurement words
measurements = [ "tablespoons", "tablespoon", "cup", "cups", "rib", "teaspoon", "teaspoons", "pound", "pounds", 
"cloves", "clove", "slice", "slices", "pinch", "can", "cans", "ounce", "ounces", "package", "packages", "rack",
"bottle", "bottles", "fluid", "head", "heads", "containter", "sprig", "sprigs", "stalk", 
"stalks", "jar", "jars", "dash", "fluid ounce", "fluid ounces", "inch", "inches", "foot", "feet", "halves",
"half", "dollop", "dollops" ]

# List of descriptors
descriptors = [ "bone-in", "frozen", "fresh", "extra", "very", "lean", "fatty", "virgin", "extra-virgin", "small",
"large", "tiny", "big", "giant", "long", "short", "whole", "wheat", "grain", "hot", "cold", "ground", "sweet",
"seasoned", "italian-seasoned", "extra-extra-virgin" ]

# List of containers
containers = [ "can", "cans", "bottle", "bottles", "jar", "jars", "package", "packages", "container", "containers" ]

# List of conjunctions
conjunctions = [ "for", "and", "nor", "but", "or", "yet", "so" ]

ingredient = "1 tablespoon freshly ground black pepper"


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
		while ((increment < word_list_len) and ((any(char.isdigit() for char in lower_word_list[increment])) or (lower_word_list[increment] in measurements))):
			if (new_measurement != ""):
				new_measurement += " "
			new_measurement += lower_word_list[increment]
			increment += 1
		if (tmp_inc == increment):
			increment += 1
	increment += 1

# Find measurement in the rest of the ingredient
while ((increment < word_list_len) and (lower_word_list[increment] in measurements)):
	if (measurement != ""):
		measurement += " "
	measurement += lower_word_list[increment]
	increment += 1


if (measurement in containers):
	if(new_measurement!=""):
		measurement = new_measurement+" "+measurement

elif ((new_measurement != "") and (measurement == "")):
	measurement = new_measurement

elif ((new_measurement != "") and (measurement != "")):
	measurement = new_measurement + " " + measurement

# Find ingredient name
while ((increment < word_list_len) and (lower_word_list[increment] != ",") and (lower_word_list[increment] != "-")):
	if (lower_word_list[increment] not in containers):
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

for i_r in ingred_repl:
	ingredient_name = ingredient_name.replace(i_r, "")
for p_r in prep_repl:
	preparation = preparation.replace(p_r, "")

# Parse ingredient to find descriptor


ingredient, ingredient_name, ingredient_name_tokens = lower_word_list, ingredient_name, ingredient_name_tokens

 

results = { 1: None, 2: None, 3: None, 4: None }
descriptor, preparation, measurement = "", "",""

ingredient_pos = nltk.pos_tag(ingredient)
ing_pos_len = len(ingredient_pos)
increment = 0

while (increment < ing_pos_len):
	if (ingredient_pos[increment][0] in ingredient_name_tokens):
		print "ingredient_pos[increment][0] is :",ingredient_pos[increment][0]
		print "ingredient_pos[increment][1] is :",ingredient_pos[increment][1]
		print "increment is :", increment
	increment+=1













