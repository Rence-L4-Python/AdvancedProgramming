from tkinter import *
import random
import operator

# Dictionaries
difficulties = { # Dictionary of selectable difficulties with different ranges according to their difficulty
    "Difficulty: Easy": (0, 9),
    "Difficulty: Moderate": (0, 99),
    "Difficulty: Advanced": (0, 9999),
}

operations = { # Was originally going to contain other operators such as multiplication and division
    "+": operator.add,
    "-": operator.sub,
}

score_ranks = { # List of score ranks / grades that the user can achieve
     "A+": (90, 100),
     "A": (80,89),
     "B": (70,79),
     "C": (60,69),
     "D": (50,59),
     "F": (0,49),
}

# Global variables, these are used by different functions
points = 0
quiz_count = 0
attempts = 0

def displayMenu(): # FUNCTION REQUIREMENT FOR ASSESSMENT
    global selected_difficulty
    selected_difficulty = StringVar(value="Difficulty: Easy") # Sets the difficulty to easy by default

    clear_widgets() # Clears previous widgets to load new ones
    newGame() # Resets global variables for replayability

    Label(root, text="Welcome to the Math Quiz Generator!", font=("Arial", 26, "bold"), fg="#8B0000", bg="#F0F0F0").place(relx=0.5, rely=0.225, anchor=CENTER) # Header text
    
    Button(root, text="Start Quiz", font=("Arial", 16, "bold"), bg="#E9E9E9", command=displayProblem, padx=15, pady=15).place(relx=0.5, rely=0.5, anchor=CENTER) # Start Quiz button

    option_menu = OptionMenu(root, selected_difficulty, *difficulties) # Dropdown list for difficulties
    option_menu.config(font=("Arial", 14), bg="#E9E9E9", padx=5, pady=5)
    option_menu.place(relx=0.5, rely=0.65, anchor=CENTER)
    
def newGame(): # Resets all global variables to allow for replayability
     global points, quiz_count, attempts # Makes sure this affects the variables outside this function
     points = 0
     quiz_count = 0
     attempts = 0

def clear_widgets(): # Clears all previous widgets to replace with new ones from other functions
     for widget in root.winfo_children(): # Hides the root window's widgets until they get initialized again
          widget.place_forget() 

def displayProblem(): # FUNCTION REQUIREMENT FOR ASSESSMENT
    global x, y, answer_entry, quiz_count # Makes sure this affects the variables outside this function

    if quiz_count >= 10: # Condition for displaying results once you finish answering ten questions in the quiz
        displayResults()
        return

    clear_widgets() # Clears previous widgets to load new ones

    chosenDifficulty = selected_difficulty.get() # Variable for selected difficulty
    x = randomInt(chosenDifficulty) # Variables for the randomly generated number function that scales according to difficulty
    y = randomInt(chosenDifficulty)

    decideOperation()

    Label(root, text=f"Points: {points}/100", font=("Arial", 10, "italic"), justify=LEFT, fg="#006400", bg="#F0F0F0").place(relx=0.46, rely=0.265, anchor=CENTER) # Shows points achieved out of 100, placed beside the red button
    Button(root, text=" X ", command=displayMenu, font="Arial", bg="#CD5C5C").place(relx=0.3495, rely=0.2375) # 'Home' or 'Back' button

    quiz_frame = Frame(root, padx=20, pady=20, borderwidth=1, relief=RIDGE) # Frame to avoid opening new windows, acting as a page
    quiz_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(quiz_frame, text=f"Question # {quiz_count + 1}/10: \n\n{x} {chosenOperation} {y} = ?", font="Arial").pack(pady=10) # Main quiz question generator
    answer_entry = Entry(quiz_frame, font="Arial", justify=CENTER) # User input entry
    answer_entry.pack()
    Button(quiz_frame, text="Submit", command=lambda: isCorrect(chosenOperation), font=("Arial", 12, "bold"), bg="#90EE90", padx=10, pady=10).pack(pady=(20, 10)) # Calls the isCorrect() function, checking to see if the user's input corresponds with the correct answer of the generated item

    quiz_count += 1 # Increases the value checker of the current quiz item after the user completes the question

