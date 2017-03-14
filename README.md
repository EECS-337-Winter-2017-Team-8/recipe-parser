This is a Recipe Parser for EECS 337 taught in Winter 2017 at Northwestern University. It is written by Drew Bronson, Omar Shanti, Kurt Imhoff, and Adrian Andronic.



To run the program, enter Python on the command line and run execfile("final.py").

The program will ask you for a URL.

It will create one Recipe object from the URL print its title, formatted ingredients, and the list of directions.

Then it will ask you to type a number corresponding to a transformation (Vegan, Serving Size, Low Fat, High Fat, Low Carb, High Carb, Vegetarian).

It will then create a new Recipe object with the proper transformation, and print this new object the same way it did the last one, with a modified title, modified ingredients and directions.

After the program is done running, there are two Recipe objects on the command line you can investigate, old and new. These correspond to the original and transformed recipes, resepctively.

A list of all the class variables are in RecipeClass.py and StepClass.py, but here are a few examples of how to get info from the two objects.

old.PrimaryMethods
old.formattedToolsData

for step in new.Steps:
  print step.step (prints the plain txt of the step)
  print step.methods
  print step.tools


....etc
