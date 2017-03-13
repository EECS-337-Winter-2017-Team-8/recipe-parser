from ingredients import *
from directions import *
from StepClass import *

class Recipe:
    #Note that this class requires acces to the global variables defined in ingredients.py

    def __init__(self, unparsed_recipe):
        self.unparsed_recipe = unparsed_recipe
        #self.FormattedIngrData = None
        #List of breakdown of Steps; data from "Directions" Section
        self.FormattedDirnData = None
        #List of Tools Needed for Recipe; data from "Directions" Section
        self.FormattedToolsData = None
        #List of Methods Needed for Recipe; data from "Directions" Section
        self.FormattedMethodsData = None

        self.PrimaryMethods = None
        self.SecondaryMethods = None
        if(self.unparsed_recipe.servings!=None):
            self.Servings = self.unparsed_recipe.servings
        else:
            self.Servings = None

        #~~~~~~~~~~~~~~~~~~~~~~~~~ Intermediary Variables for calculation purposes ~~~~~~~~~~~~~~~~~~~~~~~~~
        self.RawIngrData = self.unparsed_recipe.ingredients
        self.RawDirnData = self.unparsed_recipe.directions

        self.FormattedIngrData = self.parse_ingredients()
        self.SolelyIngrData = self.extractSolelyIngrData()
        self.Steps = self.extractSteps()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interface ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #~~~~~~~~~~~~~~~~~~~~~~~~~ Input ~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_ingredients(self):
        return [self.parse_ingredient(ingredient)
                for ingredient in self.unparsed_recipe.ingredients]

    #~~~~~~~~~~~~~~~~~~~~~~~~~ Analyze ~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~ Ingredients ~~~~~~~~~~~~
    #We provide optional data & store parameters in next 2 funxns to allow us to test the functionality.

    def extractSolelyIngrData(self, data=None, store=False):
        #Extracts only the 'Ingredient' elements within the entire ingredient dictionary...
        val = None

        if(self.FormattedIngrData!=None):
            val = [ frm_ingr['Ingredient'] for frm_ingr in self.FormattedIngrData]
        elif (data != None):
            val = self.getRecipeIngredientsAttributes(data)

        return val

    #~~~~~~~~~~~~ Directions ~~~~~~~~~~~~
    def extractSteps(self, data=None, store=False):
        # Finds all of the steps in the data paramater (or, if that is not given, the RawDirnData).
        # Creates a Step object for every one of them, and if store==True, stores it in self.Steps
        val = None
        ret_arr = []

        if(data):
            val = getSteps(data)
        else:
            val = getSteps(self.RawDirnData)

        if(val):
            ret_arr = [Step(step, self.SolelyIngrData) for step in val]

        return ret_arr

    def categorizeMethods(self, data=None, store=False):
        primary_methods = []
        secondary_methods = []
        for step in self.Steps:
            for method in step.methods:
                if ((method in dirn_primary_methods) and (method not in primary_methods)):
                    primary_methods.append(method)
                else:
                    secondary_methods.append(method)
        if(store==True):
            self.PrimaryMethods = primary_methods
            self.SecondaryMethods = secondary_methods

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Non-Interface/Behind The Scenes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #~~~~~~~~~~~~~~~~~~~~~~~~~ Ingredient Functionality ~~~~~~~~~~~~~~~~~~~~~~~~~
    def parse_ingredient (self, ingredient):
        #Initialize list of tokens
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

    def remove_token(ingredient_name, token):
        ingredient_name = ingredient_name.replace(" " + token + " ", "")
        ingredient_name = ingredient_name.replace(" " + token, "")
        ingredient_name = ingredient_name.replace(token + " ", "")
        ingredient_name = ingredient_name.replace(token, "")
        return ingredient_name

    def parse_ing_name(self, ingredient, ingredient_name, ingredient_name_tokens):
        results = { 1: None, 2: None, 3: None, 4: None }
        descriptor, preparation, measurement = "", "",""


        ingredient_pos_tags = nltk.pos_tag(ingredient)
        ing_pos_len = len(ingredient_parts_of_speech)
        increment = 0

        while (increment < ing_pos_len):
            ingredient_pos_tag = ingredient_pos_tags[increment]

            token = ingredient_pos_tag[0]
            token_pos = token_pos_tag[1]

            if (token in ingredient_name_tokens):
                if ((token_pos == 'VBN')
                    or (token in ing_descriptors)
                    or (token.find("less") != -1)):

                        #verb, past participle. Used w/ Auxillary version of has
                        #he HAS ridden. he HAS eaten. he HAS rowed the boat.
                        if (descriptor != ""):
                                descriptor += " "
                                descriptor += token
                                ingredient_name = remove_token(ingredient_name, token)

                elif ((token_pos == 'VBD') or (token_pos == 'RB')):
                    #VBD past tense Verb: dipped, pleased, swiped, adopted, strode, wore
                    #RB averb. occassionally, professionally, maddeningly, swiftly, quickly
                    if (preparation != ""):
                        preparation += " " + token
                    else:
                        preparation = token
                    ingredient_name = remove_token(ingredient_name, token)

                elif (token in ing_measurements):
                    measurement += token
                    ingredient_name = remove_token(ingredient_name, token)

                elif (token == "("):
                    ingredient_name = remove_token(ingredient_name, token)
                    increment += 1
                    if (descriptor != ""):
                        descriptor += " ; "
                    while ((increment < ing_pos_len) and (token != ")")):
                        if (descriptor != ""):
                            descriptor += " "
                        descriptor += token
                        ingredient_name = remove_token(ingredient_name, token)
                        increment += 1
                    ingredient_name = remove_token(ingredient_name, token)

                elif ((token == "CC") and (token != "and")):
                    #CC: Conjunction, coordinating. 
                    #and both but either et for less minus neither nor or plus so therefore times yet whether
                    ingredient_name = remove_token(ingredient_name, token)

                elif (token == "-"):
                    ingredient_name = remove_token(ingredient_name, token)
                    increment += 1
                    while (increment < ing_pos_len):
                        if (preparation != ""):
                            preparation += " "
                        preparation += token
                        ingredient_name = remove_token(ingredient_name, token)
                        increment += 1

            increment += 1

        results[1] = ingredient_name
        results[2] = descriptor
        results[3] = preparation
        results[4] = measurement
        return results

    def getRecipeIngredientsAttributes(self, recipe_ingrs_raw):
        recipe_ingrs_formatted = []
        for ingr in recipe_ingrs_raw:
            ingr_formatted = parse_ingredient(ingr)
            recipe_ingrs_formatted.append(ingr_formatted)
        recipe_ingrs_extracted = [recipe["Ingredient"] for recipe in recipe_ingrs_formatted]
        return recipe_ingrs_extracted

    #~~~~~~~~~~~~~~~~~~~~~~~~~ Input ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def clone(self):
        clone = Recipe(copy.deepcopy(self.unparsed_recipe))
        clone.FormattedDirnData = copy.deepcopy(self.FormattedDirnData)
        clone.FormattedToolsData = copy.deepcopy(self.FormattedToolsData)
        clone.FormattedMethodsData = copy.deepcopy(self.FormattedMethodsData)
        clone.PrimaryMethods = copy.deepcopy(self.PrimaryMethods)
        clone.SecondaryMethods = copy.deepcopy(self.SecondaryMethods)
        clone.Servings = copy.deepcopy(self.Servings)
        clone.RawIngrData = copy.deepcopy(self.RawIngrData)
        clone.RawDirnData = copy.deepcopy(self.RawDirnData)
        clone.FormattedIngrData = copy.deepcopy(self.FormattedIngrData)
        clone.SolelyIngrData = copy.deepcopy(self.SolelyIngrData)
        clone.Steps = copy.deepcopy(self.Steps)
        return clone

    def print_recipe(self):
        print "\n~~~~~" + self.unparsed_recipe.title + "~~~~~"
        print "~~~~~INGREDIENTS~~~~~\n"
        for ing in self.RawIngrData:
            print ing

        print "\n~~~~~DIRECTIONS~~~~~\n"

        for step in self.Steps:
            print step.step


    def transform(self, transformation):
        if transformation == 1:
            print "Hi from", 1
        elif transformation == 2:
            print "Hi from", 2
        elif transformation == 3:
            print "Hi from", 3
        elif transformation == 4:
            print "Hi from", 4
        elif transformation == 5:
            print "Hi from", 5
        elif transformation == 6:
            print "Hi from", 6
