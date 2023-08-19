from printtables import myToDoTable
import customtkinter as ctk

root = ctk.CTk()
root.withdraw()

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
        #this will run if "Save_todo_list.txt" didn't exists.oldToDoList
        todoList = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
        myToDoTable(todoList)
    return todoList

#Write Text File For ToDo list
class writeToDo():
    def __init__(self,todo_lists):
        self.todo_lists = todo_lists
        self.alert_box = ctk.CTkToplevel(root)
        self.alert_box.geometry("200x200")
        self.alert_box.title("Save")

        alert = ctk.CTkLabel(self.alert_box, text="Are you sure! do you want to permanently write(This can't be undo)")
        alert.pack()

        button_yes = ctk.CTkButton(self.alert_box, text="Yes", command=self.press_Yes, width=80)
        button_no = ctk.CTkButton(self.alert_box, text="No", command=self.press_No, width=80)
        button_yes.pack(side=ctk.RIGHT, padx=10, pady=10)
        button_no.pack(side=ctk.LEFT, padx=10, pady=10)

    def press_Yes(self):
        self.todoFile = open("Save_todo_list.txt", "w+")
        for day,todo in self.todo_lists.items():
            self.todoFile.write("%s : %s\n" % (day, todo))
        self.todoFile.close()
        setupList()
        print("Successfully Wrote\n")
        self.alert_box.destroy()

    def press_No(self):
        setupList()
        print("Unsuccessfully Wrote\n")
        self.alert_box.destroy()

