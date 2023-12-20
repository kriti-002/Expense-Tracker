import mysql.connector

def createTable():
    mydb= mysql.connector.connect(host='localhost', user='root', password='1234', database='expenseTracker')
    cur= mydb.cursor()
    cur.execute('CREATE TABLE EXPENSES(ID int PRIMARY KEY NOT NULL AUTO_INCREMENT, Date DATE, Payee VARCHAR(100), Description VARCHAR(100), Amount FLOAT, ModeOfPayment VARCHAR(100))')

createTable()