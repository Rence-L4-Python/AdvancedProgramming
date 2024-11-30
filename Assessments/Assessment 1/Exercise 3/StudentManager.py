import customtkinter # Using custom themes in Tkinter for better and modern visuals. Need to run `pip install customtkinter` in CMD or this program wont work as intended. 
from tkinter import ttk
from tkinter import messagebox
import re

# Dictionary for grade ranges
grades = {
    "A": (70, 100),
    "B": (60, 69),
    "C": (50, 59),
    "D": (40, 49),
    "F": (0, 39),
}

def parse_file(): # Repeated commands, basically just for reading and matching the strings inside studentMarks.txt
    student_data = [] # Holds all the appended data from the text file
    with open("studentMarks.txt", "r") as file:
        for regex in file:
            match = re.match(r'(\d+),\s*([\w\s]+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)', regex.strip()) # regEx pattern for the characters in studentMarks.txt
            if match: # Ensures only valid lines that match the pattern are appended (if the records added are not formatted properly, then it will not show up in the records at all despite being written inside studentMarks.txt)
                student_data.append(match.groups())
    return student_data # Allows the new value to be used in other functions

def regExLogic():
    student_data = parse_file() # student_data variable becomes a list of tuples that hold the student records
    for student in student_data: # Iterates through each student
        overall_percentage = overallPercentageCalc(student) # overall_percentage variable calls the overallPercentageCalc() function 
        overall_percentage_symbol = f"{overall_percentage}%" # Adds the % symbol to the calculated percentage through f-strings
        grade = grading(overall_percentage) # grade variable calls the grading() function
        treeview.insert("", "end", values=student + (overall_percentage_symbol, grade)) # Inserts previous (student id, marks...) and new data (percentage and grade) to the treeview widget

def show_highestMarks(): # REQUIRED FUNCTION FOR ASSESSMENT: SHOW STUDENT WITH HIGHEST OVERALL MARK
    treeview.delete(*treeview.get_children()) # Helps with clearing the treeview data before moving to different "pages"

    top_student = None # Stores data of the student with the highest marks
    highest_mark = -1 # Tracks the highest mark a student has

    student_data = parse_file() # Returns a list of student records
    for student in student_data: 
        overall_mark = overallPercentageCalc(student) # Computes the student's overall percentage
        if overall_mark > highest_mark: # Since this is true, these variables will be updated with the new data.
            highest_mark = overall_mark
            top_student = student
    
    if top_student: # Checks if top_student was found
        overall_percentage = overallPercentageCalc(top_student) # Calculates the overall percentage of the top student
        overall_percentage_symbol = f"{overall_percentage}%" # f-string formatted with a variable to allow styling numbers with a percentage
        grade = grading(overall_percentage) # Assigning a function to a variable
        treeview.insert("", "end", values=top_student + (overall_percentage_symbol, grade)) # Inserts previous (student id, marks...) and new data (percentage and grade) to the treeview widget

def show_lowestMarks(): # REQUIRED FUNCTION FOR ASSESSMENT: SHOW STUDENT WITH LOWEST OVERALL MARK
    treeview.delete(*treeview.get_children()) 

    lowest_student = None # Stores data of the student with the lowest marks
    lowest_mark = float('inf') # Tracks the lowest mark a student has using 'positive infinity' to make sure the boolean works in the iterated list

    student_data = parse_file() 
    for student in student_data: 
        overall_mark = overallPercentageCalc(student)
        if overall_mark < lowest_mark: # Because of the 'positive infinity', overall_mark is automatically lower than lowest_mark. This helps update the variables with the new data
            lowest_mark = overall_mark
            lowest_student = student
    
    if lowest_student: # Checks if lowest_student was found
        overall_percentage = overallPercentageCalc(lowest_student)
        overall_percentage_symbol = f"{overall_percentage}%"
        grade = grading(overall_percentage)
        treeview.insert("", "end", values=lowest_student + (overall_percentage_symbol, grade))

