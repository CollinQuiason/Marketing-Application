from tkinter import *
from tkinter import ttk


import hashlib
import os
import uuid
import bcrypt



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

# def generateSalt():
#   return bcrypt.gensalt()
#
# passw = '12345'
# password_salt = generateSalt()
# password_hash = hash(password_salt, passw)
#
#
# print(check_secure_val(password_salt, passw, password_hash))




#Sample sql call

import mysql.connector


mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="root", # this will be different depening on your database
 database="Project2",
 port = 8889 #3306 ,
 #auth_plugin='mysql_native_password'
)

#mycursor = mydb.cursor()
#sqlstatement = "SELECT * FROM users WHERE UserFirstName = %(name)s;"
#mycursor.execute(sqlstatement, {"name": "Connor"})

#myresult = mycursor.fetchall()

#for x in myresult:
#  print(x)



def login_verify():
    username = username_verify.get()
    password = userpassword_verify.get()
    user_type = user_type_verify.get()
    username_login_entry.delete(0, END)
    my_cursor = mydb.cursor()

    if user_type == 'USER' :
        sqlstatement = "SELECT User_ID, UserPassword, UserSalt FROM Users WHERE User_ID = %(User_ID)s;"
        my_cursor.execute(sqlstatement, {"User_ID": username})
        list_of_users = my_cursor.fetchall()
        flag_user_found = False
        for x in list_of_users:
            if (username == x[0] and check_secure_val(x[2], password, x[1])):
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

def add_advertisement():
    # todo add functionality
    print('add advertisement')

def user_screen():
    # todo add stuff

    def search_button_click():
        # todo add functionality
        print("Search Button Clicked")

    def edit_button_click():
        # todo add functionality
        print('Edit button clicked')
    def delete_button_click():
        # todo add functionality
        print('delete button clicked')

    main_screen.destroy()
    global user_screen
    user_screen = Tk()  # Create instance
    user_screen.geometry("850x600")
    user_screen.title("User Tab")  # Add a title

    global search_verify1
    search_verify1 = StringVar(user_screen)

    Label(text="User Tab", bg="green", width="300", height="2", font=("Calibri", 22)).pack()
    Label(text="").pack()
    Button(user_screen, text="Add Advertisements", command=add_advertisement, width=40, height=4).pack()

    tab_control = ttk.Notebook(user_screen)  # Create Tab Control
    tab1 = ttk.Frame(tab_control)  # Create a tab
    tab2 = ttk.Frame(tab_control)  # Create a tab

    tab_control.add(tab1, text='Advertisements ')  # Add the tab
    tab_control.add(tab2, text='My Advertisements')  # Add the tab
    ## Advertisements tab

    optionsframe = ttk.Frame(tab1)
    optionsframe.pack(side="top", fill="x")  # Split tab into two frames top and bottom
    tableframe = ttk.Frame(tab1)  # Split tab into two frames top and bottom
    tableframe.pack(side="bottom", fill="x")

    optionsframe.columnconfigure(0, weight=1)
    optionsframe.columnconfigure(1, weight=1)
    optionsframe.columnconfigure(2, weight=1)
    optionsframe.columnconfigure(3, weight=1)

    category_options = [  # Category options menu
        "All",
        "Cars and Trucks",
        "Housing",
        "Electronics",
        "Child Care"
    ]
    category_verify = StringVar(optionsframe)
    category_verify.set(category_options[0])  # default value
    category_entry = OptionMenu(optionsframe, category_verify, *category_options)
    Label(optionsframe, text="Category").grid(row=0, column=0, padx=20)
    category_entry.grid(row=1, column=0)
    Label(text="").pack()

    period_options = [  # Period options menu
        "Forever",
        "Past Day",
        "Past Week",
        "Past Month",
        "Past Year"
    ]
    period_verify = StringVar(optionsframe)
    period_verify.set(period_options[0])  # default value
    period_entry = OptionMenu(optionsframe, category_verify, *period_options)
    Label(optionsframe, text="Period").grid(row=0, column=1, padx=20)
    period_entry.grid(row=1, column=1)
    Label(text="").pack()


    Label(optionsframe, text="Title, Description:").grid(row=0, column=2, padx=40)  # Search bar in tab 1
    search_entry = Entry(optionsframe, textvariable=search_verify1).grid(row=1, column=2, padx=40)

    Button(optionsframe, text="GO", command=search_button_click).grid(row=1, column=3, sticky="W")  # Search button

    advertisements = ttk.Treeview(tableframe)  # advertisements Ads Table
    advertisements['columns'] = ('title', 'description', 'price', 'date')
    advertisements['show'] = 'headings'
    advertisements.heading('title', text='Title')
    advertisements.column('title', width=125)
    advertisements.heading('description', text='Description')
    advertisements.column('description', width=125)
    advertisements.heading('price', text='Price')
    advertisements.column('price', width=125)
    advertisements.heading('date', text='Date')
    advertisements.column('date', width=125)
    advertisements.pack()

    ## My advertisements Tab
    optionsframe2 = ttk.Frame(tab2)
    optionsframe2.pack(side="top", fill="x")  # Split tab into two frames top and bottom

    tableframe2 = ttk.Frame(tab2)  # Split tab into two frames top and bottom
    tableframe2.pack(side="bottom", fill="x")
    optionsframe2.columnconfigure(0, weight=1)
    optionsframe2.columnconfigure(1, weight=1)
    Button(optionsframe2, text="EDIT", command=edit_button_click, width= 20, height=4).grid(row=0, column= 0, padx=20 , pady=5)  # Edit  button
    Button(optionsframe2, text="DELETE", command=delete_button_click, width = 20,  height=4).grid(row=0, column=1, padx=20, pady=5 )  # Delete Search button

    my_advertisements = ttk.Treeview(tableframe2)  # Unclaimed Ads Table
    my_advertisements['columns'] = ('id','title', 'description','status', 'price', 'date')
    my_advertisements['show'] = 'headings'
    my_advertisements.heading('id', text='ID')
    my_advertisements.column('id', width=125)
    my_advertisements.heading('title', text='Title')
    my_advertisements.column('title', width=125)
    my_advertisements.heading('description', text='Description')
    my_advertisements.column('description', width=125)
    my_advertisements.heading('status', text='Status')
    my_advertisements.column('status', width=125)
    my_advertisements.heading('price', text='Price')
    my_advertisements.column('price', width=125)
    my_advertisements.heading('date', text='Date')
    my_advertisements.column('date', width=125)
    my_advertisements.pack()


    tab_control.pack(expand=1, fill="both")
    user_screen.mainloop()



