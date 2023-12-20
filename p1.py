import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from tkcalendar import DateEntry

win= Tk()
win.title("Expense Tracker")
win.geometry("1200x600")
win.resizable(0,0)


#connection to the database
mydb= mysql.connector.connect(host='localhost', user='root', password='1234', database='expenseTracker')
curr= mydb.cursor()


#functionalities
def addExpense():
    global curr, mydb
    if not date.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():
        messagebox.showerror('Error', "Please fill all the missing fields!")
    else:
        statement= 'INSERT INTO expenses(Date, Payee, Description, Amount, ModeOfPayment) VALUES (%s, %s, %s, %s, %s)'
        tup=(date.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get())
        curr.execute(statement, tup)
        mydb.commit()
        getAllExpense()
        messagebox.showinfo("Success!", "Expense added successfully!")
        date.get_date= datetime.datetime.today()
        payee.set('')
        description.set('')
        amount.set(0.0)
        modeOfPayment.set('Cash')

def getAllExpense():
    global curr, table
    table.delete(*table.get_children())
    statement= 'SELECT * FROM EXPENSES'
    curr.execute(statement)
    res= curr.fetchall()
    #print(res)
    for values in res:
        table.insert('', END, values=values)

def deleteExpense():
    global mydb, curr, table
    if not table.selection():
        messagebox.showerror('No record selected!', 'Please select a record to delete!')
        return
    currExpense= table.item(table.focus())
    val= currExpense['values']
    check= messagebox.askyesno("Warning", "Do you really want to delete this record?")
    if check:
        statement='DELETE FROM EXPENSES WHERE ID=%s'
        curr.execute(statement, (val[0], ))
        mydb.commit()
        getAllExpense()
        messagebox.showinfo("Success!", "Deleted!")

def totalExpense():
    global curr
    statement= 'SELECT SUM(Amount) from expenses'
    curr.execute(statement)
    sum= curr.fetchall()[0][0]
    if sum!= None:
        messagebox.showinfo("Success!", f"Total Sum of Expense Amount recorded:{sum}")
    else:
        messagebox.showinfo("Success!", f"Total Sum of Expense Amount recorded:{0.0}")

def deleteAllRecords():
    global mydb,curr
    st='select * from expenses'
    curr.execute(st)
    res= curr.fetchall()
    if len(res)==0:
        messagebox.showerror("Error", "There is no record in the table.")
    else:
        option= messagebox.askyesno("Warning", "Do you really want to delete all the records?")
        if option:
            statement='DELETE FROM expenses'
            curr.execute(statement)
            mydb.commit()
            messagebox.showinfo("Success!", "All the records are deleted.")
            getAllExpense()

def updateRecord():
    global mydb, curr, table
    st='select * from expenses'
    curr.execute(st)
    res= curr.fetchall()
    if len(res)==0:
        messagebox.showerror("Error", "There is no record in the table.")
    else:
        if not table.selection():
            messagebox.showerror('No record selected!', 'Please select a record to update!')
            return
        currExpense= table.item(table.focus())
        val= currExpense['values']
        date.set_date(datetime.date(int(val[1][:4]), int(val[1][5:7]), int(val[1][8:])))
        payee.set(val[2])
        description.set(val[3])
        amount.set(val[4])
        modeOfPayment.set(val[5])
        def update():
            global mydb, curr
            if not date.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():
                    messagebox.showerror('Error', "Please fill all the missing fields!")
            else:
                statement='update expenses set Date=%s, Payee=%s, Description=%s, Amount=%s, ModeOfPayment=%s where ID=%s'
                values=(date.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get(), val[0])
                curr.execute(statement, values)
                mydb.commit()
                messagebox.showinfo("Success", "The records have been updated!")
                date.get_date= datetime.datetime.today()
                payee.set('')
                description.set('')
                amount.set(0.0)
                modeOfPayment.set('Cash')
                getAllExpense()
                editButton.destroy()
        editButton= Button(dataEntryFrame,text="Edit Expense" , command=update, width=36)
        editButton.place(x=10, y=375)

#initialization
payee= StringVar()
description= StringVar()
amount= DoubleVar()
modeOfPayment= StringVar(value='Cash')

dataEntryFrame = Frame(win)
dataEntryFrame.place(x=0, y=30, relheight=0.95, relwidth=0.25)

buttonFrame = Frame(win)
buttonFrame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.21)

treeFrame = Frame(win)
treeFrame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)


#Form
Label(dataEntryFrame, text='Created Date (MM/DD/YY)  :').place(x=10, y=50)
date = DateEntry(dataEntryFrame, date=datetime.datetime.now().date())
date.place(x=180, y=50)

Label(dataEntryFrame, text='Payee  :').place(x=10, y=230)
Entry(dataEntryFrame, width=40, text=payee).place(x=10, y=260)

Label(dataEntryFrame, text='Description  :').place(x=10, y=100)
Entry(dataEntryFrame, width=40, text=description).place(x=10, y=130)

Label(dataEntryFrame, text='Amount  :').place(x=10, y=180)
Entry(dataEntryFrame, width=20, text=amount).place(x=160, y=180)

Label(dataEntryFrame, text='Mode of Payment  :').place(x=10, y=300)
dd1 = OptionMenu(dataEntryFrame, modeOfPayment, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay'])
dd1.configure(width=16)
dd1.place(x=150, y=305)

Button(dataEntryFrame,text="Add Expense" , command=addExpense, width=36).place(x=10, y=375)

#Additional Features
Button(buttonFrame, text="Get Total Amount of All Expenses", command=totalExpense).place(x=30, y=5)
Button(buttonFrame, text="Delete All Records", command=deleteAllRecords).place(x=250, y=5)
Button(buttonFrame, text="Delete Selected Expense Record", command=deleteExpense).place(x=450, y=5)
Button(buttonFrame, text="Update Selected Record", command=updateRecord).place(x=700, y=5)


table = ttk.Treeview(treeFrame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'))

X_Scroll = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroll = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroll.pack(side=BOTTOM, fill=X)
Y_Scroll.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroll.set, xscrollcommand=X_Scroll.set)

table.heading('ID', text='ID', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=30, stretch=NO)
table.column('#2', width=95, stretch=NO)  
table.column('#3', width=150, stretch=NO) 
table.column('#4', width=300, stretch=NO)  
table.column('#5', width=135, stretch=NO)  
table.column('#6', width=130, stretch=NO)  

table.place(relx=0, y=0, relheight=1, relwidth=1)

getAllExpense()
win.update()
win.mainloop()


