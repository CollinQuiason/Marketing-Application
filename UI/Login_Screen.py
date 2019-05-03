from tkinter import *

import hashlib, os, uuid, bcrypt



def check_secure_val(salt, password, hashval): #Requires that the 'h' is in the form ("<inputpasswordtocheck>,<hashvalfromDB>")
    rehashval = hash(salt, password)
    if rehashval == hashval:
        return True
    return False
def hash(salt, password):
    #password_salt = uuid.uuid4().hex
    #password_salt = ""
    
    #print(password_salt)
    hash = hashlib.sha512()
    hash.update(('%s%s' % (salt, password)).encode('utf-8'))
    passhash = hash.hexdigest()
    return passhash

def generateSalt():
    return bcrypt.gensalt()


passw = '12345'
password_salt = generateSalt()
password_hash = hash(password_salt, passw)


print(check_secure_val(password_salt, passw, password_hash))




#Sample sql call

import mysql.connector


mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="password", # this will be different depening on your database
 database="Project2",
 port = 3306
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
        flag_user_found = False
        for x in list_of_users:
            if username == x[0]:
                flag_user_found = True
                login_success_user()
        if not flag_user_found:
            user_not_found()

    else :
        sqlstatement = "SELECT User_ID FROM Moderators WHERE User_ID = %(User_ID)s;"
        my_cursor.execute(sqlstatement, {"User_ID": username})
        list_of_moderators = my_cursor.fetchall()
        flag_moderator_found = False
        for x in list_of_moderators:
            if username == x[0]:
                flag_moderator_found = True
                login_success_moderators()
        if not flag_moderator_found:
            moderator_not_found()


def login_success_user():
    global login_success_users_screen
    login_success_users_screen = Toplevel(main_screen)
    login_success_users_screen.title("Success")
    login_success_users_screen.geometry("150x100")
    Label(login_success_users_screen, text="Login Success").pack()
    Button(login_success_users_screen, text="OK", command=delete_login_success_users).pack()

def login_success_moderators():
    global login_success_moderators_screen
    login_success_moderators_screen = Toplevel(main_screen)
    login_success_moderators_screen.title("Success")
    login_success_moderators_screen.geometry("150x100")
    Label(login_success_moderators_screen, text="Login Success").pack()
    Button(login_success_moderators_screen, text="OK", command=delete_login_success_moderators).pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(main_screen)
    user_not_found_screen.title("User Not Found")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
def moderator_not_found():
    global moderator_not_found_screen
    moderator_not_found_screen = Toplevel(main_screen)
    moderator_not_found_screen.title("Moderator Not Found")
    moderator_not_found_screen.geometry("150x100")
    Label(moderator_not_found_screen, text="Moderator Not Found").pack()
    Button(moderator_not_found_screen, text="OK", command=delete_moderator_not_found_screen).pack()

def delete_login_success_users():
    login_success_users_screen.destroy()
    user_screen()

def delete_login_success_moderators():
    login_success_moderators_screen.destroy()
    moderator_screen()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()


def delete_moderator_not_found_screen():
    moderator_not_found_screen.destroy()



def user_screen():
    # todo add stuff
    main_screen.destroy()
    global user_screen
    user_screen = Tk()
    user_screen.geometry("500x300")
    user_screen.title("User Tab")
    form_label = Label(text="User Tab", bg="green", width="300", height="2", font=("Calibri", 22))
    form_label.pack()
    Label(text="").pack()

def moderator_screen():
    # todo add stuff
    main_screen.destroy()
    global moderator_screen
    moderator_screen = Tk()
    moderator_screen.geometry("500x300")
    moderator_screen.title("Moderator Tab")
    form_label = Label(text="Moderator Tab", bg="blue", width="300", height="2", font=("Calibri", 22))
    form_label.pack()
    Label(text="").pack()

# todo define the above classes


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