def moderator_screen():

    def search_button_click():
        print("Search Button Clicked")
    def claimad_button_click():
        print("Ad Claim Button Clicked")

    # todo add stuff
    main_screen.destroy()
    global moderator_screen

    moderator_screen = Tk()
    moderator_screen.geometry("750x600")
    moderator_screen.title("Moderator Tab")

    global search_verify
    search_verify = StringVar(moderator_screen)

    form_label = Label(text="Moderator Tab", bg="blue", width="300", height="2", font=("Calibri", 22))
    form_label.pack()
    tab_control = ttk.Notebook(moderator_screen)  # Create Tab Control

    tab1 = ttk.Frame(tab_control)  # Create a tab
    tab2 = ttk.Frame(tab_control)  # Create a tab



    tab_control.add(tab1, text='Unclaimed Advertisements')  # Add the tab
    tab_control.add(tab2, text='My Advertisements') # Add the tab

    optionsframe = ttk.Frame(tab1)
    optionsframe.pack(side="top", fill="x")     #Split tab into two frames top and bottom

    tableframe = ttk.Frame(tab1)                #Split tab into two frames top and bottom
    tableframe.pack(side="bottom", fill="x")

    category_options = [ # Category options menu
        "All",
        "Cars and Trucks",
        "Housing",
        "Electronics",
        "Child Care"
    ]
    category_verify = StringVar(optionsframe)
    category_verify.set(category_options[0])  # default value
    category_entry = OptionMenu(optionsframe, category_verify, *category_options)
    Label(optionsframe, text="Category").grid(row = 1, column = 1, padx=20)
    category_entry.grid(row = 2, column = 1)
    Label(text="").pack()

    period_options = [ # Period options menu
        "Forever",
        "Past Day",
        "Past Week",
        "Past Month",
        "Past Year"
    ]
    period_verify = StringVar(optionsframe)
    period_verify.set(period_options[0])  # default value
    period_entry = OptionMenu(optionsframe, category_verify, *period_options)
    Label(optionsframe, text="Period").grid(row = 1, column = 2, padx=20)
    period_entry.grid(row = 2, column = 2)
    Label(text="").pack()

    Label(optionsframe, text="Title, Description:").grid(row = 1, column = 3, padx = 40)                    #Search bar in tab 1
    search_entry = Entry(optionsframe, textvariable = search_verify).grid(row = 2, column = 3, padx = 40)

    Button(optionsframe, text="GO", command=search_button_click).grid(row = 2, column = 4, sticky = "W") #Search button


    rowsize, columnsize = optionsframe.grid_size()
    Button(optionsframe, text="Claim Ad", command = claimad_button_click, justify= "right").grid(row = 3, column = 4, padx = 300,pady = 20)






    unclaimedAdsTable = ttk.Treeview(tableframe) #Unclaimed Ads Table
    unclaimedAdsTable['columns'] = ('id', 'title', 'description', 'price', 'status', 'date')
    #unclaimedAdsTable.heading("#0", text='ID', anchor='w')
    #unclaimedAdsTable.column("#0", anchor="w")
    unclaimedAdsTable['show'] = 'headings'
    unclaimedAdsTable.heading('id', text='ID')
    unclaimedAdsTable.column('id', width=125)
    unclaimedAdsTable.heading('title', text='Title')
    unclaimedAdsTable.column('title', width=125)
    unclaimedAdsTable.heading('description', text='Description')
    unclaimedAdsTable.column('description', width=125)
    unclaimedAdsTable.heading('price', text='Price')
    unclaimedAdsTable.column('price', width=125)
    unclaimedAdsTable.heading('status', text='Status')
    unclaimedAdsTable.column('status', width=125)
    unclaimedAdsTable.heading('date', text='Date')
    unclaimedAdsTable.column('date', width=125)
    unclaimedAdsTable.pack()

    


    tab_control.pack(expand=1, fill="both")  # Pack to make visible
    moderator_screen.mainloop()



# main page

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")

    global username_verify
    global userpassword_verify
    global user_type_verify

    username_verify = StringVar()
    userpassword_verify = StringVar()

    global username_login_entry
    global userpassword_login_entry
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

    # Set password entry
    userpassword_login_entry = Entry(main_screen, textvariable = userpassword_verify)
    userpassword_login_entry.pack()

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
