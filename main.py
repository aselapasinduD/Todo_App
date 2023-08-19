import sys
import tkinter as tk
import customtkinter as ctk
import copy as cy
import threading as thd

# Import App funtions:
sys.path.insert(0, './src/functions')
from printtables import myToDoTable, myToDoTableOneDay, fillBlankToDo
from setuptodolist import setupList, writeToDo

# SetupOld Lists

app_bg = "#ffffff"
column_bg = "#a0c6f2"

gui_V = input("Do you wanna run GUI Version (Y/n): ")
todoList = setupList()
ctk.set_appearance_mode("system")

class addwindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.geometry("500x500")
        self.grab_set()
        self.title("Edit todo Table")
        self.resizable(False, False)
        self.update_idletasks()

        self.refresh_todoTable = Todo_App()

        self.entrykeys = []
        self.todoList=setupList()
        print(f"refreshed todoList = {self.todoList}\n")

        #self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        #self.label.pack(pady = 10)
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

        self.setoldTodo_textinput(self.dayMenu.get())
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

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side=ctk.BOTTOM, pady=10)
        self.apply_button = ctk.CTkButton(button_frame, text="Apply", command=lambda:self.store_Inputvalues())
        self.close_button = ctk.CTkButton(button_frame, text="Close", command=self.close_window)
        self.apply_button.pack(side=ctk.LEFT, padx=15, pady=15)
        self.close_button.pack(side=ctk.RIGHT, padx=15, pady=15)

        self.updateWithDay_inTextinput(self.dayMenu.get())
        self.textinput_frame.bind("<Configure>", self.set_windowcenter)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        print("----Add Widnow was Loaded----")

    def updateWithDay_inTextinput(self,var):
        self.currentDay = var
        for childwidget in self.textinput_frame.winfo_children():
            childwidget.destroy()
            self.entrykeys = []
        self.setoldTodo_textinput(self.currentDay)

        if len(self.todoList[self.currentDay]) == 0:
            self.add_textinput()
        print(self.currentDay)

    def add_textinput(self, oldTodo = None):
        if len(self.entrykeys) < 10:
            frame = ctk.CTkFrame(self.textinput_frame, fg_color= "transparent")
            frame.pack(pady=(15,0))

            textinput = ctk.CTkEntry(frame, placeholder_text="Enter your Todo", justify=ctk.CENTER, width=250, height=30, corner_radius=30)
            textinput.pack(side=ctk.LEFT, pady=0)
            if oldTodo is not None:
                textinput.insert(0, string = oldTodo)
            #else:
                #textinput.insert(0, string = "New String")

            remove_button = ctk.CTkButton(frame, text="X", command=lambda:self.remove_textinput(frame, textinput), width=30, height=30, corner_radius=30)
            remove_button.pack(side=ctk.LEFT, padx=(10, 0), pady=0)

            self.entrykeys.append(textinput)
        else:
            print("Maxmum List Size is 10")

    def remove_textinput(self, frame, textinput):
        print(f"----Removing {textinput.get()}----")
        if textinput in self.entrykeys:
            try:
                self.todoList[self.currentDay].remove(textinput.get())
            except:
                pass
            frame.pack_forget()
            frame.destroy()
            self.entrykeys.remove(textinput)
            print("----Remove Success----")
        else:
            print(f"-----{textinput} Entry Key didn't exists in entry list----\n----Remove Unsuccess----")

    def store_Inputvalues(self):
        print("----Todo list Storing----")
        self.inputtext = cy.deepcopy(self.todoList)
        for key in self.entrykeys:
            inputvalue = key.get()
            self.inputtext[self.currentDay].append(inputvalue)
        print("Store = ",self.todoList)
        todoList = setupList()
        print("After Setup Store = ",self.todoList)
        self.todoList = self.inputtext
        writeToDo(self.inputtext)
        #Todo_App.refresh_todoTable()
        print("----Todo List Store Success----")

    def setoldTodo_textinput(self, day):
        self.todoList = setupList()
        for items in self.todoList[day]:
            self.add_textinput(items)

    #def checkExists(self):

    def set_windowcenter(self, event):
        x = self.winfo_width()
        y = self.winfo_width() + 200
        center = f"{(self.winfo_screenwidth()//2) - (x//2)}+{(self.winfo_screenheight()//2) - (y//2)}"
        self.geometry(f"{x}x{y}+{center}")
        print("----Set Add Window to Center----")

    def close_window(self):
        print("----Closed The Add Window----")
        self.refresh_todoTable.refresh_todoTable()
        self.destroy()

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
        print("----Starting App----")
        self.title("ToDo App")
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
        print("----Started App----")

    def make_todoTable(self):
        print("----Making Todo Table----")
        self.todo_table = ctk.CTkFrame(self, width=800, height=800, border_color="#202121", border_width=2, corner_radius=30)
        self.todo_table.pack(fill = "both", padx = 20, pady = 20)
        #self.todo_table.pack_propagate(False)

        self.fillblanktodolist = setupList()#todoList#fillBlankToDo(todoList, " ")
        print("todoList =",self.todoList)
        print("fillblanktodolist =",self.fillblanktodolist)

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

        listfg_color = "#323232"

        for i, day in enumerate(self.fillblanktodolist):
            tableBpad = 0
            if i >= 4:
                brow = maxcolumns + 1
                i -= 4
                if len(self.fillblanktodolist[day]) == 0:
                    bpady = 15
                else:
                    bpady = 0
                for h in list(self.fillblanktodolist.keys())[4:]:
                    if tableBpad < len(self.fillblanktodolist[h]):
                        tableBpad = len(self.fillblanktodolist[h])
            else:
                brow = 0
                bpady= 0
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

                self.mark_done = ctk.CTkCanvas(self.todo_table, width=maxtodo*12, height=0, bg=listfg_color)
                self.mark_done.grid(row=x + 1 + brow, column=i, ipadx = 8, ipady = 6, padx = (fpadx, 10 ), pady = (3, bpady))

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

                self.mark_done.create_line(0, 10, maxtodo*12, 10, width=2, capstyle="round")

        #self.todo_table.bind('<Configure>', self.set_geometry)
        print("----Successfuly Maded----")

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
        print("refresh =", self.todoList)
        print("----Refresh Success----")

    def delete_todoList(self):
        for day in self.todoList:
            self.todoList[day] = []
        writeToDo(self.todoList)
        self.refresh_todoTable()
        print(self.todoList)
        print("Delete is Successful")
        pass

    def set_geometry(self, event):
        x = self.winfo_width()
        y = self.winfo_height()
        center = f"{(self.winfo_screenwidth()//2) - (x//2)}+{(self.winfo_screenheight()//2) - (y//2)}"
        self.geometry(f"{x}x{y}+{center}")
        print("----Set Main Window to Center----")

    def menu_bar(self):
        menubar = ctk.CTkFrame(self, height=30)
        menubar.pack(fill="both")
        self.file_Option(menubar)
        print("----Menu Bar Loaded----")

    def file_Option(self, frame):
        options = ["Add all", "Refresh"]
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

    def trigger_commands(self, value):
        if value == "Add all":
            self.open_Addwindow()
        elif value == "Refresh":
            self.refresh_todoTable()
        else:
            print("----Somthing Wrong----")
    def exit_App(self):
        self.destroy()
        exit()

App = Todo_App()
App.mainloop()

exit()
