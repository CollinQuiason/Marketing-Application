from tkinter import *

#Sample sql call

import mysql.connector


mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="root", # this will be different depening on your database
 database="Project2",
 port = 8889
)

#mycursor = mydb.cursor()
#sqlstatement = "SELECT * FROM users WHERE UserFirstName = %(name)s;"
#mycursor.execute(sqlstatement, {"name": "Connor"})

#myresult = mycursor.fetchall()

#for x in myresult:
#  print(x)



def login_verify():
    username = username_verify.get()
    user_type = user_type_verify.get()
    username_login_entry.delete(0, END)
    my_cursor = mydb.cursor()

    if user_type == 'USER' :
        sqlstatement = "SELECT User_ID FROM Users WHERE User_ID = %(User_ID)s;"
        my_cursor.execute(sqlstatement, {"User_ID": username})
        list_of_users = my_cursor.fetchall()
        if username in list_of_users :
            login_success_user()
        else :
            user_not_found()


    else :
        sqlstatement = "SELECT User_ID FROM Moderators WHERE User_ID = %(User_ID)s;"
        my_cursor.execute(sqlstatement, {"User_ID": username})
        list_of_moderators = my_cursor.fetchall()
        if username in list_of_moderators :
            login_success_moderators()
        else :
            moderator_not_found()

def login_success_user():

def login_success_moderators():

def user_not_found():

def moderator_not_found():



#todo define the above classes


# main page

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")

    global username_verify
    global user_type_verify

    username_verify = StringVar()

    global username_login_entry
    global user_type_entry


    # create a Form label
    form_label = Label(text="Choose Login", bg="red", width="300", height="2", font=("Calibri", 22))
    form_label.pack()
    Label(text="").pack()

    # Set username label
    username_label = Label(main_screen, text="Enter your Username and select User Type ")
    username_label.pack()

    # Set username entry
    username_login_entry = Entry(main_screen, textvariable=username_verify)
    username_login_entry.pack()

    # User Selection
    user_type_verify = StringVar(main_screen)
    user_type_verify.set("USER")  # default value
    user_type_entry = OptionMenu(main_screen, user_type_verify, "USER", "MODERATOR")
    user_type_entry.pack()

    # create Login Button
    login_button = Button(text="Login", height="2", width="30", command= login_verify )
    login_button.pack()
    Label(text="").pack()

    main_screen.mainloop()


main_account_screen()