def overallPercentageCalc(student): # Function to calculate the overall percentage of a student
    mark1 = int(student[2]) # These variables are the same ones used throughout the treeview. The student tuples' items are converted into integers as they get accessed through indexing
    mark2 = int(student[3])
    mark3 = int(student[4])
    exam_mark = int(student[5])

    total_marks = mark1 + mark2 + mark3 + exam_mark # Simple logic for getting the total marks
    total_available = 160 # Total available marks

    percentage = (total_marks / total_available) * 100 # Divides the total marks a student receives by the total available marks and multiplies it by 100 to get floating point numbers

    return round(percentage) # Rounds off the floating point numbers and converts them to integers

def grading(percentage): # Assigns the grades in the dictionary
    for grade, (floor, ceiling) in grades.items(): # Iterates over the grades dictionary and returns the key-value pairs
        if floor <= percentage <= ceiling: # Checks whether the percentage falls within the range of floor and ceiling (0, 9 etc...)
            return grade

def showAll(): # REQUIRED FUNCTION FOR ASSESSMENT: SHOW ALL STUDENT RECORDS (just uses the regExLogic() function since they just do the same things, except it deletes all the rows in the treeview before initializing them again)
    treeview.delete(*treeview.get_children())
    regExLogic() # Initializes the regExLogic() function to show all the student records again

def searchFunc(): # REQUIRED FUNCTION FOR ASSESSMENT: VIEW INDIVIDUAL STUDENT RECORD
    student_id = entry.get() # Retrieves the user input inside the search bar
    treeview.delete(*treeview.get_children()) 

    student_data = parse_file()
    for student in student_data:
        if student[0] == student_id: # Checks if the student id inside the tuple corresponds with the user input in the search bar
            treeview.insert("", "end", values=student) # Inserts the searched student in the treeview, only showing them individually
            break

def sortByOrder(treeview, col, descending): # BONUS FUNCTION FOR ASSESSMENT: SORT STUDENT RECORDS ===== Logic reference: https://www.w3resource.com/python-exercises/tkinter/python-tkinter-widgets-exercise-18.php 
    items = [(treeview.set(item, col), item) for item in treeview.get_children('')] # List comprehension that makes a list of tuples that contains values from columns and rows from the treeview

    if col in ('student_id', 'mark1', 'mark2', 'mark3', 'exam_mark'): # Checks if the column contains any of the items here and then sorts them in a descending or ascending order after converting the column value into an integer
        items.sort(key=lambda x: int(x[0]), reverse=descending) 
    elif col == 'overall': # Same logic as the previous statement, but removes the '%' character so integers can be used to sort the column value
        items.sort(key=lambda x: int(x[0].replace('%', '')), reverse=descending)
    else: # Sorts any other type of column in an alphabetical order
        items.sort(reverse=descending)

    for index, (_, item) in enumerate(items): # Updates the treeview with the sorted items
        treeview.move(item, '', index) # Reorders the items in a new position depending on the index
    
    treeview.heading(col, command=lambda: sortByOrder(treeview, col, not descending)) # Sorting command for toggling either ascending or descending order when clicking on the column header

def deleteRecord(): # BONUS FUNCTION FOR ASSESSMENT: DELETE STUDENT RECORDS
    student_id = entry.get() # Retrieves the user input inside the search bar
    student_data = parse_file()

    student_data = [student for student in student_data if student[0] != student_id] # List comprehension about updating the list of student records and removing ONLY the matching student ID

    if len(student_data) == len(parse_file()): # Checks if the length of the two objects are the same, and if the student ID is not in the lists, it will print the error
        print("No matching student found!") # Console testing
        messagebox.showwarning("Warning!", "No matching student found!\nUse the searchbar to input proper IDs.") # Warning messagebox popup
        return
    
    with open("studentMarks.txt", "w") as file: # Updates the student records in the studentMarks.txt file
        for student in student_data:
            file.write(', '.join(student) + '\n')
        
    print(f"Student ID {student_id}'s records have been deleted.") # Console testing
    messagebox.showwarning("Warning!", f"Student ID {student_id}'s records have been deleted.") # Warning messagebox popup

    showAll() # Updates the treeview again to show the updated list (removed student data)

