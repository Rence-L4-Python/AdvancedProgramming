# Badum-tsh, maybe make a bot that tells the joke?
import re
import random
from tkinter import *

jokes = [] # List to hold text lines from regex

def loadJokes(): # Function for opening text files, using regular expressions for data extraction
    with open("randomJokes.txt","r") as file: # Opens and reads the text file
        for regex in file:
            x = re.split(r'(?<=\?)', regex.strip()) # Splits the strings in the text file into lists using the question mark as reference. 
            jokes.append(x) # Adds the extracted data to the global list "jokes"

def displayJokes(): # Code logic
    if jokes:
        selected_joke = random.choice(jokes) # Selects a random joke from the list
        jokes.remove(selected_joke) # Removes the current joke from the list
        print("\n".join(selected_joke)) # Print the current joke in console for testing
        print(f"\nRemaining jokes: {len(jokes)}\n") # Print remaining jokes in console for testing
        return selected_joke # Makes this available to displayGUI()
    else:
        return ["No more jokes available!"] # Returns this text to Tklabel1

def displayGUI(): # Function for displaying things in the Tkinter GUI
    selected_joke = displayJokes() # Assigning functions to the variable

    if selected_joke: # Runs these commands if selected_joke contains something
        Tklabel1.config(text=selected_joke[0]) # Changes text in first label
        Tkimage.config(image=image1) # Reverts image back to robot neutral face
        root.after(1500, update_image, selected_joke)  # Updates image to robot smiling face after a 1.5 second delay

    if len(selected_joke) > 1: # Can just combine this with the first if-statement; this only serves to organize the code
        Tklabel2.config(text="") # Clears the second label's text every time the button is pressed
        secondLabel = selected_joke[1] # Second label uses the "punchline" in the jokes list
        root.after(1500, update_Tklabel2, secondLabel) # Updates Tklabel2 "punchline" after a 1.5 second delay

    if len(jokes) == 0: # Clears the second label if there are no more jokes left
        Tklabel2.config(text="")

    Tklabel3.config(text=f"Remaining jokes: {len(jokes)}") # Shows how many jokes are left

def update_Tklabel2(text): # Function for updating Tklabel2
    Tklabel2.config(text=text)

def update_image(selected_joke): # Function for updating Tkimage
    Tkimage.config(image=image2)

loadJokes() # Initialize regex function

# Tkinter GUI code
root = Tk()
root.title("Joke Generator")
root.geometry("350x250")
root.minsize(350, 250)
root.maxsize(350, 250)
root.configure(background="lightgray")
image1 = PhotoImage(file="sprite1.png") # Custom image I made in Aseprite, robot neutral face
image2 = PhotoImage(file="sprite2.png") # Custom image I made in Aseprite, robot smiling face
Tkimage = Label(root, image=image1)
Tkimage.pack(side=TOP, expand=TRUE, pady=10)
Tklabel1 = Label(root, text="", borderwidth=2, relief=GROOVE, font=("Roboto"))
Tklabel1.pack(side=TOP, expand=TRUE, fill=BOTH)
Tklabel2 = Label(root, text="", borderwidth=2, relief=GROOVE, font=("Roboto"))
Tklabel2.pack(side=TOP, expand=TRUE, fill=BOTH)
Tklabel3 = Label(root, text=f"Remaining jokes: {len(jokes)}", bg="lightgray", font=("Roboto"))
Tklabel3.pack(side=TOP, expand=TRUE, fill=BOTH, pady=10)
Tkbutton = Button(root, text="Generate Joke", bg="#b4b4b4", command=displayGUI, font=("Roboto", 16))
Tkbutton.pack(side=TOP, expand=TRUE, pady=(0,20))
root.mainloop()