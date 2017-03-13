#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fat Substitutions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fat_h2l_subs = {
    'unhealthy':'healthy',
    'ground beef':'lean ground turkey',
    'bacon':'canadian bacon',
    'strips bacon': 'strips canadian bacon',
    'sausage':'lean ham',
    'chicken':'skinless chicken',
    'thigh': 'breast',
    "chicken thighs": "chicken breasts",
    "chicken thigh": "chicken breast",
    'turkey':'skinless turkey',
    "turkey breast": "turkey thigh",
    "turkey breasts": "turkey thighs",
    'duck':'skinless turkey',
    'goose':'skinless turkey',
    'beef' :'beef loin',
    'beef chuck':'beef loin',
    'beef rib':'beef loin',
    'beef brisket':'beef loin',
    'pork spareribs':'pork tenderloin',
    'chorizo sausage':'turkey sausage',
    'whole milk': "skim milk",
    'milk':'skim milk',
    'cream':'evaporated skim milk',
    'iceberg lettuce':'arugula',
    'butter':'cooking spray',
    'margarine':'olive oil',
    'cheddar cheese': "low-fat cheddar cheese",
    'mozzerella cheese': "low-fat mozzerella cheese",
    'american cheese': "low-fat american cheese",
    'cottage cheese': 'low-fat cottage cheese',
    'vegetable oil':'olive oil',
    'shortening':'fat-free margarine',
    'soy sauce':'low-sodium soy sauce',
    'alfredo':'marinara',
    'pasta':'whole wheat pasta',
    'sour cream':'plain Greek yogurt',
    'bread':'pita',
    'flour tortilla':'corn tortilla',
    'white bread':'whole wheat bread',
    'bread' : 'whole wheat bread',
    'mayonnaise':'Greek yogurt',
    'eggs':'egg whites',
    'cream cheese':'fat-free ricotta cheese',
    'white rice':'brown rice', 
    'salted' : 'unsalted'
}

fat_l2h_subs = {v: k for k, v in fat_h2l_subs.iteritems()}
fat_l2h_subs['skim milk'] = 'whole milk'
fat_l2h_subs['low-fat milk'] = "whole milk"
fat_l2h_subs['low fat milk'] = 'whole milk'
fat_l2h_subs['milk'] = 'whole milk'
fat_l2h_subs['wheat bread'] = 'white bread'
fat_l2h_subs['bread'] = 'white bread'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fat Transformation Code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def high2low_fat_transform(Recipe):
    new_recipe = Recipe.clone()
    for ing in new_recipe.FormattedIngrData:
        if ing["Ingredient"] in fat_h2l_subs.keys():
            ing["Ingredient"] = fat_h2l_subs[ing["Ingredient"]]

    old_data = new_recipe.SolelyIngrData
    new_data = new_recipe.SolelyIngrData

    for ing in new_data:
        if ing in fat_h2l_subs.keys():
            ing = fat_h2l_subs[ing]

    for step in new_recipe.Steps:
        for ing in old_data:
            if ing in step.step:
                if ing in fat_h2l_subs.keys():
                    step.step = step.step.replace(ing, fat_h2l_subs[ing])

    new_recipe.SolelyIngrData = new_recipe.extractSolelyIngrData()
    

    for i in range(len(new_recipe.RawIngrData)):
        for ing in old_data:
            if ing in new_recipe.RawIngrData[i]:
                if ing in fat_h2l_subs.keys():
                    new_recipe.RawIngrData[i] = new_recipe.RawIngrData[i].replace(ing, fat_h2l_subs[ing])

    return new_recipe


def low2high_fat_transform(Recipe):
    new_recipe = Recipe.clone()
    for ing in new_recipe.FormattedIngrData:
        if ing["Ingredient"] in fat_l2h_subs.keys():
            ing["Ingredient"] = fat_l2h_subs[ing["Ingredient"]]

    old_data = new_recipe.SolelyIngrData
    new_data = new_recipe.SolelyIngrData

    for ing in new_data:
        if ing in fat_l2h_subs.keys():
            ing = fat_l2h_subs[ing]

    for step in new_recipe.Steps:
        for ing in old_data:
            if ing in step.step:
                if ing in fat_l2h_subs.keys():
                    step.step = step.step.replace(ing, fat_l2h_subs[ing])

    new_recipe.SolelyIngrData = new_recipe.extractSolelyIngrData()
    

    for i in range(len(new_recipe.RawIngrData)):
        for ing in old_data:
            if ing in new_recipe.RawIngrData[i]:
                if ing in fat_l2h_subs.keys():
                    new_recipe.RawIngrData[i] = new_recipe.RawIngrData[i].replace(ing, fat_l2h_subs[ing])


    return new_recipe