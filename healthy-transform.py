bad_ingredients = ["salt", "oil", "butter", "bacon", "sugar", "lard", "grease"]

def make_healthy(recipe):
    ingredients = recipe.SolelyIngrData
    for ingredient in bad_ingredients:
        ingredients = reduce_ingredient(ingredients, ingredient["name"], 2)

def reduce_ingredient(ingredients, ingredient_name, factor):
    new_ingredients = {ingredient: ingredients[ingredient] for ingredient in ingredients}
    for ingredient in ingredients:
        if ingredient["name"] == ingredient_name:
            ingredient["quantity"] = float(ingredient["quantity"]) / factor
    return new_ingredients
