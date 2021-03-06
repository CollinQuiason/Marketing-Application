from tkinter import *
from tkinter import ttk
import mysql.connector
import datetime
import time

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

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="root", # this will be different depening on your database
 database="Project2",
 port = 8889 ,
 #auth_plugin='mysql_native_password'
)





def login_verify():
    # gets the variables needed
    username = username_verify.get()
    password = userpassword_verify.get()
    user_type = user_type_verify.get()
    # clears out old entry boxes
    userpassword_login_entry.delete(0, END)
    username_login_entry.delete(0, END)
    my_cursor = mydb.cursor()

    if user_type == 'USER' :
        # Querys database to make sure user is in database
        sqlstatement = "SELECT User_ID, UserPassword, UserSalt FROM Users WHERE User_ID = %(User_ID)s;"
        my_cursor.execute(sqlstatement, {"User_ID": username})
        list_of_users = my_cursor.fetchall()
        flag_user_found = False
        for x in list_of_users:
            if (username == x[0] and check_secure_val(x[2], password, x[1])):
                flag_user_found = True
                login_success_user(username)
        if not flag_user_found:
            user_not_found()

    else :
        # Querys the Database to see if moderator is in there.
        sqlstatement = "SELECT User_ID FROM Moderators WHERE User_ID = %(User_ID)s;"
        my_cursor.execute(sqlstatement, {"User_ID": username})
        list_of_moderators = my_cursor.fetchall()
        flag_moderator_found = False
        for x in list_of_moderators:
            if username == x[0]:
                flag_moderator_found = True
                login_success_moderators(username)
        if not flag_moderator_found:
            moderator_not_found()


def login_success_user(username):
    global login_success_users_screen
    login_success_users_screen = Toplevel(main_screen)
    login_success_users_screen.title("Success")
    login_success_users_screen.geometry("150x100")
    Label(login_success_users_screen, text="Login Success").pack()
    Button(login_success_users_screen, text="OK", command=delete_login_success_users(username)).pack()

def login_success_moderators(username):
    global login_success_moderators_screen
    login_success_moderators_screen = Toplevel(main_screen)
    login_success_moderators_screen.title("Success")
    login_success_moderators_screen.geometry("150x100")
    Label(login_success_moderators_screen, text="Login Success").pack()
    Button(login_success_moderators_screen, text="OK", command=delete_login_success_moderators(username)).pack()

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

def delete_login_success_users(username):
    login_success_users_screen.destroy()
    user_screen(username)

def delete_login_success_moderators(username):
    login_success_moderators_screen.destroy()
    moderator_screen(username)

def delete_user_not_found_screen():
    user_not_found_screen.destroy()


def delete_moderator_not_found_screen():
    moderator_not_found_screen.destroy()


