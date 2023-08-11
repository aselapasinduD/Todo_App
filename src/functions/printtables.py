import copy
from prettytable import PrettyTable

# Fill the blanks in todo list with this (-):
def fillBlankToDo(todo_lists):
    newtodo_lists = copy.deepcopy(todo_lists)
    maxLenInList = 0
    for day in newtodo_lists:
        if maxLenInList < len(newtodo_lists[day]):
            maxLenInList = len(newtodo_lists[day])
    for day in todo_lists:
        newmaxLenInList = maxLenInList - len(newtodo_lists[day])
        if newmaxLenInList != 0 and newmaxLenInList > 0:
            for i in range(newmaxLenInList):
                newtodo_lists[day].append("-")
    return newtodo_lists

# PrettyTable For ToDo lists:
def myToDoTable(todo_lists):
    myTable = PrettyTable()
    newtodo_lists = fillBlankToDo(todo_lists)
    myTable.add_column("Sunday", newtodo_lists["Sunday"])
    myTable.add_column("Monday", newtodo_lists["Monday"])
    myTable.add_column("Tuesday", newtodo_lists["Tuesday"])
    myTable.add_column("Wednesday", newtodo_lists["Wednesday"])
    myTable.add_column("Thursday", newtodo_lists["Thursday"])
    myTable.add_column("Friday", newtodo_lists["Friday"])
    myTable.add_column("Saturday", newtodo_lists["Saturday"])
    #myTable.add_autoindex("rowNumber")
    print(myTable, "\n")
    return myTable

def myToDoTableOneDay(day, todo_list):
    myTableOneDay = PrettyTable()
    day = day.title()
    myTableOneDay.add_column(day, todo_list[day])
    print(myTableOneDay, "\n")

