import sys
import os
import tkinter as tk
import customtkinter as ctk
import copy as cy
import threading as thd

def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Import App funtions:
sys.path.insert(0, resource_path('src\\functions'))
from setuptodolist import setupList, writeToDo #this line 20

app_bg = "#ffffff"
column_bg = "#a0c6f2"
listfg_color = "#323232"

todoList = setupList()
ctk.set_appearance_mode("dark")

class addwindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grab_set()
        self.title("Edit todo Table")
        self.resizable(False, False)
        self.update_idletasks()

        self.doneMarkList = []
        self.entrykeys = []
        self.todoList=setupList()

        var = ctk.StringVar(value = "Sunday")
        self.dayMenu = ctk.CTkOptionMenu(
            self,
            font=("TkMenuFont", 20),
            values=list(self.todoList.keys()),
            anchor="center",
            variable=var,
            command=self.updateWithDay_inTextinput
        )
        self.dayMenu.pack(fill="both", ipady=4, pady=(20,10), padx=15)

        self.textinput_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.textinput_frame.pack(anchor=ctk.CENTER, fill="both", padx=40, pady=0)

        #self.setoldTodo_textinput(self.dayMenu.get())
        self.add_textinput()
        self.add_button = ctk.CTkButton(
            self,
            text="+",
            command=self.add_textinput,
            width=250,
            height=30,
            corner_radius=30,
            font=("TkMenuFont", 18)
        )
        self.add_button.pack(pady=(10,0))

        self.Alert_box(self)
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side=ctk.BOTTOM, pady=10)
        self.apply_button = ctk.CTkButton(button_frame, text="Apply", command=lambda:self.store_Inputvalues())
        self.close_button = ctk.CTkButton(button_frame, text="Close", command=lambda:self.close_window())
        self.apply_button.pack(side=ctk.LEFT, padx=15, pady=15)
        self.close_button.pack(side=ctk.RIGHT, padx=15, pady=15)

        self.updateWithDay_inTextinput(self.dayMenu.get())
        self.textinput_frame.bind("<Configure>", self.set_windowcenter)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.set_Alert("--Add Widnow was Loaded--")

    def updateWithDay_inTextinput(self,var):
        self.currentDay = var
        for childwidget in self.textinput_frame.winfo_children():
            childwidget.destroy()
            self.entrykeys = []
            self.doneMarkList = []
        self.setoldTodo_textinput(self.currentDay)

        if len(self.todoList[self.currentDay]) == 0:
            self.add_textinput()
        self.set_Alert(self.currentDay)

    def add_textinput(self, oldTodo = None):
        if len(self.entrykeys) < 10:
            frame = ctk.CTkFrame(self.textinput_frame, fg_color= "transparent")
            frame.pack(pady=(15,0))

            textinput = ctk.CTkEntry(frame, placeholder_text="Enter your Todo", justify=ctk.CENTER, width=250, height=30, corner_radius=30)
            textinput.pack(side=ctk.LEFT, pady=0)
            if oldTodo is not None:
                textinput.insert(0, string = oldTodo)

            remove_button = ctk.CTkButton(frame, text="X", command=lambda:self.remove_textinput(frame, textinput), width=30, height=30, corner_radius=30)
            remove_button.pack(side=ctk.LEFT, padx=(10, 0), pady=0)

            self.entrykeys.append(textinput)
        else:
            self.set_Alert("--Maxmum List Size is 10--")

    def remove_textinput(self, frame, textinput):
        if textinput in self.entrykeys:
            removeValue = textinput.get()
            try:
                self.todoList[self.currentDay].remove(removeValue)
            except:
                pass
            frame.pack_forget()
            frame.destroy()
            try:
                self.doneMarkList.remove(removeValue)
            except:
                pass
            self.entrykeys.remove(textinput)

            self.set_Alert("--Remove Success--")
        else:
            self.set_Alert(f"--Value didn't exists in entry list--\n--Remove Unsuccess--")

    def store_Inputvalues(self):
        self.inputtext = cy.deepcopy(self.todoList)
        self.inputtext[self.currentDay].clear()
        for key in self.entrykeys:
            inputvalue = key.get()
            self.inputtext[self.currentDay].append(inputvalue)
        for value in self.doneMarkList:
            indexNum = self.inputtext[self.currentDay].index(value)
            self.inputtext[self.currentDay][indexNum] = "!" + self.inputtext[self.currentDay][indexNum]
        self.todoList = self.inputtext
        writeToDo(self.inputtext)
        self.set_Alert("--Wrote is success--\n--Todo List Store Success--")

    def setoldTodo_textinput(self, day):
        self.todoList = setupList()
        for items in self.todoList[day]:
            if items[0] == "!":
                items = items[1:]
                self.doneMarkList.append(items)
            self.add_textinput(items)

    #def checkExists(self):

    def set_windowcenter(self, event):
        x = self.winfo_width()
        y = self.winfo_width() + 300
        center = f"{(self.winfo_screenwidth()//2) - (x//2)}+{(self.winfo_screenheight()//2) - (y//2)}"
        self.geometry(f"{x}x{y}+{center}")

    def close_window(self):
        self.destroy()

    def Alert_box(self, frame):
        self.alert = ctk.CTkLabel(frame, text="Working", text_color="#fb0019")
        self.alert.pack(fill=ctk.X, side=ctk.BOTTOM, pady=5)
    def set_Alert(self, text):
        self.alert.configure(text=text)
        self.setTimer(self.Alert)
    def Alert(self):
        self.alert.configure(text="")
    def setTimer(self, function, time=5.0):
        timer = thd.Timer(time,function)
        timer.start()

