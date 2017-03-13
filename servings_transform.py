import copy
def change_servings(inp_servings, recipe):	
	# new_recipe = copy.deepcopy(recipe)
	new_recipe = recipe.clone()

	ingredients = new_recipe.FormattedIngrData
	steps = new_recipe.Steps
	servings = int(new_recipe.Servings)
	factor = float(inp_servings)/servings

	ingredients = changeIngredientSize(ingredients, factor)
	steps = changeStepsTimes(steps, factor)

	new_recipe.FormattedIngrData = ingredients
	new_recipe.Steps = steps

	return new_recipe

def changeIngredientSize(ingredients, factor):
	for i in range(len(ingredients)):
		ingredient = ingredients[i]
		measurement_val = extractQtyFromMeasurementAttribute(ingredient["Measurement"])
		quantity_val = extractQtyFromQuantityAttribute(ingredient["Quantity"])
		if(quantity_val!=None):
			ingredients[i]["Quantity"] = str(quantity_val*factor)
		elif(measurement_val!=None):
			ingredients[i]["Measurement"].replace(str(measurement_val), str(measurement_val*factor))
	return ingredients

def changeStepsTimes(steps, factor):
	ret_arr = copy.deepcopy(steps)
	for i in range(len(steps)):
		step = steps[i].step
		new_step = step
		indices = [x for x in range(len(step)) if (step[x].isdigit() or (step[x]=="."))]
		if(len(indices)==0):
			continue
		elif(len(indices)==1):
			if(step[indices[0]]=="."):
				continue
			else:
				new_val = float(step[indices[0]])*factor
				new_step = step[:indices[0]]+str(new_val)+step[indices[0]+1:]
		else:
			first_num = []
			iterator = 0

			while( (len(indices)>(iterator+1)) and (indices[iterator+1]==(1+indices[iterator]))):
				iterator+=1

			first_num.append(step[indices[0]:indices[iterator]+1])

			if(iterator!=(len(indices)-1)):
				second_num = []

				iterator2=iterator+1
				start = iterator2
				while( (len(indices)>(iterator2+1)) and (indices[iterator2+1]==(1+indices[iterator2]))):
					iterator2+=1

				if((iterator2+1)==(len(indices))):
					second_num.append(step[indices[iterator2]])
				else:
					second_num.append(step[indices[start]:indices[iterator2]+1])

				if(first_num[0]!=""):
					first_num_float = float(first_num[0])
					desired_first_num = first_num_float*factor
				if((second_num[0]!="") and (second_num[0]!=".")):
					second_num_float = float(second_num[0])
					desired_second_num = second_num_float*factor
				if((first_num[0]!="") and ((second_num[0]!="") and (second_num[0]!="."))):
					new_step = step[:indices[0]]+str(desired_first_num) + step[indices[iterator]+1:indices[iterator+1]] + str(desired_second_num) + step[indices[iterator2]+1:]
				elif(first_num[0]!=""):
					new_step = step[:indices[0]]+str(desired_first_num) + step[indices[iterator]+1:]

			else:
				if(first_num[0]!=""):
					first_num_float = float(first_num[0])
					desired_first_num = first_num_float*factor
					new_step = step[:indices[0]]+str(desired_first_num) + step[indices[iterator]+1:]
		ret_arr[i].step = new_step
	return ret_arr

def extractQtyFromMeasurementAttribute(attribute):
	if(attribute==None):
		return None
	else:	
		string_rep = ''.join([char for char in attribute if ( (char.isdigit()) or (char==".") or (char=="/"))])
		if(string_rep):
			if("/" in string_rep):
				n1, n2 = map(int, string_rep.split('/'))
				return float(n1)/float(n2)
			else:
				return float(string_rep)
	return None

def extractQtyFromQuantityAttribute(attribute):
	#This function can be used BOTH on Measurement & on Quantity
	if(attribute==None):
		return None
	if(" " in attribute):
		whole_num, frac = attribute.split(" ")
		whole_num = extractQtyFromAttribute(whole_num)
		frac = extractQtyFromAttribute(frac)
		return float(whole_num)+float(frac)
	else:	
		string_rep = ''.join([char for char in attribute if ( (char.isdigit()) or (char==".") or (char=="/"))])
		if(string_rep):
			if("/" in string_rep):
				n1, n2 = map(int, string_rep.split('/'))
				return float(n1)/float(n2)
			else:
				return float(string_rep)
	return None


def updateRecipeObject(recipe):
	updateRecipe(recipe)
	updateSteps(recipe.Steps)

def updateSteps(Steps):
	for i in len(range(Steps)):
		Steps[i].lower_step = Steps[i].step.lower()
		Steps[i].lower_step_toks = nltk.word_tokenize(Steps[i].lower_step)
		Steps[i].lower_step_pos = nltk.pos_tag(Steps[i].lower_step_toks)
		Steps[i].ExtractFromTxt()