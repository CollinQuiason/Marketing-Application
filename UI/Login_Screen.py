from tkinter import *

# from mysql import *


def login_account_screen():
    main_screen = Tk()  # create a GUI window
    main_screen.geometry("300x250")  # set the configuration of GUI window
    main_screen.title("Account Login")  # set the title of GUI window
    username = StringVar()

    # create a Form label
    form_Label = Label(text="Choose Login", bg="blue", width="300", height="2", font=("Calibri", 13))
    form_Label.pack()
    Label(text="").pack()

    # Set username label
    username_lable = Label(main_screen, text="Enter your Username and select User Type ")
    username_lable.pack()

    # Set username entry
    username_entry = Entry(main_screen, textvariable=username)
    username_entry.pack()

    # User Selection
    variable = StringVar(main_screen)
    variable.set("USER")  # default value

    userDropDown = OptionMenu(main_screen, variable, "USER", "MODERATOR")
    userDropDown.pack()

    # create Login Button
    login_button = Button(text="Login", height="2", width="30")
    login_button.pack()
    Label(text="").pack()

    main_screen.mainloop()  # start the GUI


login_account_screen()