def user_screen(username):
    # todo add advertisement, edit delete.
    global search_entry

    def add_advertisement():
        # todo add functionality
        global add_advertisement_screen
        add_advertisement_screen = Tk()
        add_advertisement_screen.geometry("300x400")
        add_advertisement_screen.title("Add Advetisement")

        # title entry
        global adv_title_verify
        adv_title_verify = StringVar(add_advertisement_screen)
        Label(add_advertisement_screen, text="Title ").pack()
        adv_title_entry = Entry(add_advertisement_screen, textvariable=adv_title_verify)
        adv_title_entry.pack()
        Label(text="").pack()
        # description entry
        global adv_descp_verify
        adv_descp_verify = StringVar(add_advertisement_screen)
        Label(add_advertisement_screen, text="Description ").pack()
        adv_descp_entry = Entry(add_advertisement_screen, textvariable=adv_descp_verify, width="30", )
        adv_descp_entry.pack()
        Label(text="").pack()
        type_options = [  # Category options menu
            "Cars and Trucks",
            "Houseing",
            "Electronics",
            "Child Care"
        ]
        # category Selection
        global ad_type_verify
        Label(add_advertisement_screen, text="Category ").pack()
        ad_type_verify = StringVar(add_advertisement_screen)
        ad_type_verify.set(type_options[0])  # default value
        ad_type_entry = OptionMenu(add_advertisement_screen, ad_type_verify, *type_options)
        ad_type_entry.pack()
        Label(text="").pack()
        # price entry
        global adv_price_verify
        adv_price_verify = StringVar(add_advertisement_screen)
        Label(add_advertisement_screen, text="Price ").pack()
        adv_price_entry = Entry(add_advertisement_screen, textvariable=adv_price_verify)
        adv_price_entry.pack()
        Label(text="").pack()
        Label(text="").pack()

        # create Advertisement  Button
        create_ad_button = Button(add_advertisement_screen, text="Create AD ", height="3", width="30",
                                  command=create_ad)
        create_ad_button.pack()

    def create_ad():
        # Queries database to make sure user is in database
        title = adv_title_verify.get()
        details = adv_descp_verify.get()
        category = ad_type_verify.get()
        price = adv_price_verify.get()
        date = datetime.date.today()
        status = "PN"

        my_cursor = mydb.cursor()
        sql_add_statement = "INSERT INTO Advertisements (AdvTitle, AdvDetails, AdvDateTime, price, User_ID, Category_ID, Status_ID) VALUES (%(title)s, %(details)s, %(date)s, %(price)s, %(username)s, (SELECT Category_ID FROM Categories WHERE CatName = %(category)s), %(status)s)"
        my_cursor.execute(sql_add_statement, (
            {"title": title, "details": details, "date": date.strftime('%y-%m-%d'), "price": price,
             "username": username,
             "category": category, "status": status}))
        mydb.commit()
        add_advertisement_screen.destroy()
        build_my_advertisements_table(my_advertisements)



    def search_button_click2():
        # variables needed for SQL query
        category = category_verify.get()
        period = period_verify.get()
        search = search_verify1.get()
        wherecluase = ''
        # adds the category filtering to where clause
        if category != 'All':
            wherecluase += ' AND C.CatName = \'' + category + '\''
        # adds time period filtering to where clause
        if period != 'Forever':
            today = datetime.date.today()
            if period == 'Past Day':
                past_date = datetime.date.today() - datetime.timedelta(days=1)
            elif period == 'Past Week':
                past_date = datetime.date.today() - datetime.timedelta(days=7)
            elif period == 'Past Month':
                past_date = datetime.date.today() - datetime.timedelta(days=30)
            elif period == 'Past Year':
                past_date = datetime.date.today() - datetime.timedelta(days=365)

            wherecluase += ' AND (A.AdvDateTime BETWEEN \' ' + past_date.strftime('%y-%m-%d') + '\' AND \'' + today.strftime('%y-%m-%d') +'\')'
        # adds search filtering to where clause
        if search != '':
            wherecluase += ' AND A.AdvTitle LIKE \'%' + search + '%\' OR A.AdvDetails LIKE \'%'  + search + '%\' '
        # rebuilds the table
        build_advertisements_table(advertisements, wherecluase)

    def edit_advertisement(selectedItem):
        global edit_advertisement_screen
        edit_advertisement_screen = Tk()
        edit_advertisement_screen.geometry("300x400")
        edit_advertisement_screen.title("Edit Advertisement")
        row_data = selectedItem['values']
        mycursor = mydb.cursor()
        sqlstatement = "SELECT A.User_ID, c.CatName, A.Advertisements_ID FROM Advertisements A  INNER JOIN Categories C ON A.Category_ID = C.Category_ID WHERE a.AdvTitle =  %(title)s"
        mycursor.execute(sqlstatement, {"title": row_data[1]})
        global myresult1
        myresult1 = mycursor.fetchall()

        # title
        global ad_title_verify4
        ad_title_verify4 = StringVar(edit_advertisement_screen)
        ad_title_verify4.set(row_data[1])
        Label(edit_advertisement_screen, text="Title ").pack()
        ad_title_entry = Entry(edit_advertisement_screen, textvariable=ad_title_verify4)
        ad_title_entry.pack()
        Label(text="").pack()

        # description entry
        global adv_desc_verify4
        adv_desc_verify4 = StringVar(edit_advertisement_screen)
        adv_desc_verify4.set(row_data[2])
        Label(edit_advertisement_screen, text="Description ").pack()
        adv_desc_entry = Entry(edit_advertisement_screen, textvariable=adv_desc_verify4, width="30", )
        adv_desc_entry.pack()
        Label(text="").pack()
        global ad_type_verify4
        type_options = [  # Category options menu
            "Cars and Trucks",
            "Houseing",
            "Electronics",
            "Child Care"
        ]
        # category Selection
        Label(edit_advertisement_screen, text="Category ").pack()
        ad_type_verify4 = StringVar(edit_advertisement_screen)
        ad_type_verify4.set(myresult1[0][1])  # default value
        ad_type_entry = OptionMenu(edit_advertisement_screen, ad_type_verify4, *type_options)
        ad_type_entry.pack()
        Label(text="").pack()

        # price entry
        global adv_price_verify2
        adv_price_verify2 = StringVar(edit_advertisement_screen)
        adv_price_verify2.set(row_data[3])

        Label(edit_advertisement_screen, text="Price ").pack()
        adv_price_entry = Entry(edit_advertisement_screen, textvariable=adv_price_verify2, width="30", )
        adv_price_entry.pack()
        Label(text="").pack()

        #  Edit Advertisement Button

        edit_ad_button = Button(edit_advertisement_screen, text="Edit Ad", height="3", width="30", command=edit_ad_button2)
        edit_ad_button.pack()


    def edit_ad_button2():
        temp = myresult1

        t = ad_title_verify4.get()
        d = adv_desc_verify4.get()
        c = ad_type_verify4.get()
        newprice = float(adv_price_verify2.get())
        mycursor = mydb.cursor()
        updateSQL = 'UPDATE Advertisements SET AdvTitle = %(T)s,AdvDetails = %(D)s, Category_ID = (SELECT Category_ID FROM Categories WHERE CatName = %(C)s),price = %(P)s WHERE Advertisements_ID = %(ID)s'

        mycursor.execute(updateSQL, {"T": t, "D": d, "C": c,
                                     "P": newprice, "ID": temp[0][2]})
        mydb.commit()
        close_edit()
    def close_edit():
        edit_advertisement_screen.destroy()
        build_my_advertisements_table(my_advertisements)

    def selectrow():
        item = my_advertisements.item(my_advertisements.selection())
        return item
    def edit_button_click():
        my_advertisements.bind('<ButtonRelease-1>', selectrow)
        my_advertisements.grid()
        selectedItem = selectrow()
        edit_advertisement(selectedItem)


    def delete_button_click():
        my_advertisements.bind('<ButtonRelease-1>', selectrow)
        my_advertisements.grid()
        selectedItem = selectrow()

        ADID = selectedItem['values'][0]
        my_cursor = mydb.cursor()
        sql_delete_statement = "DELETE FROM Advertisements WHERE Advertisements.Advertisements_ID = %(ID)s; "
        my_cursor.execute(sql_delete_statement, {"ID": ADID})
        time.sleep(5)
        build_my_advertisements_table(my_advertisements)


    # deletes the login screen
    main_screen.destroy()

    # global variables declared
    global user_screen
    user_screen = Tk()  # Create instance
    user_screen.geometry("850x600")
    user_screen.title("User Tab")  # Add a title

    global search_verify1
    search_verify1 = StringVar(user_screen)
    global wherecluase
    wherecluase =''

    # title section
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
        "Houseing",
        "Electronics",
        "Child Care"
    ]
    global category_verify
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
    global period_verify
    period_verify = StringVar(optionsframe)
    period_verify.set(period_options[0])  # default value
    period_entry = OptionMenu(optionsframe, period_verify, *period_options)
    Label(optionsframe, text="Period").grid(row=0, column=1, padx=20)
    period_entry.grid(row=1, column=1)
    Label(text="").pack()


    Label(optionsframe, text="Title, Description:").grid(row=0, column=2, padx=40)  # Search bar in tab 1
    search_entry = Entry(optionsframe, textvariable=search_verify1).grid(row=1, column=2, padx=40)

    # SQL statement to pull in the defualt data
    status = 'Active'
    sqlstatement = "SELECT AdvTitle, AdvDetails, price, AdvDateTime FROM Advertisements A INNER JOIN Status_Type B on A.Status_ID = B.Status_ID INNER JOIN Categories C ON A.Category_ID = C.Category_ID WHERE B.StatusName =  %(StatusName)s "
    Button(optionsframe, text="GO", command=search_button_click2).grid(row=1, column=3, sticky="W")  # Search button
    # this functions builds the Advertisement table given the table name and where clause
    def build_advertisements_table(table,where):
        # clears out old data
        for row in table.get_children():
            table.delete(row)
        # sets up Query
        my_cursor = mydb.cursor()
        tempsql = sqlstatement + where
        my_cursor.execute(tempsql, {"StatusName": status})
        records = my_cursor.fetchall()
        # inserts updated records
        for row in records:
            table.insert('', 'end', values=(row[0],row[1],row[2],row[3].strftime("%y/ %m/ %d")))
            table.pack()

    global advertisements
    advertisements = ttk.Treeview(tableframe)  # advertisements Table
    advertisements['columns'] = ('title', 'description', 'price', 'date')
    advertisements['show'] = 'headings'
    advertisements.heading('title', text='Title')
    advertisements.column('title', width=200)
    advertisements.heading('description', text='Description')
    advertisements.column('description', width=280)
    advertisements.heading('price', text='Price')
    advertisements.column('price', width=125)
    advertisements.heading('date', text='Date')
    advertisements.column('date', width=150)
    build_advertisements_table(advertisements, wherecluase)


    ## My advertisements Tab

    optionsframe2 = ttk.Frame(tab2)
    optionsframe2.pack(side="top", fill="x")  # Split tab into two frames top and bottom

    tableframe2 = ttk.Frame(tab2)  # Split tab into two frames top and bottom
    tableframe2.pack(side="bottom", fill="x")
    optionsframe2.columnconfigure(0, weight=1)
    optionsframe2.columnconfigure(1, weight=1)

      # Edit  button
    Button(optionsframe2, text="DELETE", command=delete_button_click, width = 20,  height=4).grid(row=0, column=1, padx=20, pady=5 )  # Delete Search button

    def build_my_advertisements_table(table):
        for row in table.get_children():
            table.delete(row)
        my_cursor = mydb.cursor()
        sqlstatement2 = "SELECT A.Advertisements_ID, A.AdvTitle, A.AdvDetails, A.price, B.StatusName, A.AdvDateTime, A.User_ID FROM Advertisements A INNER JOIN Status_Type B on A.Status_ID = B.Status_ID WHERE A.User_ID = %(User_ID)s; "
        my_cursor.execute(sqlstatement2, {"User_ID": username})
        result = my_cursor.fetchall()
        for row in result:
            table.insert('', 'end', values=(row[0], row[1], row[2], row[3],row[4], row[5].strftime("%y/ %m/ %d")))
            table.pack()

    global my_advertisements
    my_advertisements = ttk.Treeview(tableframe2)  # my_advertisements Table
    my_advertisements['columns'] = ('id', 'title', 'description', 'price', 'status', 'date')
    my_advertisements['show'] = 'headings'
    my_advertisements.heading('id', text='ID')
    my_advertisements.column('id', width=40)
    my_advertisements.heading('title', text='Title')
    my_advertisements.column('title', width=175)
    my_advertisements.heading('description', text='Description')
    my_advertisements.column('description', width=280)
    my_advertisements.heading('price', text='Price')
    my_advertisements.column('price', width=75)
    my_advertisements.heading('status', text='Status')
    my_advertisements.column('status', width=80)
    my_advertisements.heading('date', text='Date')
    my_advertisements.column('date', width=120)




    build_my_advertisements_table(my_advertisements)

    Button(optionsframe2, text="EDIT", command=edit_button_click, width=20, height=4).grid(row=0, column=0,
                                                                                                 padx=20, pady=5)
    tab_control.pack(expand=1, fill="both")
    user_screen.mainloop()


