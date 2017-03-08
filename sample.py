class Recipe:
	def __init__(self, ingredients, tools, methods, step_list):
		self.ingredients = ingredients
		self.tools = tools
		self.methods = methods
		self.steps = step_list

class Step:
	def __init__(self, txt, ingredients, tools, methods, times):
		self.txt = txt
		self.ingredients = ingredients
		self.tools = tools
		self.methods = methods
		self.times = times

# Recipe 1

r1_ing = \
[{"name": "fillets salmon",
  "quantity": 4,
  "measurement": "6 ounce",
  "descriptor": "none",
  "preparation": "none"},

 {"name": "olive oil",
  "quantity": 2,
  "measurement": "tablespoon",
  "descriptor": "none",
  "preparation": "none"},

 {"name": "capers",
  "quantity": 2,
  "measurement": "tablespoon",
  "descriptor": "none",
  "preparation": "none"},

  {"name": "salt",
  "quantity": 1/8,
  "measurement": "teaspoon",
  "descriptor": "none",
  "preparation": "none"},

  {"name": "black pepper",
  "quantity": 1/8,
  "measurement": "teaspoon",
  "descriptor": "none",
  "preparation": "ground"},

  {"name": "lemon",
  "quantity": 4,
  "measurement": "none",
  "descriptor": "none",
  "preparation": "slices"}]

r1_tools = \
["skillet", "fork", "plates"]

r1_methods = ["pan-fry"]

r1_steps =  \
["Preheat a large heavy skillet over medium heat for 3 minutes.",
"Coat salmon with olive oil.",
"Place in skillet, and increase heat to high.",
"Cook for 3 minutes. Sprinkle with capers, and salt and pepper.",
"Turn salmon over, and cook for 5 minutes, or until browned.",
"Salmon is done when it flakes easily with a fork.",
"Transfer salmon to individual plates, and garnish with lemon slices."]



R1 = Recipe(r1_ing, r1_tools, r1_methods, [])

for s in r1_steps:
	step = Step(s, [], [], [], [])
	R1.steps.append(step)

R1.steps[0].ingredients = []
R1.steps[0].tools = ["skillet"]
R1.steps[0].methods = ["preheat"]
R1.steps[0].times = ["3 minutes"]

R1.steps[1].ingredients = ["salmon", "olive oil"]
R1.steps[1].tools = []
R1.steps[1].methods = ["coat"]
R1.steps[1].times = []

R1.steps[2].ingredients = []
R1.steps[2].tools = ["skillet"]
R1.steps[2].methods = ["increase heat"]
R1.steps[2].times = []

R1.steps[3].ingredients = ["capers", "salt", "pepper"]
R1.steps[3].tools = []
R1.steps[3].methods = ["cook"]
R1.steps[3].times = ["3 minutes"]

R1.steps[4].ingredients = ["salmon"]
R1.steps[4].tools = []
R1.steps[4].methods = ["turn over"]
R1.steps[4].times = ["5 minutes", "until browned"]

R1.steps[5].ingredients = ["salmon"]
R1.steps[5].tools = ["fork"]
R1.steps[5].methods = []
R1.steps[5].times = []

R1.steps[6].ingredients = ["salmon", "lemon"]
R1.steps[6].tools = ["plates"]
R1.steps[6].methods = ["transer", "garnish"]
R1.steps[6].times = []
