#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Carb Substitutions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

carb_h2l_subs = {

    'sliced bread': 'eggplant',
	'bread':'wheat bread',
	'pasta':'wheat pasta',
    'sweet potatoes': 'zucchini',
    'sweet potato': 'zucchini',
	'linguine': 'whole wheat linguine',
    'spaghetti': 'whole what spaghetti',
	'penne': 'whole wheat penne',
	'fettuccine': 'whole wheat fettuccine',
    'farfalle' : 'whole wheat farfalle',
	'buns' : 'portabello mushroom buns',
	'bun' : 'portabello mushroom bun',
	'potato chips' : 'kale',
	'potato' : 'zucchini',
    'chips': 'kale',
	'potatoes' : 'zucchini',
	'spaghetti' : 'spaghetti squash',
	'french fries': 'butternut squash fries',
	'pancakes' : 'almond flour pancakes',
	'flour' : 'almond flour',
	'pizza crust' : 'cauliflower crust',
	'taco shells' : 'lettuce wraps',
    'taco shell' : 'lettuce wrap',
	'flour tortillas' : 'corn tortillas',
    'flour tortilla' : 'corn tortilla',
	'rice' : 'quinoa',
    'cereal': 'oats',
    'crackers': 'cucumber slices',
    'beans': 'soy beans',
    'milk': 'unsweetened almond milk',
    'sugar': 'artificial sweetener',
    'jam': 'fresh fruit',
    'jelly': 'fresh fruit',
    'candy': 'sugar-free candy',
    'pasta sauce': 'almond pesto',
    'hash browns': 'squash',
    'noodles': 'zuchinni slices',
    'elbow macaroni': 'diced vegetables',
    'macaroni': 'diced vegetables',
    'bananas': 'strawberries',
    'beets': 'carrots',
    'chickpeas': 'soy beans',
    'garbonzo beans': 'soy beans'
}

carb_l2h_subs = {v: k for k, v in carb_h2l_subs.iteritems()}
carb_l2h_subs["wheat bread"] = 'white bread'
carb_l2h_subs["bread"] = 'white bread'



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Carb Transformation Code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def high2low_carb_transform(Recipe):
    new_recipe = Recipe.clone()
    for ing in new_recipe.FormattedIngrData:
        if ing["Ingredient"] in carb_h2l_subs.keys():
            ing["Ingredient"] = carb_h2l_subs[ing["Ingredient"]]

    old_data = new_recipe.SolelyIngrData
    new_data = new_recipe.SolelyIngrData

    for ing in new_data:
        if ing in carb_h2l_subs.keys():
            ing = carb_h2l_subs[ing]

    for step in new_recipe.Steps:
        for ing in old_data:
            if ing in step.step:
                if ing in carb_h2l_subs.keys():
                    step.step = step.step.replace(ing, carb_h2l_subs[ing])

    new_recipe.SolelyIngrData = new_recipe.extractSolelyIngrData()
    

    for i in range(len(new_recipe.RawIngrData)):
        for ing in old_data:
            if ing in new_recipe.RawIngrData[i]:
                if ing in carb_h2l_subs.keys():
                    new_recipe.RawIngrData[i] = new_recipe.RawIngrData[i].replace(ing, carb_h2l_subs[ing])

    return new_recipe


def low2high_carb_transform(Recipe):
    new_recipe = Recipe.clone()
    for ing in new_recipe.FormattedIngrData:
        if ing["Ingredient"] in carb_l2h_subs.keys():
            ing["Ingredient"] = carb_l2h_subs[ing["Ingredient"]]

    old_data = new_recipe.SolelyIngrData
    new_data = new_recipe.SolelyIngrData

    for ing in new_data:
        if ing in carb_l2h_subs.keys():
            ing = carb_l2h_subs[ing]

    for step in new_recipe.Steps:
        for ing in old_data:
            if ing in step.step:
                if ing in carb_l2h_subs.keys():
                    step.step = step.step.replace(ing, carb_l2h_subs[ing])

    new_recipe.SolelyIngrData = new_recipe.extractSolelyIngrData()
    

    for i in range(len(new_recipe.RawIngrData)):
        for ing in old_data:
            if ing in new_recipe.RawIngrData[i]:
                if ing in carb_l2h_subs.keys():
                    new_recipe.RawIngrData[i] = new_recipe.RawIngrData[i].replace(ing, carb_l2h_subs[ing])


    return new_recipe