#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fat Substitutions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fat_h2l_subs = {
    'unhealthy':'healthy',
    'ground beef':'lean ground turkey',
    'bacon':'canadian bacon',
    'sausage':'lean ham',
    'chicken':'skinless chicken',
    'thigh': 'breast',
    "chicken thighs": "chicken breasts",
    "chicken thigh": "chicken breast",
    'turkey':'skinless turkey',
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


#low_to_high_stopwords = {"whole wheat": "", "wheat": "", "low-fat": "", "low fat": "", "healthy": "", "1%": "", '2%': "", ',': "", "canadian-style": "canadian", "extra-virgin": "", "extra virgin": ""}
#high_to_low_stopwords = ["whole", "full-fat", "1%", '2%', ',', 'with skin', "canadian-style", "canadian", "white", "softened"]


#ignorelist = ["buttermilk"]

method_subs_h2l = 
{
    'deep-fryer': 'oven',
    'fryer': 'oven',
    'fry':'bake',
    'fried': 'baked',
    'frying pan': 'oven',
    'boil':'steam',
    'deep-fry':'bake',
    'pan fry':'bake'
}

method_subs_l2h = 
{
    "oven": "deep-fryer",
    "bake": "fry",
    "baked": "fried",
    "steam": "fry"
}

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
            if ing in step:
                step = step.replace(ing, fat_h2l_subs[ing])


def low2high_fat_transform(Recipe):