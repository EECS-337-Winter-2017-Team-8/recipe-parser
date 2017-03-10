class Step:
	#Note that this class requires acces to the global variables defined in directions.py AND ingredients.py

	def __init__(self, txt, SolelyIngrData):
		#~~~~~~~~~~~~~~~~~~~~~~~~~ The final values we will return ~~~~~~~~~~~~~~~~~~~~~~~~~
		self.ingredients = None
		self.tools = None
		self.methods = None
		self.times = None

		#~~~~~~~~~~~~~~~~~~~~~~~~~ Intermediary Variables for calculation purposes ~~~~~~~~~~~~~~~~~~~~~~~~~
		self.step = txt
		self.lower_step = txt.lower()
		self.lower_step_toks = nltk.word_tokenize(self.lower_step)
		self.lower_step_pos = nltk.pos_tag(self.lower_step_toks)

		self.recipeIngrData = SolelyIngrData #This is only the Ingredient attribute of the ingredients.
		self.recipeIngrTokens = map(lambda(x): nltk.word_tokenize(x), recipe_ingrs_extracted)
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interface ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def ExtractFromTxt(self):
		m1,t1,i1 = self.firstWordAnalysis()
		m2,t2,i2 = self.splitAnalysis()

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Non-Interface/Behind The Scenes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	#~~~~~~ Main Methods ~~~~~~
	def firstWordAnalysis(self, inpText=None):
		#We have inpText attribute because we do recursion in event of "("
		if(inpText!=None):
			lower_step_tokens = nltk.word_tokenize(inpText.lower())
			lower_step_pos = nltk.pos_tag(lower_step_tokens)
		else:
			lower_step_tokens = self.lower_step_toks
			lower_step_pos = self.lower_step_pos

		recipe_ingrs_extracted_tokens = self.recipeIngrTokens

		method, tool, ingredient = None, None, None
		fw = lower_step_tokens[0]
		if(fw == "("):
			#In the event of this
			return self.firstWordAnalysis(lower_step[lower_step.index(")")+1:])
		
		elif (fw in dirn_methods):
			# If it is a verb
			method = fw
			in_a_index = self.findConsecutiveWords(["in", "a"], lower_step_tokens)
			if(in_a_index):
				tool = self.getAdjacentTool(in_a_index+2, lower_step_tokens, lower_step_pos)
				ingr, iterator = None, 1
				while(iterator<in_a_index):
					ingr = self.getAdjacentIngredient(iterator, lower_step_tokens, lower_step_pos)
					if(ingr!=None):
						iterator+=len(ingr)
				if(ingr!=None):
					ingredient = ingr
			else:
				iterator = 1
				if(recipe_ingrs_extracted_tokens!=None):
					ingr = self.getAdjacentIngredient(1, lower_step_tokens, lower_step_pos)
					if(ingr==None):
						tool = self.getAdjacentTool(iterator, lower_step_tokens, lower_step_pos)
					else:
						ingredient = ingr

		elif (fw == "in"):
			#Functionality works! 
			iterator = 1
			tool, iterator = self.getAdjacentTool(iterator, lower_step_tokens, lower_step_pos, retIterator=True)
			if( (tool==None) or (iterator==None) ): iterator = 1

			# Check for "over ____ heat"
			if((lower_step_tokens[iterator] == "over") and (lower_step_tokens[iterator+2] == "heat")):
				iterator+=3
				
			#Get the method name. Checks for commas mainly.
			while(lower_step_tokens[iterator] not in dirn_methods):
				iterator+=1

			method = lower_step_tokens[iterator]
			
		elif ( (lower_step_pos[0][1]=="RB") and (lower_step_tokens[0] not in dirn_bad_adverbs)) :
			# if slowly, lightly, generously, lightly
			method, tool = self.firstWordAdverb(lower_step, lower_step_tokens, lower_step_pos)

		else: 
			ingredient = self.getAdjacentIngredient(0)

		return method, tool, ingredient

	def splitAnalysis(self):
		lower_step = self.lower_step
		lower_step_list = self.splitForSplitAnalysis()
		methods, tools, ingredients = [],[],[]
		for splitted_elt in lower_step_list:
			if(len(splitted_elt)==0):
				continue
			method, tool, ingr = None, None, None
			lower_step_tokens = nltk.word_tokenize(splitted_elt)
			lower_step_pos = nltk.pos_tag(lower_step_tokens)
			tool = getAdjacentTool(0, lower_step_tokens, lower_step_pos)
			if(lower_step_tokens[0] in dirn_methods):
				method = lower_step_tokens[0]
				ingr = getAdjacentIngredient(lower_step_tokens, 1, recipe_ingrs_extracted_toks)
			else:
				ingr = getAdjacentIngredient(lower_step_tokens, 0, recipe_ingrs_extracted_toks)
			if((tool) and (method==tool)):
				#Then we are trying to declare the same thing twice.
				print "In splitted_elt = \"", splitted_elt, "\", we come across tool:", tool, " = elt: \" ", elt, " \" \n"
			if(tool!=None): tools += (tool)
			if(ingr!=None):
				if (len(ingr)>1): ingredients.append(ingr)
				else: ingredients+=ingr
			if(method!=None): methods.append(method)
		return methods, tools, ingredients
	
	#~~~~~~ Get Methods ~~~~~~
	def getAdjacentTool(self, index, inp_lower_step_toks = None, inp_lower_step_pos = None, retIterator=False):
		#checks if there is a tool starting from that index
		iterator, tool = index, None
		if(inp_lower_step_toks):
			lower_step_tokens, lower_step_pos = inp_lower_step_toks, inp_lower_step_pos
		else:
			lower_step_tokens, lower_step_pos = self.lower_step_toks, self.lower_step_pos

		#remove "determiners" such as 'a'
		while( (iterator<len(lower_step_pos)) and (lower_step_pos[iterator][1]=='DT')):
			iterator+=1

		start = iterator
		if(iterator==len(lower_step_pos)):
			if(retIterator):
				return None, None
			else:
				return None

		#While the next_word is compatible but not a tool, we continue onwards.
		while ((lower_step_tokens[iterator] in dirn_measurements) or (lower_step_tokens[iterator] in dirn_descriptors) 
		  or (bool(filter(lambda(x): x.isdigit(), lower_step_tokens[iterator])))):
			iterator+=1

		#To ensure accuraccy some more
		if(lower_step_tokens[iterator] in dirn_tools):
			#In event we have "grill grate" or something.
			while((iterator<len(lower_step_tokens)) and (lower_step_tokens[iterator] in dirn_tools)):
				iterator+=1

			next_tool, next_iterator = None, None

			if((iterator<len(lower_step_tokens)) and (lower_step_tokens[iterator]=="or")):
				next_tool, next_iterator = getAdjacentTool(iterator+1, lower_step_tokens, lower_step_pos, retIterator=True)

			if(next_iterator!=None):
				iterator = next_iterator
				tool = lower_step_tokens[start:iterator]
			else:
				tool = lower_step_tokens[start:iterator]

			if(retIterator):
				return tool, iterator
			else:
				return tool

		if(retIterator):
			return None, None
		else:
			return None

	def getAdjacentIngredient(self, index, inp_lower_step_toks = None, inp_lower_step_pos = None):
		#Function returns  adjacent ingredients or Nothing at all.
		if(inp_lower_step_toks):
			lower_step_tokens = inp_lower_step_toks
			lower_step_pos = inp_lower_step_pos
		else:
			lower_step_tokens = self.lower_step_toks
			lower_step_pos = self.lower_step_pos
		
		recipe_ingrs_extracted_tokens = self.recipeIngrTokens

		iterator = index

		while( (iterator<len(lower_step_tokens)) and ((lower_step_pos[iterator][1] in ["DT", "CD"]) or (lower_step_tokens[iterator] in ing_measurements) or (lower_step_tokens[iterator] in ing_descriptors) 
		  or (bool(filter(lambda(x): x.isdigit(), lower_step_tokens[iterator]))))):
			iterator+=1

		if(iterator==len(lower_step_tokens)):
			return None

		susp_ingr  = lower_step_tokens[iterator]
		for ingr_token in recipe_ingrs_extracted_tokens:
			#The tokens of 1 ingredient 
			if(susp_ingr in ingr_token):
				len_ingr_token = len(ingr_token)
				iterator_fwd, iterator_bwd = None, None
				if(len_ingr_token>1):
					token_index = ingr_token.index(susp_ingr)
					len_step_tokens = len(lower_step_tokens)

					if(token_index==0): 
						#if suspected ingredient is found at the start of the token, check if there is a match w the next one
						iterator_fwd = 1
						while( (len_step_tokens > (token_index+iterator_fwd) ) and ( lower_step_tokens[token_index+iterator_fwd] in ingr_token) ):
							iterator_fwd+=1
						iterator_fwd-=1

					elif(token_index == (len_step_tokens-1) ): 
						#if suspected ingredient is found at the end of the token, check if there is a match w the previous one
						iterator_bwd = -1
						while( (len_step_tokens > (token_index+iterator_bwd) ) and ( lower_step_tokens[token_index+iterator_bwd] in ingr_token) ):
							iterator_bwd-=1
						iterator_bwd+=1

					else:
						#may be a chance that it is before OR after.
						iterator_fwd, iterator_bwd = 1, -1
						while( (len_step_tokens > (token_index+iterator_fwd) ) and ( lower_step_tokens[token_index+iterator_fwd] in ingr_token) ):
							iterator_fwd+=1
						
						while( ( (token_index+iterator_bwd) >= 0 ) and ( lower_step_tokens[token_index+iterator_bwd] in ingr_token) ):
							iterator_bwd-=1
						
						#Just to undo the offset
						iterator_fwd-=1
						iterator_bwd+=1

				if((iterator_fwd!=None) and (iterator_bwd!=None)):
					return lower_step_tokens[iterator+iterator_bwd : iterator+iterator_fwd+1]
				elif(iterator_fwd):
					return lower_step_tokens[iterator: iterator+iterator_fwd+1]
				elif(iterator_bwd):
					return lower_step_tokens[iterator+iterator_bwd : iterator]
				else:
					return [lower_step_tokens[iterator]]
			else:
				continue
		return None

	#~~~~~~ Other Methods ~~~~~~
	def firstWordAdverb(self, inp_lower_step = None, inp_lower_step_toks = None, inp_lower_step_pos = None):
		#Call this function when the firstWord is an Adverb.
		#It will extract METHOD & TOOL.
		#If it can't find either, it will return None in their place
		if(inp_lower_step):
			lower_step = inp_lower_step
			lower_step_tokens = inp_lower_step_toks
			lower_step_pos = inp_lower_step_pos
		else:
			lower_step = self.lower_step
			lower_step_tokens = self.lower_step_toks
			lower_step_pos = self.lower_step_pos

		if(lower_step_tokens[1] in dirn_methods): 
			method = lower_step_tokens[1] #Should always be the case
			iterator = 2
			tool = getAdjacentTool(iterator, lower_step_tokens, lower_step_pos)
			return method, tool
		else:
			print "FAILED lower_step is: ", lower_step
			raise ValueError('Adverb wasnt followed by a method!', lower_step)

	#~~~~~~ Utility Functions ~~~~~~
	def findConsecutiveWords(self, lower_arr_words, lower_arr_tokens):
		#returns the index of the first of the consecutive word block, or None if it is absent
		length_words = len(lower_arr_words)
		for i in range(len(lower_arr_tokens)-length_words):
			if(lower_arr_tokens[i:i+length_words] == lower_arr_words):
				return i
		return None

	def splitForSplitAnalysis(self):
		lower_step = self.lower_step
		lower_step_list = [lower_step]
		for split_tok in dirn_split_toks:
			for i in lower_step_list:
				toks = nltk.word_tokenize(i)
				if split_tok in toks:
					lower_step_list+=map(str.strip, i.split(split_tok))
					lower_step_list.remove(i)
		return lower_step_list


