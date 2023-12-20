import mysql.connector
def createDB():
    mydb= mysql.connector.connect(host='localhost', user='root', password='1234')
    cur= mydb.cursor()
    cur.execute('CREATE DATABASE expenseTracker')
createDB()