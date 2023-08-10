import sys

# Import App funtions:
sys.path.insert(0, './src/functions')
from printtables import myToDoTable, myToDoTableOneDay

print ("To Do List")

instruction = ("\n1. Add ToDo Activities : Add\n2. Mark ToDo Activity Done : Done\n3. Remove ToDo Activity : Remove\n4. Edit ToDo Activity : Edit\n5. Print ToDo Activities : ToDo\n6. Clean ToDo Activities : Clean\n7. Exit Application: Exit")
print(instruction)

# SetupLists and Old Lists
def setupList():
    global todoList
    try:
        #this will run if "Save_todo_list.txt" is in.
        oldToDoList = open("Save_todo_list.txt", "r")
        oldToDoListRead = oldToDoList.read()
        oldToDoListRead = [x for x in oldToDoListRead.split("\n") if len(x) > 1]
        oldToDoListRead = {l.split(":")[0].strip():l.split(":")[1].strip() for l in oldToDoListRead}
        for day in oldToDoListRead:
            if oldToDoListRead[day] == "[]":
                oldToDoListRead[day] = []
            else:
                oldToDoListRead[day] = oldToDoListRead[day].replace("[", "").replace("]", "").replace("'", "")
                oldToDoListRead[day] = [x.strip() for x in oldToDoListRead[day].split(",")]
        todoList = oldToDoListRead
        myToDoTable(todoList)
        oldToDoList.close()
    except:
        #this will run if "Save_todo_list.txt" didn't exists.
        todoList = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
        myToDoTable(todoList)

# SetupOld Lists
setupList()

#Write Text File For ToDo list
def writeToDo(todo_lists):
    if input("Are you sure do you want to write permanently(y/n): ") == "y":
       todoFile = open("Save_todo_list.txt", "w+")
       for day,todo in todo_lists.items():
           todoFile.write("%s : %s\n" % (day, todo))
       todoFile.close()
       setupList()
       print("Successfully Wrote\n")
    else:
        setupList()
        print("Unsuccessfully Wrote\n")

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
