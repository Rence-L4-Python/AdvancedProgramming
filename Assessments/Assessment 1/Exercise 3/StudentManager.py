import customtkinter # Using custom themes in Tkinter for better and modern visuals. Need to run `pip install customtkinter` in CMD or this program wont work as intended. 
from tkinter import ttk
import re

# Dictionary for grade ranges
grades = {
    "A": (70, 100),
    "B": (60, 69),
    "C": (50, 59),
    "D": (40, 49),
    "F": (0, 39),
}

def parse_file(): 
    student_data = []
    with open("studentMarks.txt", "r") as file:
        for regex in file:
            match = re.match(r'(\d+),\s*([\w\s]+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)', regex.strip())
            if match:
                student_data.append(match.groups())
    return student_data

def regExLogic():
    student_data = parse_file()
    for student in student_data:
        overall_percentage = overallPercentageCalc(student)
        overall_percentage_symbol = f"{overall_percentage}%"
        grade = grading(overall_percentage)
        treeview.insert("", "end", values=student + (overall_percentage_symbol, grade))

def show_highestMarks():
    treeview.delete(*treeview.get_children())

    top_student = None
    highest_mark = -1

    student_data = parse_file()
    for student in student_data:
        overall_mark = overallPercentageCalc(student)
        if overall_mark > highest_mark:
            highest_mark = overall_mark
            top_student = student
    
    if top_student:
        overall_percentage = overallPercentageCalc(top_student)
        overall_percentage_symbol = f"{overall_percentage}%"
        grade = grading(overall_percentage)
        treeview.insert("", "end", values=top_student + (overall_percentage_symbol, grade))

def show_lowestMarks():
    treeview.delete(*treeview.get_children())

    lowest_student = None
    lowest_mark = float('inf')

    student_data = parse_file()
    for student in student_data:
        overall_mark = overallPercentageCalc(student)
        if overall_mark < lowest_mark:
            lowest_mark = overall_mark
            lowest_student = student
    
    if lowest_student:
        overall_percentage = overallPercentageCalc(lowest_student)
        overall_percentage_symbol = f"{overall_percentage}%"
        grade = grading(overall_percentage)
        treeview.insert("", "end", values=lowest_student + (overall_percentage_symbol, grade))

def overallPercentageCalc(student):
    mark1 = int(student[2])
    mark2 = int(student[3])
    mark3 = int(student[4])
    exam_mark = int(student[5])

    total_marks = mark1 + mark2 + mark3 + exam_mark
    total_available = 160

    percentage = (total_marks / total_available) * 100

    return round(percentage)

def grading(percentage):
    for grade, (floor, ceiling) in grades.items():
        if floor <= percentage <= ceiling:
            return grade

def showAll():
    treeview.delete(*treeview.get_children())
    regExLogic()

def searchFunc():
    student_id = entry.get()
    treeview.delete(*treeview.get_children())

    student_data = parse_file()
    for student in student_data:
        if student[0] == student_id:
            treeview.insert("", "end", values=student)
            break

def sortByOrder(treeview, col, descending): # Logic reference: https://www.w3resource.com/python-exercises/tkinter/python-tkinter-widgets-exercise-18.php
    items = [(treeview.set(item, col), item) for item in treeview.get_children('')]

    if col in ('student_id', 'mark1', 'mark2', 'mark3', 'exam_mark'):
        items.sort(key=lambda x: int(x[0]), reverse=descending)
    elif col == 'overall':
        items.sort(key=lambda x: int(x[0].replace('%', '')), reverse=descending)
    else:
        items.sort(reverse=descending)

    for index, (_, item) in enumerate(items):
        treeview.move(item, '', index)
    
    treeview.heading(col, command=lambda: sortByOrder(treeview, col, not descending))

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

root = customtkinter.CTk()
root.title("Student Manager")
root.state('zoomed')
root.minsize(854, 480)

navbar = customtkinter.CTkFrame(root, corner_radius=0)
navbar.configure(fg_color="#3F51B5")
navbar.pack(fill='x')

header = customtkinter.CTkLabel(navbar, text="STUDENT MANAGER", font=("Lato", 24, "bold"), text_color="#FFFFFF", height=78)
header.pack(side='left', padx=(20, 10))

placeholder_text = "Enter Student ID"

searchBar = customtkinter.CTkFrame(navbar)
searchBar.configure(fg_color="#3F51B5")
searchBar.pack(side='left', padx=10)

entry = customtkinter.CTkEntry(searchBar, width=250, height=35)
entry.insert(0, placeholder_text)
entry.configure(text_color="gray")
entry.bind("<FocusIn>", on_focus_in)
entry.bind("<FocusOut>", on_focus_out)
entry.pack(side='left', fill='both')

search_button = customtkinter.CTkButton(searchBar, text="🔍", font=("Lato", 12, "bold"), command=searchFunc, width=10)
search_button.configure(bg_color="#FFFFFF")
search_button.place(relx=0.9875, rely=0.49, anchor="e")

showAll_button = customtkinter.CTkButton(navbar, text="Show all student records", font=("Lato", 12, "bold"), command=showAll)
showAll_button.pack(side='left', padx=10)

showHighest_button = customtkinter.CTkButton(navbar, text="Show student with highest marks", font=("Lato", 12, "bold"), command=show_highestMarks)
showHighest_button.pack(side='left', padx=10)

showLowest_button = customtkinter.CTkButton(navbar, text="Show student with lowest marks", font=("Lato", 12, "bold"), command=show_lowestMarks)
showLowest_button.pack(side='left', padx=10)

columns = ('student_id','name','mark1','mark2','mark3','exam_mark','overall','grade')
treeview = ttk.Treeview(root, columns=columns, show='headings')

treeview.heading('student_id', text="Student ID", command=lambda: sortByOrder(treeview, 'student_id', False))
treeview.heading('name', text="Name", command=lambda: sortByOrder(treeview, 'name', False))
treeview.heading('mark1', text="Coursework 1", command=lambda: sortByOrder(treeview, 'mark1', False))
treeview.heading('mark2', text="Coursework 2", command=lambda: sortByOrder(treeview, 'mark2', False))
treeview.heading('mark3', text="Coursework 3", command=lambda: sortByOrder(treeview, 'mark3', False))
treeview.heading('exam_mark', text="Exam Score", command=lambda: sortByOrder(treeview, 'exam_mark', False))
treeview.heading('overall', text="Overall Percentage", command=lambda: sortByOrder(treeview, 'overall', False))
treeview.heading('grade', text="Grade", command=lambda: sortByOrder(treeview, 'grade', False))
treeview.pack(fill='both', expand='true')

regExLogic()

root.mainloop()