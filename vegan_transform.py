import nltk

non_vegetarian_ingredients = [ "beef", "veal", "lamb", "pork", "bacon", "pork belly", "ham", "ribs",
"rib", "rib tips", "rabbit", "venison", "boar", "roast", "shoulder", "sweetbread", "liver", "kidney", "tongue", 
"duck", "goose", "quail", "pheasant", "pidgeon", "squab", "chicken", "turkey", "snipe", "mutton", "steak",
"burger" ]

types_of_fish = [ "fish", "salmon", "catfish", "shrimp", "tuna", "oyster", "halibut", "fish" ]
types_of_beef = [ "beef", "steak", "rib", "brisket", "ribeye", "tenderloin", "sirloin", "filet mignon", "flank steak", "rump roast", "porterhouse" ]
types_of_poultry = [ "poultry", "chicken", "duck", "goose", "quail", "pidgeon", "squab", "turkey", "snipe" ]
types_of_pork = [ "pork", "ribs", "bacon", "pork chop", "tenderloin", "ham", "sausage", "pancetta", "prosciutto", "sausage", "chorizo" ]
types_of_protein = [ types_of_fish, types_of_pork, types_of_beef, types_of_poultry ]

non_vegan_ingredients = [ "milk", "cheese", "butter", "egg" ]

replacements = { "meat": "tofu", "poultry" : "tofu", "fish": "tempeh", "burger": "portobello mushroom", "beef": "seitan", "pork": "seitan" }

def make_vegetarian(recipe):
    new_recipe = recipe
    ingredients = recipe.FormattedIngrData
    steps = recipe.Steps
    changes = {}
    for ingredient in ingredients:
        veggie_protein = ""
        ingredient_tokens = None
        curIndex = recipe.FormattedIngrData.index(ingredient)
        curIngredient = ingredient['Ingredient']
        ingredient_tokens = nltk.word_tokenize(curIngredient)
        for token in ingredient_tokens:
            if(not_vegetarian(token)):
                if(("broth" in ingredient_tokens) or ("stock" in ingredient_tokens)):
                    new_recipe.FormattedIngrData[curIndex]['Ingredient'] = "vegetable broth"
                    new_recipe.SolelyIngrData[curIndex] = "vegetable broth"
                    changes[curIngredient] = "vegetable broth"
                else:
                    protein = protein_type(curIngredient)
                    if(protein in replacements.keys()):
                        veggie_protein = replacements[protein]
                    new_recipe.FormattedIngrData[curIndex]['Ingredient'] = veggie_protein
                    new_recipe.SolelyIngrData[curIndex] = veggie_protein
                    changes[curIngredient] = veggie_protein
    for step in steps:
        curIndex = steps.index(step)
        stepText = step.step
        new_ingredients = []
        print changes.keys()
        print step.ingredients, "\n"
        for key in changes.keys():
            while(stepText.find(key) != -1):
                stepText = stepText.replace(key, changes[key])
            new_recipe.Steps[curIndex].step = stepText
            if(new_ingredients == []):
                for ingredient in step.ingredients:
                    ingredient_sub = ""
                    if (isinstance(ingredient, list)):
                        for token in ingredient:
                            ingredient_sub += token + " "
                        ingredient_sub = ingredient_sub[0:-1]
                    else:
                        ingredient_sub = ingredient
                    if(ingredient_sub in changes.keys()):
                        new_ingredients.append(changes[ingredient_sub])
                    else:
                        new_ingredients.append(ingredient)
        new_recipe.Steps[curIndex].ingredients = new_ingredients
    return new_recipe

def not_vegetarian(ingredient):
    ingredient_tokens = nltk.word_tokenize(ingredient)
    for token in ingredient_tokens:              
        if((token in non_vegetarian_ingredients) or 
            (token in types_of_pork) or 
            (token in types_of_beef) or 
            (token in types_of_poultry) or 
            (token in types_of_fish)):
            if(("seasoning" not in ingredient_tokens) and 
                ("spice" not in ingredient_tokens)):
                return True
    return False

def protein_type(ingredient):
    ingredient_tokens = nltk.word_tokenize(ingredient)
    for token in ingredient_tokens:
        for protein_list in types_of_protein:
            if(token in protein_list):
                return protein_list[0]
    return "meat"

def make_vegan(recipe):
    new_recipe = make_vegetarian(recipe)
    return new_recipe