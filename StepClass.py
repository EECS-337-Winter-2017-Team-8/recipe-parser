from directions import *
from ingredients import *
import pattern.en

class Step:
	#Note that this class requires acces to the global variables defined in directions.py AND ingredients.py

	def __init__(self, txt, SolelyIngrData):
		#~~~~~~~~~~~~~~~~~~~~~~~~~ The final values we will return ~~~~~~~~~~~~~~~~~~~~~~~~~
		self.ingredients = None
		self.tools = None
		self.methods = None
		self.times = None
		self.concreteTime = None
		self.untilTime = None

		#~~~~~~~~~~~~~~~~~~~~~~~~~ Intermediary Variables for calculation purposes ~~~~~~~~~~~~~~~~~~~~~~~~~
		self.step = txt
		self.lower_step = txt.lower()
		self.lower_step_toks = nltk.word_tokenize(self.lower_step)
		self.lower_step_pos = nltk.pos_tag(self.lower_step_toks)

		self.recipeIngrData = SolelyIngrData #This is only the Ingredient attribute of the ingredients.
		self.recipeIngrTokens = map(lambda(x): nltk.word_tokenize(x), SolelyIngrData)
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Interface ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def ExtractFromTxt(self, Display=False):
		meth1,tool1,ingr1 = self.firstWordAnalysis()
		meth2,tool2,ingr2 = self.splitAnalysis()

		time = None
		ConcrTime = self.getConcreteTime()
		UntilTime = self.getUntilTime()

		if(ConcrTime and UntilTime):
			time = ConcrTime+" or " + UntilTime
			self.concreteTime = ConcrTime
			self.untilTime = UntilTime
		elif(ConcrTime):
			time = ConcrTime
			self.concreteTime = ConcrTime
		elif(UntilTime):
			time = UntilTime
			self.untilTime = UntilTime

		if(len(meth1)==0):
			meth_combined = meth2
		elif(len(meth1)==1):
			meth_combined = meth2
			if(meth1[0] not in meth_combined):
				meth_combined.append(meth1[0])
		else:
			if(meth1 in meth2):
				meth_combined = meth2
			else:
				meth_combined = meth2
				meth_combined.append(meth1)

		if(len(tool1)==0):
			if(len(tool2)>1):
				tool_combined = [tool2]
			else:
				tool_combined = tool2
		elif(len(tool1)==1):
			if(tool1[0] in tool2):
				tool_combined = tool2
			else:
				tool_combined = tool2
				tool_combined.append(tool1[0])
		else: #len(ingr1)>1
			if(tool1!=tool2):
				if((tool1 in tool2) or ([tool1] in tool2) or ([tool1] in [tool2])):
					tool_combined = tool2
				else:
					tool_combined = tool2
					tool_combined.append(tool1)
			else:
				if(len(tool2)>1):
					tool_combined = [tool2]
				else:
					tool_combined = tool2

		if( (ingr1==None) or (len(ingr1)==0)):
			ingr_combined = ingr2
		elif(len(ingr1)==1):
			if( (ingr2 != None) and (ingr1[0] in ingr2)):
				ingr_combined = ingr2
			else:
				if(ingr2!=None):
					ingr_combined = ingr2
					ingr_combined.append(ingr1[0])
				else:
					ingr_combined = [ingr1[0]]
		else: #len(ingr1)>1
			if(ingr2!=None):
				if(ingr1 in ingr2):
					ingr_combined = ingr2
				else:
					ingr_combined = ingr2
					ingr_combined.append(ingr1)
			else:
				ingr_combined = ingr1

		self.methods = meth_combined
		self.tools = tool_combined
		self.ingredients = ingr_combined
		self.time = time

		if(Display):
			self.DisplayInfo()

	def DisplayInfo(self):
		print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		print "self.step = ", self.step
		print "self.methods = ",self.methods
		print "self.ingredients = ", self.ingredients
		print "self.tools = ", self.tools
		print "self.times = ", self.time
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Non-Interface/Behind The Scenes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	#~~~~~~ Main Methods ~~~~~~
	def firstWordAnalysis(self, inpText=None):
		#We have inpText attribute because we do recursion in event of "("
		if(inpText!=None):
			lower_step = inpText.lower()
			lower_step_tokens = nltk.word_tokenize(lower_step)
			lower_step_pos = nltk.pos_tag(lower_step_tokens)
		else:
			lower_step = self.lower_step
			lower_step_tokens = self.lower_step_toks
			lower_step_pos = self.lower_step_pos

		recipe_ingrs_extracted_tokens = self.recipeIngrTokens

		method, tool, ingredient = [],[],[]
		fw = lower_step_tokens[0]
		if(fw == "("):
			#Nothing between () pertains to what we're after
			return self.firstWordAnalysis(lower_step[lower_step.index(")")+1:])
		
		elif (fw in dirn_methods):
			# If it is a verb
			method = [fw]
			in_a_index = self.findConsecutiveWords(["in", "a"], lower_step_tokens)
			if(in_a_index):
				tool = self.getAdjacentTool(in_a_index+2, lower_step_tokens, lower_step_pos)
				ingr, iterator = None, 1
				while(iterator<in_a_index):
					ingr = self.getAdjacentIngredient(iterator, lower_step_tokens, lower_step_pos)
					if(ingr!=None):
						iterator+=len(ingr)
					else:
						iterator+=1
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
			if( (tool==[]) or (iterator==None) ): iterator = 1

			# Check for "over ____ heat"
			if((lower_step_tokens[iterator] == "over") and (lower_step_tokens[iterator+2] == "heat")):
				iterator+=3
				
			#Get the method name. Checks for commas mainly.
			while(lower_step_tokens[iterator] not in dirn_methods):
				iterator+=1

			method = [lower_step_tokens[iterator]]
			
		elif ( (lower_step_pos[0][1]=="RB") and (lower_step_tokens[0] not in dirn_bad_adverbs)) :
			# if slowly, lightly, generously, lightly
			method, tool = self.firstWordAdverb(lower_step, lower_step_tokens, lower_step_pos)

		else: 
			ingredient = self.getAdjacentIngredient(0)

		return method, tool, ingredient

	def splitAnalysis(self):
		lower_step = self.lower_step
		lower_step_list = self.splitForSplitAnalysis()
		recipe_ingrs_extracted_toks = self.recipeIngrTokens
		methods, tools, ingredients = [],[],[]
		for splitted_elt in lower_step_list:
			if(len(splitted_elt)==0):
				continue
			method, tool, ingr = None, None, None
			lower_step_tokens = nltk.word_tokenize(splitted_elt)
			lower_step_pos = nltk.pos_tag(lower_step_tokens)
			tool = self.getAdjacentTool(0, lower_step_tokens, lower_step_pos)
			ingr = self.getAdjacentIngredient(0, lower_step_tokens, lower_step_pos)
			if(ingr==None):
				if(lower_step_tokens[0] in dirn_methods):
					method = lower_step_tokens[0]
					ingr = self.getAdjacentIngredient(1, lower_step_tokens, lower_step_pos)
				else:
					ingr = self.getAdjacentIngredient(0, lower_step_tokens, lower_step_pos)
			if((tool) and (method==tool)):
				#Then we are trying to declare the same thing twice.
				print "In splitted_elt = \"", splitted_elt, "\", we come across tool:", tool, " = elt: \" ", elt, " \" \n"
			if(tool!=None): tools += (tool)
			if(ingr!=None):
				if (len(ingr)>1): ingredients.append(ingr)
				else: ingredients+=ingr
			if(method!=None): methods.append(method)
		return methods, tools, ingredients
	
	def getConcreteTime(self):
		""" This function takes a step (as a string) and returns a string
			like '3 to 5 minutes' or '4 hours' or 'approximately 45 minutes'."""
		step = self.lower_step  #or maybe self.lowerstep

		print step
		tokens = nltk.word_tokenize(step)
		pos = nltk.pos_tag(tokens)

		# Check if this step metions time at all, using list defined at top of file
		time_unit = ""
		for time in dirn_time_units:
			if time in tokens:
				time_unit = time

		# If there is no mention of time, exit function
		if not time_unit:
			return "none"

		# This pattern matches anything that looks like:
		# 3 to 5 minutes, 4 hours, etc.
		final_time = ""
		pattern = "[0-9]+ [a-z]* *[0-9]* *" + time_unit

		match = re.search(pattern, step)
		if match:
			final_time = step[match.start():match.end()]
			# Add extra detail to time, if it is an estimate like "about 5 minutes"
			if "about " + final_time in step:
				final_time = "about " + final_time
			elif "approximately " + final_time in step:
				final_time = "approximately " + final_time
			# Else this step unfortunately doesn't use digits for its numbers
		# First check for numbers using NLTK Part-Of-Speech Tagging, numbers
		# are "CD"
		else:
			for word in pos:
				if word[1] == "CD":
					pattern = word[0] + " (to)? ?[a-z]* ?" + time_unit
					match = re.search(pattern, step)
					if match:
						final_time = step[match.start():match.end()]
					break
			
			# Check for phrases like "for five minutes"
		 	if "for" in tokens:
				idx = tokens.index("for") + 1
				while tokens[idx] != time_unit:
					final_time += tokens[idx] + " "
					idx += 1
				final_time += time_unit
				
			# Check for phrases like "a minute", "an hour", "an hour or two", etc
			elif " a " + time_unit in step:
				if " or two" in step:
					final_time = "a " + time_unit + " or two"

			elif " an " + time_unit in step:
				if " or two" in step:
					final_time = "an " + time_unit + " or two"	

			elif " a few " + time_unit in step:
				final_time = "a few " + time_unit

		# A few steps specify "per side" or "per batch", this grabs them
		if "per" in tokens:
			final_time += " per " + tokens[tokens.index("per") + 1]

		return final_time

	def getUntilTime(self):
		"""This function takes a step (as a string) that has the word 'until' in it,
		   and returns a string with the rest of the phrase, i.e. 'until golden brown'"""
		step = self.lower_step
		if "until" not in step:
			return None
		until_time = ""
		tokens = nltk.word_tokenize(step)
		if("until" in tokens):
			idx = tokens.index("until")	
			while idx < len(tokens) and tokens[idx] not in ",./;:()[]{}\|":
				until_time += tokens[idx] + " "
				idx += 1

			return until_time.strip()
		else:
			return None
	 
	#~~~~~~ Get Methods ~~~~~~
	def getAdjacentTool(self, index, inp_lower_step_toks = None, inp_lower_step_pos = None, retIterator=False):
		#checks if there is a tool starting from that index
		iterator, tool = index, []
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
				return [], None
			else:
				return []

		#While the next_word is compatible but not a tool, we continue onwards.
		while ( (iterator<len(lower_step_tokens)) and ((lower_step_tokens[iterator] in dirn_measurements) or (lower_step_tokens[iterator] in dirn_descriptors) 
		  or (bool(filter(lambda(x): x.isdigit(), lower_step_tokens[iterator]))))):
			iterator+=1
		if(iterator==len(lower_step_tokens)):
			if(retIterator):
				return [], None
			else:
				return []
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
			return [], None
		else:
			return []

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
		susp_ingr_singular, susp_ingr_plural = pattern.en.singularize(susp_ingr), pattern.en.pluralize(susp_ingr)
		susp_ingr_present, susp_ingr_present_regular, susp_ingr_present_singular, susp_ingr_present_plural = False, False, False, False
		for ingr_token in recipe_ingrs_extracted_tokens:
			#The tokens of 1 ingredient 
			if(susp_ingr in ingr_token):
				susp_ingr_present = True
				susp_ingr_present_regular = True
			elif(susp_ingr_singular in ingr_token):
				susp_ingr_present = True
				susp_ingr_present_singular = True
			elif(susp_ingr_plural in ingr_token):
				susp_ingr_present = True
				susp_ingr_present_singular = False

			if(susp_ingr_present):
				len_ingr_token = len(ingr_token)
				iterator_fwd, iterator_bwd = None, None
				if(len_ingr_token>1):
					if(susp_ingr_present_regular):
						token_index = ingr_token.index(susp_ingr) #The Index at which the Susp_Ingr occurs in the ingr_token
					elif(susp_ingr_present_singular):
						token_index = ingr_token.index(susp_ingr_singular) #The Index at which the Susp_Ingr occurs in the ingr_token
					else:
						token_index = ingr_token.index(susp_ingr_plural) #The Index at which the Susp_Ingr occurs in the ingr_token
					
					len_ingr_token = len(ingr_token)
					len_step_tokens = len(lower_step_tokens) #The length of the lower_step_tokens (the input segment)

					if(token_index==0): 
						#if suspected ingredient is found at the start of the token, check if there is a match w the next one
						iterator_fwd = 1
						while( (len_step_tokens > (iterator_fwd+iterator) ) and ( (lower_step_tokens[iterator_fwd+iterator] in ingr_token)
						  or ( pattern.en.singularize(lower_step_tokens[iterator_fwd+iterator]) in ingr_token) 
					 	  or ( pattern.en.pluralize(lower_step_tokens[iterator_fwd+iterator]) in ingr_token))):
							iterator_fwd+=1
						iterator_fwd-=1

					elif(token_index == (len_ingr_token-1) ): 
						#if suspected ingredient is found at the end of the token, check if there is a match w the previous one
						iterator_bwd = -1
						while( ((iterator_bwd+iterator) >= 0) and ( (lower_step_tokens[iterator_bwd+iterator] in ingr_token)
						  or ( pattern.en.singularize(lower_step_tokens[iterator_bwd+iterator]) in ingr_token)
						  or ( pattern.en.pluralize(lower_step_tokens[iterator_bwd+iterator]) in ingr_token))):
							iterator_bwd-=1
						iterator_bwd+=1

					else:
						#may be a chance that it is before OR after.
						iterator_fwd, iterator_bwd = 1, -1
						while( (len_step_tokens > (iterator_fwd+iterator)) and ( (lower_step_tokens[iterator_fwd+iterator] in ingr_token)
						  or (pattern.en.singularize(lower_step_tokens[iterator_fwd+iterator]) in ingr_token) 
						  or (pattern.en.pluralize(lower_step_tokens[iterator_fwd+iterator]) in ingr_token))):
							iterator_fwd+=1
						
						while( ((iterator_bwd+iterator) >= 0 ) and ( (lower_step_tokens[iterator_bwd+iterator] in ingr_token)
							or (pattern.en.singularize(lower_step_tokens[iterator_bwd+iterator]) in ingr_token)
						    or (pattern.en.pluralize(lower_step_tokens[iterator_bwd+iterator]) in ingr_token))):
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
			method = [lower_step_tokens[1]] #Should always be the case
			iterator = 2
			tool = self.getAdjacentTool(iterator, lower_step_tokens, lower_step_pos)
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

	def splitForSplitAnalysis(self, inp_str=None):
		if(inp_str):
			lower_step = inp_str
		else:
			lower_step = self.lower_step
		lower_step = lower_step.replace("(","").replace(")","")
		lower_step_list = [lower_step]
		for split_tok in dirn_split_toks:
			i = 0
			while(i<len(lower_step_list)):
				list_elt = lower_step_list[i]
				toks = nltk.word_tokenize(list_elt)
				if split_tok in toks:
					if(split_tok.isalpha()):
						span_generator = WhitespaceTokenizer().span_tokenize(list_elt)
						spans = [span for span in span_generator]
						cut_start, cut_end = spans[toks.index(split_tok)]
						str1 = list_elt[:cut_start]
						str2 = list_elt[cut_end+1:]
						if(str1.strip()!=""):
							str1 = self.splitForSplitAnalysis(str1)
						if(str2.strip()!=""):
							str2 = self.splitForSplitAnalysis(str2)
						if(str1 and str2):
							lower_step_list+=map(str.strip, str1+str2)
						elif(str1):
							lower_step_list+=map(str.strip, str1)
						elif(str2):
							lower_step_list+=map(str.strip, str2)
						lower_step_list.remove(list_elt)
						i = - 1
					else:
						lower_step_list+=map(str.strip, list_elt.split(split_tok))
						lower_step_list.remove(list_elt)
						i = -1
				i+=1
		return lower_step_list
