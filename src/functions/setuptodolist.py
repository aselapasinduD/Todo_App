import customtkinter as ctk
import os
import sys

def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

sys.path.insert(0, resource_path('.'))

root = ctk.CTk()
root.withdraw()

ctk.set_appearance_mode("dark")

def setupList():
    try:
        # Open and read the file
        with open("Save_todo_list.txt", "r") as oldToDoList:
            oldToDoListRead = oldToDoList.read().split("\n")
        oldToDoListRead = [x for x in oldToDoListRead if len(x) > 1]
        oldToDoListRead = {
            l.split(":", 1)[0].strip(): l.split(":", 1)[1].strip() for l in oldToDoListRead
        }

        # Convert string representations to lists
        for day in oldToDoListRead:
            if oldToDoListRead[day] == "[]":
                oldToDoListRead[day] = []
            else:
                oldToDoListRead[day] = oldToDoListRead[day].replace("[", "").replace("]", "").replace("'", "")
                oldToDoListRead[day] = [x.strip() for x in oldToDoListRead[day].split(",")]

        todoList = oldToDoListRead
        
    except:
        # Initialize with default empty lists if file does not exist
        todoList = {
            "Sunday": [], "Monday": [], "Tuesday": [], "Wednesday": [],
            "Thursday": [], "Friday": [], "Saturday": []
        }
    return todoList


#Write Text File For ToDo list
class writeToDo():
    def __init__(self, todo_lists, popArlet=True):
        self.todo_lists = todo_lists
        self.alert_box = ctk.CTkToplevel(root)
        self.alert_box.geometry("320x100")
        self.alert_box.title("Save")
        if popArlet:
            alert = ctk.CTkLabel(self.alert_box, text="Are you sure!\nDo you want to permanently write(This can't be undo)")
            alert.pack(fill="both", side="top", expand=True, pady=10, padx=10)

            button_yes = ctk.CTkButton(self.alert_box, text="Yes", command=self.press_Yes, width=80)
            button_no = ctk.CTkButton(self.alert_box, text="No", command=self.press_No, width=80)
            button_yes.pack(side=ctk.RIGHT, padx=(20,40), pady=10)
            button_no.pack(side=ctk.LEFT, padx=(40,20), pady=10)
        else:
            self.press_Yes()

    def press_Yes(self):
        self.todoFile = open(resource_path("Save_todo_list.txt"), "w+")
        for day,todo in self.todo_lists.items():
            self.todoFile.write("%s : %s\n" % (day, todo))
        self.todoFile.close()
        setupList()
        self.alert_box.destroy()

    def press_No(self):
        setupList()
        self.alert_box.destroy()