addStudentRecordWindow = None # Used to keep track of whether the addStudentRecordWindow has already been opened or not

def addRecordWindow(): # BONUS FUNCTION FOR ASSESSMENT: ADD STUDENT RECORDS
    global addStudentRecordWindow

    if addStudentRecordWindow is not None and addStudentRecordWindow.winfo_exists(): # Shows a warning popup if the window is already open, stopping the user from opening more of them
        messagebox.showinfo("", "The Add New Student Record window is already open.")
        return

    addStudentRecordWindow = customtkinter.CTkToplevel(root)
    addStudentRecordWindow.title("Add New Student Record")
    addStudentRecordWindow.geometry("854x480")
    addStudentRecordWindow.resizable(False, False)

    student_id_label = customtkinter.CTkLabel(addStudentRecordWindow, text="Student ID:")
    student_id_label.pack(expand=True)
    student_id_entry = customtkinter.CTkEntry(addStudentRecordWindow)
    student_id_entry.pack(expand=True)

    name_label = customtkinter.CTkLabel(addStudentRecordWindow, text="Name:")
    name_label.pack(expand=True)
    name_entry = customtkinter.CTkEntry(addStudentRecordWindow)
    name_entry.pack(expand=True)

    mark1_label = customtkinter.CTkLabel(addStudentRecordWindow, text="Coursework 1 Score:")
    mark1_label.pack(expand=True)
    mark1_entry = customtkinter.CTkEntry(addStudentRecordWindow)
    mark1_entry.pack(expand=True)

    mark2_label = customtkinter.CTkLabel(addStudentRecordWindow, text="Coursework 2 Score:")
    mark2_label.pack(expand=True)
    mark2_entry = customtkinter.CTkEntry(addStudentRecordWindow)
    mark2_entry.pack(expand=True)

    mark3_label = customtkinter.CTkLabel(addStudentRecordWindow, text="Coursework 3 Score:")
    mark3_label.pack(expand=True)
    mark3_entry = customtkinter.CTkEntry(addStudentRecordWindow)
    mark3_entry.pack(expand=True)

    exam_mark_label = customtkinter.CTkLabel(addStudentRecordWindow, text="Exam Score:")
    exam_mark_label.pack(expand=True)
    exam_mark_entry = customtkinter.CTkEntry(addStudentRecordWindow)
    exam_mark_entry.pack(expand=True)

    def saveAddedRecord(): # Function for saving the added records
        global addStudentRecordWindow

        student_id = student_id_entry.get() # Attaching retrieved input from the user to variables
        name = name_entry.get()
        mark1 = mark1_entry.get()
        mark2 = mark2_entry.get()
        mark3 = mark3_entry.get()
        exam_mark = exam_mark_entry.get()

        if not all([student_id, name, mark1, mark2, mark3, exam_mark]): # Checks if the fields are empty or not and shows a warning popup if they are empty
            messagebox.showwarning("", "All fields must be filled!")
            return
        
        with open("studentMarks.txt", "a") as file: # Appends text to the end of the file without overwriting data
            file.write(f"\n{student_id}, {name}, {mark1},{mark2},{mark3},{exam_mark}")

        messagebox.showinfo("", "New student record added successfully!")
        addStudentRecordWindow.destroy() # Closes the window and resets tracking
        addStudentRecordWindow = None
        showAll()

    saveRecord_button = customtkinter.CTkButton(addStudentRecordWindow, text="Save Record", font=("Lato", 12, "bold"), command=saveAddedRecord)
    saveRecord_button.pack(expand=True, pady=20)

# Functions for search bar placeholder text
def on_focus_in(_):
    if entry.get() == placeholder_text:
        entry.delete(0, customtkinter.END)
        entry.configure(text_color="black")
