import sys
import tkinter as tk

# Import App funtions:
sys.path.insert(0, './src/functions')
from printtables import myToDoTable, myToDoTableOneDay
from setuptodolist import setupList, writeToDo

# SetupOld Lists
todoList = setupList()

app_bg = "#ffffff"
column_bg = "#a0c6f2"


gui_V = input("Do you wanna run GUI Version (Y/n): ")
if True:

    root = tk.Tk()
    root.title("ToDo App")
    root.geometry('500x500')
    root.eval("tk::PlaceWindow . center")

    frame1 = tk.Frame(root, width=800, height=400, bg=app_bg)
    frame1.grid(row=0, column=0)
    frame1.pack_propagate(False)

    for i, day in enumerate(todoList):
        tk.Label(frame1, text=day, bg = column_bg, font=("TkMenuFont", 14), width=16, height=1, ipadx = 10).grid(row=1, column=i)
        for x, value in enumerate(todoList[day]):
            tk.Label(frame1, text=value, bg = column_bg, font=("TkMenuFont", 12), width=20, height=1).grid(row=x + 2, column=i)

    tk.Button(
        frame1,
        text = "Print Todo Table",
        font = ("TkHeadingFont", 20),
        bg = "#28393a",
        fg = "white",
        cursor = "hand2",
        activebackground = "#babee2",
        activeforeground = "black",
        command = lambda:myToDoTable(todoList)
    ).pack(pady=20)




    root.mainloop()
    exit()

print ("To Do List")
instruction = ("\n1. Add ToDo Activities : Add\n2. Mark ToDo Activity Done : Done\n3. Remove ToDo Activity : Remove\n4. Edit ToDo Activity : Edit\n5. Print ToDo Activities : ToDo\n6. Clean ToDo Activities : Clean\n7. Exit Application: Exit")
print(instruction)


# getToDoList can return day and row-number of todoList within lists
def getToDoList():
    while True:
        command = list(input("Enter which day, which row:\nDay:Row-number - ").split(":"))
        if len(command) != 2:
            print ("Enter only giviven format (Day:Row-number)\n")
            continue
        command[0] = command[0].title()
        command[1] = int(command[1]) - 1
        return command

while True:
    #Enter command and empty input can't enter
    while True:
        command = input("Enter The Command: ").lower()
        if command == '':
            continue
        break

    # Command Activities
    if command == "add":
        # Input todo list and add them to the "todoList"
        while True:
            day, *todo = list(input("Enter ToDo Activity (Day:todolist seperate by :) - ").split(":"))
            day = day.title()
            valu = False
            # Cheking day in todoList:
            for dayVal in todoList:
                if dayVal == day:
                    valu = True
                    break
            if valu == True:
                break
            print("Enter Validated Day Name")

        for todo_activity in todo:
            todoList[day].append(todo_activity)
        writeToDo(todoList)
    elif command == "done":
        print("coming soon")
    elif command == "edit":
        # Edit added Todo list
        day,rowNum = getToDoList()
        print("You going to change this work - ", todoList[day][rowNum])
        todoList[day][rowNum] = input("Enter your Changes todo - ")
        writeToDo(todoList)
        print ("Update Success\n")
    elif command == "todo":
        which_day = input("Which day do you want print(If you want all days Enter \"all\": ")
        if which_day == "all":
            myToDoTable(todoList)
        else:
            myToDoTableOneDay(which_day, todoList)
    elif command == "remove":
        day,rowNum = getToDoList()
        print(todoList[day][rowNum])
        todoList[day].remove(todoList[day][rowNum])
        writeToDo(todoList)
    elif command == "clean":
        day = input("Which day in the Todolist do you want to clean?\n(set (all) to clean all days at ones) - ")
        if day.lower() == "all":
            todoList = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
            writeToDo(todoList)
        else:
            todoList[day.title()] = []
            writeToDo(todoList)
    elif command == "exit":
        exit()
    else:
        print("Enter the correct commands from instructions")