#    def run_once(f):
#        def wrapper(*args,**kwargs):
#            if not wrapper.has_run:
#                wrapper.has_run=True
#                return f(*args, **kwargs)
#        wrapper.has_run = False
#        return wrapper
#    @run_once
#    def run_centerwindow(self):
#
#        print("OK")

class Todo_App(ctk.CTk):
    global todoList
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ToDo App 1.0v")
        self.resizable(True, True)
        #self.eval("tk::PlaceWindow . center")

        self.todoList = setupList()

        self.menu_bar()
        self.make_todoTable()

        self.button_frame = ctk.CTkFrame(self, height = 100)
        self.button_frame.pack(fill = "both")
        #self.button_frame.pack_propagate(False)

        self.addbutton = ctk.CTkButton(
            self.button_frame,
            text = "Add All",
            font = ("TkHeadingFont", 18),
            text_color = "white",
            cursor = "hand2",
            command = self.open_Addwindow,
            corner_radius=20
        )
        self.addbutton.pack(side=ctk.LEFT, padx=20, pady = 20)

        self.refreshButton = ctk.CTkButton(
            self.button_frame,
            text="Refresh",
            font=("TkHeadingFont", 18),
            text_color="white",
            cursor="hand2",
            command=self.refresh_todoTable,
            corner_radius = 20
        )
        self.refreshButton.pack(side=ctk.LEFT, padx=20, pady=20)

        self.delete_All = ctk.CTkButton(
            self.button_frame,
            text="Delete All",
            font=("TkHeadingFont", 18),
            text_color="white",
            cursor="hand2",
            command=self.delete_todoList,
            corner_radius=20
        )
        self.delete_All.pack(side=ctk.RIGHT, padx=20, pady=20)

        self.Addwindow = None

        self.todo_table.bind('<Configure>', self.set_geometry)
        self.protocol("WM_DELETE_WINDOW", self.exit_App)

        self.alert.configure(text="--App is Started--")
        self.setTimer(self.Alert)

    def make_todoTable(self):
        self.todo_table = ctk.CTkFrame(self, width=800, height=800, border_color="#202121", border_width=2, corner_radius=30)
        self.todo_table.pack(fill = "both", padx = 20, pady = 20)
        #self.todo_table.pack_propagate(False)

        self.fillblanktodolist = setupList()

        maxcolumns = 0
        for day in self.fillblanktodolist:
            if maxcolumns < len(self.fillblanktodolist[day]):
                maxcolumns = len(self.fillblanktodolist[day])

        maxtodo = 0
        for day in self.fillblanktodolist:
            if maxtodo < len(day):
                maxtodo = len(day)
            for todo in self.fillblanktodolist[day]:
                if maxtodo < len(todo):
                    maxtodo = len(todo)

        bpadyTrue = True
        for i, day in enumerate(self.fillblanktodolist):
            if i >=4:
                if not len(self.fillblanktodolist[day]) == 0:
                    bpadyTrue = False
                    break

        for i, day in enumerate(self.fillblanktodolist):
            tableBpad = 0
            if i >= 4:
                brow = maxcolumns + 1
                i -= 4
                if bpadyTrue:
                    bpady = 15
                else:
                    bpady = 5

                for h in list(self.fillblanktodolist.keys())[4:]:
                    if tableBpad < len(self.fillblanktodolist[h]):
                        tableBpad = len(self.fillblanktodolist[h])
            else:
                brow = 0
                bpady= 5
            if i == 3:
                lpadx = 5
            else:
                lpadx = 0
            if i == 0:
                fpadx = 15
            else:
                fpadx = 0

            self.tododay_label = ctk.CTkLabel(
                self.todo_table,
                text=day,compound=ctk.BOTTOM,
                fg_color=listfg_color,
                font=("TkMenuFont", 24),
                width=maxtodo*12,
                height=1,
                corner_radius=20
            )
            self.tododay_label.grid(row=0 + brow, column=i, ipadx = 10, ipady = 10, padx = (fpadx, 10 + lpadx ), pady = (15, bpady ))

            for x, value in enumerate(self.fillblanktodolist[day]):
                bpady = 0
                if brow != 0:
                    if tableBpad == len(self.fillblanktodolist[day]):
                        if x == len(self.fillblanktodolist[day]) -1:
                            bpady = 15
                    else:
                        bpady = 0
                else:
                    bpady = 0
                if value[0] == "!":
                    doneMark, value = True, value[1:]
                else:
                    doneMark = False

                self.todo_label = ctk.CTkLabel(
                    self.todo_table,
                    text=value,
                    fg_color=listfg_color,
                    bg_color="transparent",
                    font=("TkMenuFont", 20),
                    width=maxtodo*12,
                    height=1,
                    corner_radius=20
                )
                self.todo_label.grid(row=x + 1 + brow, column=i, ipadx = 8, ipady = 6, padx = (fpadx, 10 ), pady = (3, bpady))

                if doneMark:
                    self.todo_label.configure(font=("TkMenuFont", 20, "overstrike"))

                self.todo_label.bind("<Enter>", lambda event, todo_label=self.todo_label: self.hover_LabelEnter(event, todo_label))
                self.todo_label.bind("<Leave>", lambda event, todo_label=self.todo_label: self.hover_LabelLeave(event, todo_label))
                self.todo_label.bind("<Button-1>", lambda event, todo_label=self.todo_label, day=self.tododay_label: self.mark_DoneTodo(event, todo_label, day))
                self.todo_label.bind("<Button-3>", lambda event, todo_label=self.todo_label, day=self.tododay_label: self.unmark_DoneTodo(event, todo_label, day))

    def open_Addwindow(self):
        if self.Addwindow is None or not self.Addwindow.winfo_exists():
            self.Addwindow = addwindow(self)
        else:
            self.Addwindow.focus()

    def refresh_todoTable(self):
        self.todoList = setupList()
        self.todo_table.destroy()
        self.make_todoTable()
        self.button_frame.pack_forget()
        self.button_frame.pack(fill="both")

        self.alert.configure(text="--Refresh Success--")
        self.setTimer(self.Alert)

    def delete_todoList(self):
        for day in self.todoList:
            self.todoList[day] = []
        writeToDo(self.todoList)
        self.refresh_todoTable()

        self.alert.configure(text="--All Todo Lists Deleted--")
        self.setTimer(self.Alert)
        pass

    def set_geometry(self, event):
        x = self.winfo_width()
        y = self.winfo_height()
        center = f"{(self.winfo_screenwidth()//2) - (x//2)}+{(self.winfo_screenheight()//2) - (y//2)}"
        self.geometry(f"{x}x{y}+{center}")

    def menu_bar(self):
        menubar = ctk.CTkFrame(self, height=30)
        menubar.pack(fill="both")

        self.file_Option(menubar)
        self.display_Alert(menubar)

    def file_Option(self, frame):
        options = ["Add All", "Refresh", "Delete All"]
        var = ctk.StringVar(value = "File")
        file = ctk.CTkOptionMenu(
            frame,
            values=options,
            variable= var,
            anchor="center",
            command=self.trigger_commands,
            width=80,
            corner_radius=0
        )
        file.pack(side = ctk.LEFT)

    def display_Alert(self, frame):
        self.alert = ctk.CTkLabel(frame, text="", text_color="#fb0019")
        self.alert.pack(side = ctk.RIGHT, padx=(0,30))

    def trigger_commands(self, value):
        if value == "Add All":
            self.open_Addwindow()
        elif value == "Refresh":
            self.refresh_todoTable()
        elif value == "Delete All":
            self.delete_todoList()
        else:
            self.alert.configure(text="! Somthing Wrong !")
            self.setTimer(self.Alert)

    def exit_App(self):
        self.destroy()
        exit()

    def mark_DoneTodo(self, event, label, day):
        try:
            label.configure(font = ("TkMenuFont", 20, "overstrike"))
            label.configure(fg_color="#322222")
            index = todoList[day.cget("text")].index(label.cget("text")) #get Index Number for the todoList
            todoList[day.cget("text")][index] = "!" + label.cget("text") #add mark as done todoList

            writeToDo(todoList, False)
            self.alert.configure(text="--Write is Success--")
            self.setTimer(self.Alert)

        except:
            self.alert.configure(text="! Already Mark as Done !")
            self.setTimer(self.Alert)

    def unmark_DoneTodo(self, event, label, day):
        try:
            label.configure(font = ("TkMenuFont", 20))
            label.configure(fg_color="#2b3c2b")
            index = todoList[day.cget("text")].index("!"+label.cget("text")) #get Index Number for the todoList
            todoList[day.cget("text")][index] = label.cget("text") #remove mark as undone todoList

            writeToDo(todoList, False)
            self.alert.configure(text="--Write is Success--")
            self.setTimer(self.Alert)

        except:
            self.alert.configure(text="Already Unmark")
            self.setTimer(self.Alert)

    def hover_LabelEnter(self, event, label):
        label.configure(fg_color="#888888")
    def hover_LabelLeave(self, event, label):
        label.configure(fg_color=listfg_color)

    def Alert(self):
        self.alert.configure(text="")

    def setTimer(self, function, time=5.0):
        timer = thd.Timer(time,function)
        timer.start()


App = Todo_App()
App.mainloop()

exit()