def on_focus_out(_):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.configure(text_color="gray")

# Tkinter Base
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk() # Custom tkinter has custom classes (CTk)
root.title("Student Manager")
root.state('zoomed') # Starts the GUI in windowed full-screen
root.minsize(854, 480)

navbar = customtkinter.CTkFrame(root, corner_radius=0)
navbar.configure(fg_color="#3F51B5")
navbar.pack(fill='x')

header = customtkinter.CTkLabel(navbar, text="STUDENT MANAGER", font=("Lato", 24, "bold"), text_color="#FFFFFF", height=78)
header.pack(side='left', padx=(20, 10))

placeholder_text = "Enter Student ID" # Placeholder text used in search bar

searchBar = customtkinter.CTkFrame(navbar)
searchBar.configure(fg_color="#3F51B5")
searchBar.pack(side='left', padx=10)

entry = customtkinter.CTkEntry(searchBar, width=250, height=35)
entry.insert(0, placeholder_text)
entry.configure(text_color="gray")
entry.bind("<FocusIn>", on_focus_in)
entry.bind("<FocusOut>", on_focus_out)
entry.pack(side='left', fill='both')

search_button = customtkinter.CTkButton(searchBar, text="🔍", font=("Lato", 12, "bold"), command=searchFunc, width=10) # Search button placed inside an entry widget
search_button.configure(bg_color="#FFFFFF")
search_button.place(relx=0.9875, rely=0.49, anchor="e")

showAll_button = customtkinter.CTkButton(navbar, text="Show all student records", font=("Lato", 12, "bold"), command=showAll)
showAll_button.pack(side='left', padx=10)

showHighest_button = customtkinter.CTkButton(navbar, text="Show highest marks", font=("Lato", 12, "bold"), command=show_highestMarks)
showHighest_button.pack(side='left', padx=10)

showLowest_button = customtkinter.CTkButton(navbar, text="Show lowest marks", font=("Lato", 12, "bold"), command=show_lowestMarks)
showLowest_button.pack(side='left', padx=10)

addRecord_button = customtkinter.CTkButton(navbar, text="Add record", font=("Lato", 12, "bold"), command=addRecordWindow)
addRecord_button.pack(side='left', padx=10)

deleteRecord_button = customtkinter.CTkButton(navbar, text="Delete record", font=("Lato", 12, "bold"), command=deleteRecord)
deleteRecord_button.pack(side='left', padx=(10, 20))

columns = ('student_id','name','mark1','mark2','mark3','exam_mark','overall','grade') # Defines a tuple containing items that will be used as the headers in the treeview widget
treeview = ttk.Treeview(root, columns=columns, show='headings') # Shows a treeview using the previously mentioned columns and only showing them as headings

treeview.heading('student_id', text="Student ID", anchor="w", command=lambda: sortByOrder(treeview, 'student_id', False)) # Defines the column headings for the treeview. The sorting function is attached to all of them to sort the rows under their columns in a descending or ascending order.
treeview.heading('name', text="Name", anchor="w", command=lambda: sortByOrder(treeview, 'name', False))
treeview.heading('mark1', text="Coursework 1", anchor="w", command=lambda: sortByOrder(treeview, 'mark1', False))
treeview.heading('mark2', text="Coursework 2", anchor="w", command=lambda: sortByOrder(treeview, 'mark2', False))
treeview.heading('mark3', text="Coursework 3", anchor="w", command=lambda: sortByOrder(treeview, 'mark3', False))
treeview.heading('exam_mark', text="Exam Score", anchor="w", command=lambda: sortByOrder(treeview, 'exam_mark', False))
treeview.heading('overall', text="Overall Percentage", anchor="w", command=lambda: sortByOrder(treeview, 'overall', False))
treeview.heading('grade', text="Grade", anchor="w", command=lambda: sortByOrder(treeview, 'grade', False))
treeview.pack(fill='both', expand='true')

regExLogic() # Initializes the regExLogic() function

root.mainloop()