def moderator_screen(moderator_username):
    def selectrow_mod(tableparam):
        item = tableparam.item(tableparam.selection())
        return item
    def claimad_button_click():
        print("Ad Claim Button Clicked")
        # todo add functionality
        unclaimedAdsTable.bind('<ButtonRelease-1>', selectrow_mod(unclaimedAdsTable))
        unclaimedAdsTable.grid()
        selectedItem = selectrow_mod(unclaimedAdsTable)

        sqlstatement27 = "UPDATE Advertisements SET Moderator_ID = %(moderator_id)s WHERE Advertisements_ID = %(adID)s"
        my_cursor = mydb.cursor()
        my_cursor.execute(sqlstatement27, {"adID": selectedItem['values'][0], "moderator_id": moderator_username})
        mydb.commit()
        initialize_unclaimed_ads_table(unclaimedAdsTable)
        build_my_ad_table(myAdsTable)
    def search_button_click():
        # variables needed for SQL query
        category = category_verify_moderator.get()
        period = period_verify_moderator.get()
        search = search_verify_moderator.get()
        wherecluase = ''
        # adds the category filtering to where clause
        if category != 'All':
            wherecluase += ' AND C.CatName = \'' + category + '\''
        # adds time period filtering to where clause
        if period != 'Forever':
            today = datetime.date.today()
            if period == 'Past Day':
                past_date = datetime.date.today() - datetime.timedelta(days=1)
            elif period == 'Past Week':
                past_date = datetime.date.today() - datetime.timedelta(days=7)
            elif period == 'Past Month':
                past_date = datetime.date.today() - datetime.timedelta(days=30)
            elif period == 'Past Year':
                past_date = datetime.date.today() - datetime.timedelta(days=365)

            wherecluase += ' AND (A.AdvDateTime BETWEEN \' ' + past_date.strftime('%y-%m-%d') + '\' AND \'' + today.strftime('%y-%m-%d') +'\')'
        # adds search filtering to where clause
        if search != '':
            wherecluase += ' AND A.AdvDetails LIKE \'%' + search + '%\' OR A.AdvTitle LIKE \'%' + search + '%\''
        # rebuilds the table
        build_unclaimed_ads_table(unclaimedAdsTable, wherecluase)


    def initialize_unclaimed_ads_table(table):
        # clears out old data
        for row in table.get_children():
            table.delete(row)
        # sets up Query
        my_cursor = mydb.cursor()

        sqlstatement = "SELECT Advertisements_ID, AdvTitle, AdvDetails, price, AdvDateTime, User_ID FROM advertisements WHERE Moderator_ID IS NULL"
        my_cursor.execute(sqlstatement)
        records = my_cursor.fetchall()
        # inserts updated records
        for row in records:
            table.insert('', 'end', values=(row[0],row[1],row[2],row[3],row[4].strftime("%y/ %m/ %d"),row[5]))
        table.pack()
    def build_unclaimed_ads_table(table,where):
        # clears out old data
        for row in table.get_children():
            table.delete(row)
        # sets up Query
        my_cursor = mydb.cursor()
        tempsql = sqlstatement3 + where
        my_cursor.execute(tempsql)
        records = my_cursor.fetchall()
        # inserts updated records
        for row in records:
            table.insert('', 'end', values=(row[0],row[1],row[2],row[3], row[4].strftime("%y/ %m/ %d"), row[5]))
            table.pack()
    # todo add stuff
    main_screen.destroy()
    global moderator_screen

    moderator_screen = Tk()
    moderator_screen.geometry("750x600")
    moderator_screen.title("Moderator Tab")

    global search_verify
    search_verify_moderator = StringVar(moderator_screen)

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
        "Houseing",
        "Electronics",
        "Child Care"
    ]
    category_verify_moderator = StringVar(optionsframe)
    category_verify_moderator.set(category_options[0])  # default value
    category_entry = OptionMenu(optionsframe, category_verify_moderator, *category_options)
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
    period_verify_moderator = StringVar(optionsframe)
    period_verify_moderator.set(period_options[0])  # default value
    period_entry = OptionMenu(optionsframe, period_verify_moderator, *period_options)
    Label(optionsframe, text="Period").grid(row = 1, column = 2, padx=20)
    period_entry.grid(row = 2, column = 2)
    Label(text="").pack()

    Label(optionsframe, text="Title, Description:").grid(row = 1, column = 3, padx = 40)                    #Search bar in tab 1
    search_entry = Entry(optionsframe, textvariable = search_verify_moderator).grid(row = 2, column = 3, padx = 40)

    sqlstatement3 = "SELECT  A.Advertisements_ID, A.AdvTitle, A.AdvDetails, A.price, A.AdvDateTime, A.User_ID  FROM Advertisements A INNER JOIN Status_Type B on A.Status_ID = B.Status_ID INNER JOIN Categories C ON A.Category_ID = C.Category_ID WHERE A.Moderator_ID IS NULL"
    Button(optionsframe, text="GO", command=search_button_click).grid(row = 2, column = 4, sticky = "W") #Search button


    rowsize, columnsize = optionsframe.grid_size()
    Button(optionsframe, text="Claim Ad", command = claimad_button_click, justify= "right").grid(row = 3, column = 4, padx = 300,pady = 20)





    global unclaimedAdsTable
    unclaimedAdsTable = ttk.Treeview(tableframe) #Unclaimed Ads Table
    unclaimedAdsTable['columns'] = ('id', 'title', 'description', 'price', 'date', 'username')
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
    unclaimedAdsTable.heading('date', text='Date')
    unclaimedAdsTable.column('date', width=125)
    unclaimedAdsTable.heading('username', text='Username')
    unclaimedAdsTable.column('username', width=125)
    initialize_unclaimed_ads_table(unclaimedAdsTable)

    #This is the start for the my advertisements tab inside of the moderator
    def selectrow_mod(tableparam):
        item = tableparam.item(tableparam.selection())
        return item

    def approved_botton_click():
       myAdsTable.bind('<ButtonRelease-1>', selectrow_mod(myAdsTable))
       myAdsTable.grid()
       selectedItem = selectrow_mod(myAdsTable)

       sqlstatement33 = "UPDATE Advertisements SET Status_ID = \'AC\' WHERE Advertisements_ID = %(adID)s"
       my_cursor = mydb.cursor()
       print(selectedItem['values'][0])
       my_cursor.execute(sqlstatement33, {"adID": selectedItem['values'][0]})
       mydb.commit()
       build_my_ad_table(myAdsTable)

    print ("Button Clicked")


    optionsframe2 = ttk.Frame(tab2)
    optionsframe2.pack(side="top", fill="x")  # Split tab into two frames top and bottom for My Advertisements

    tableframe2 = ttk.Frame(tab2)  # Split tab into two frames top and bottom for My Advertisements
    tableframe2.pack(side="bottom", fill="x")

    rowsize, columnsize = optionsframe.grid_size()
    Button(optionsframe2, text="Approve", command=approved_botton_click, justify="right").grid(row=3, column=4, padx=680, pady=100)


    # this functions builds the Advertisement table given the table name and where clause

    status = 'Active'
    sqlstatement2 = "SELECT A.Advertisements_ID,A.AdvTitle, A.AdvDetails, A.price,A.Status_ID, A.AdvDateTime, A.Advertisements_ID FROM Advertisements A INNER JOIN Status_Type B on A.Status_ID = B.Status_ID INNER JOIN Categories C ON A.Category_ID = C.Category_ID WHERE A.Moderator_ID =  %(moderator_id)s "

    def build_my_ad_table(table):
        # clears out old data
        for row in table.get_children():
            table.delete(row)
        # sets up Query
        my_cursor1 = mydb.cursor()
        tempsql = sqlstatement2
        my_cursor1.execute(tempsql, {"moderator_id": moderator_username})
        records = my_cursor1.fetchall()
        # inserts updated records
        for row in records:
            table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4],row[5].strftime("%y/ %m/ %d"),row[6]))
            table.pack()

    myAdsTable = ttk.Treeview(tableframe2)  # Unclaimed Ads Table
    myAdsTable['columns'] = ('id', 'title', 'description', 'price', 'status', 'date', 'username')
    # unclaimedAdsTable.heading("#0", text='ID', anchor='w')
    # unclaimedAdsTable.column("#0", anchor="w")
    myAdsTable['show'] = 'headings'
    myAdsTable.heading('id', text='ID')
    myAdsTable.column('id', width=125)
    myAdsTable.heading('title', text='Title')
    myAdsTable.column('title', width=125)
    myAdsTable.heading('description', text='Description')
    myAdsTable.column('description', width=125)
    myAdsTable.heading('price', text='Price')
    myAdsTable.column('price', width=125)
    myAdsTable.heading('status', text='Status')
    myAdsTable.column('status', width=125)
    myAdsTable.heading('date', text='Date')
    myAdsTable.column('date', width=125)
    myAdsTable.heading('username', text='Username')
    myAdsTable.column('username', width=125)
    myAdsTable.pack()
    build_my_ad_table(myAdsTable)




    tab_control.pack(expand=1, fill="both")  # Pack to make visible
    moderator_screen.mainloop()



# main page

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    global username_login_entry
    global userpassword_login_entry
    global username_verify
    global userpassword_verify
    global user_type_verify

    username_verify = StringVar()
    userpassword_verify = StringVar()



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
