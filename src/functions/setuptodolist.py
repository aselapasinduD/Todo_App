from printtables import myToDoTable

# Setup Lists and Old Lists
def setupList():
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
    return todoList

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