def randomInt(difficulty): # FUNCTION REQUIREMENT FOR ASSESSMENT
    floor, ceiling = difficulties[difficulty] # Range for the difficulties dictionary
    return random.randint(floor, ceiling) # Generates and returns random integers in the range

def decideOperation(): # FUNCTION REQUIREMENT FOR ASSESSMENT
    global chosenOperation # Makes sure this affects the variables outside this function
    chosenOperation = random.choice(list(operations.keys())) # Randomly selects between two operations for the quiz

def get_rank(score): # Added function for getting the user's rank based on their score
     for rank, (floor, ceiling) in score_ranks.items(): # Iterates over the items inside the score_ranks dictionary
          if floor <= score <= ceiling: # Checks if the user's points falls within the rank's floor and ceiling (low, high)
               return rank # Returns user's rank if it falls under the ranges

def displayResults(): # FUNCTION REQUIREMENT FOR ASSESSMENT
    global points # Makes sure this affects the variables outside this function
    user_rank = get_rank(points)  # Calls the get_rank function with the user's points/score
    rank_info = '\n\n'.join([f"{rank}: {floor}-{ceiling} points" for rank, (floor, ceiling) in score_ranks.items()]) # String concatenation to display the dictionary's items in a format
    
    clear_widgets() # Clears previous widgets to load new ones

    result_frame = Frame(root, padx=20, pady=20, borderwidth=1, relief=RIDGE) # Frame to avoid opening new windows, acting as a page
    result_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(result_frame, text=f"Quiz Over! You scored {points} points.\n\nYour score rank is: {user_rank}", font="Arial").pack(pady=10) # Shows the user's rank based on their points
    Button(result_frame, text="Play Again", command=displayMenu, font=("Arial", 12, "bold"), bg="#90EE90", padx=10, pady=10).pack(pady=10) # Button to let the user play the quiz again

    Label(result_frame, text=f"{rank_info}", font="Arial").pack(pady=10) # Shows the string concatenation

def isCorrect(chosenOperation): # FUNCTION REQUIREMENT FOR ASSESSMENT
    global points, attempts # Makes sure this affects the variables outside this function

    correct_answer = operations[chosenOperation](x, y) # Randomly selected operator from the operations dictionary adds or subtracts the randomInt() ranges through their variables

    try:
        user_answer = int(answer_entry.get()) # Retrieves user's input in the entry widget

        if user_answer == correct_answer: # Logic for correct answers
                points += 10 if attempts == 0 else 5 # Gives the user 10 points for a correct answer and 5 points for a correct answer in their second attempt; they do not get any points if they are still incorrect
                print(f"Correct! {'You got 10 points!' if attempts == 0 else 'You got 5 points!'}\nTotal points: {points}\n") # Just prints stuff in the console for testing
                attempts = 0 # Resets attempts back to 0
                displayProblem() # Shows another problem
        else:
                if attempts == 0:
                    attempts += 1 # Allows the user to try a second time 
                    print("Incorrect! Try again.\n") # Just prints stuff in the console for testing
                    Label(root, text="Incorrect! Try again.", font=("Arial", 10, "italic"), justify=LEFT, fg="#CD5C5C", bg="#F0F0F0").place(relx=0.61, rely=0.265, anchor=CENTER) # Shows an 'incorrect' message placed beside the points counter
                else:
                    print("Incorrect!") # Just prints stuff in the console for testing
                    attempts = 0 # Resets attempts back to 0
                    displayProblem() # Shows another problem, ending the user's chances to retry the question and not awarding them any points

    except ValueError:
            print("Invalid input!") # Ensures the user is only inputting integers

# Tkinter root code, this is used as a base to build on all the widgets from other functions
root = Tk()
root.title("Math Quiz Generator")
root.geometry("750x550")
root.resizable(False, False)
root.configure(bg="#F0F0F0")

displayMenu() # Initializes the main function 
root.mainloop()