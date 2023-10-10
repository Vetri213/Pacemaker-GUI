import tkinter

import pygame
from tkinter import *
from tkinter import ttk


#Login Function
def login_func():
    def login_submit():
        # Getting Username and Password from the Textboxes
        username = user_text.get(1.0, "end-1c")
        password = password_text.get(1.0, "end-1c")
        login_info = [username,password]
        if(login_info in users):
            pass
        else:
            changing_label.text = "No User Matches Your Input. Please Try Again."
    root.destroy()
    login = Tk()
    login.master = root
    login.title("Pacemaker GUI")
    # Changing background colour
    login.configure(background="black")

    # Changing window size
    width, height = login.winfo_screenwidth(), login.winfo_screenheight()
    login.geometry('%dx%d+0+0' % (width, height))

    # Heading
    label = ttk.Label(master=login, text="login", background=bg, foreground=fg, font=("Arial", 80))
    label.pack()

    # Changing Label
    changing_label = ttk.Label(master=login, text="Please Enter Your Information Below:", background=bg, foreground=fg, font=("Arial", 20))
    changing_label.pack()

    # Username
    user_label = ttk.Label(master=login, text="Username:", background=bg, foreground=fg, font=("Arial", 20))
    user_label.pack()
    user_text = Text(master=login, height=5, width=50, font=("Arial", 20))
    user_text.pack()

    # Password
    password_label = ttk.Label(master=login, text="Password:", background=bg, foreground=fg, font=("Arial", 20))
    password_label.pack()
    password_text = Text(master=login, height=5, width=50, font=("Arial", 20))
    password_text.pack()

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=20, borderwidth=1, focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

    # Submit Button
    submit_button = ttk.Button(master=login, text="Submit", command=login_submit)
    submit_button.pack()

    # Home Button
    exit_button = ttk.Button(master=login, text="Exit", command=quit)
    exit_button.pack()

#Register Function
def register_func():
    def register_submit():
        #Getting Username and Password from the Textboxes
        username = user_text.get(1.0, "end-1c")
        password = password_text.get(1.0, "end-1c")
        #Creating a New Entry to be added to the file of Users (in the same format)
        new_entry = "\n"+username+","+password
        #Opening File in Append Mode (So as not to delete other users)
        file = open("text.txt", "a")
        #Adding Entry
        file.write(new_entry)
        #Closing file
        file.close()
        #Allow Access to the PaceMaker App
        #DO THIS LATER!!!

    root.destroy()
    register = Tk()
    register.master = root
    register.title("Pacemaker GUI")
    # Changing background colour
    register.configure(background="black")

    # Changing window size
    width, height = register.winfo_screenwidth(), register.winfo_screenheight()
    register.geometry('%dx%d+0+0' % (width, height))

    # Heading
    label = ttk.Label(master=register, text="REGISTER", background=bg, foreground=fg, font=("Arial", 80))
    label.pack()

    # Username
    user_label = ttk.Label(master=register, text="Username:", background=bg, foreground=fg, font=("Arial", 20))
    user_label.pack()
    user_text = Text(master=register, height=5, width=50, font=("Arial", 20))
    user_text.pack()

    # Password
    password_label = ttk.Label(master=register, text="Password:", background=bg, foreground=fg, font=("Arial", 20))
    password_label.pack()
    password_text = Text(master=register, height=5, width=50, font=("Arial", 20))
    password_text.pack()

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=20, borderwidth=1, focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

    # Submit Button
    submit_button = ttk.Button(master=register, text="Submit", command=register_submit)
    submit_button.pack()

    #Home Button
    exit_button = ttk.Button(master=register, text="Exit", command=quit)
    exit_button.pack()








# Background Image
#bg = PhotoImage(file="Sad_Background.gif")
#label1 = Label(window, image=bg)
#label1.place(x=0, y=0)
#label1.lower()
#bg_order = 0

if __name__=='__main__':
    # Get Users List
    file = open("text.txt", "r")
    users = []

    for line in file.readlines():
        user = line.strip("\n").split(",")
        users.append(user)
    # Number of Users
    count = len(users)
    # Close File
    file.close()

    # creating and naming window
    root = Tk()
    root.title("Pacemaker GUI")
    # Changing background colour
    root.configure(background="black")

    # Changing window size
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))

    # Widget Options
    bg = "black"
    fg = "white"

    # Heading
    label = ttk.Label(master=root, text="WELCOME", background=bg, foreground=fg, font=("Arial", 80))
    label.pack()

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background=bg, foreground=fg, width=20, borderwidth=1, focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

    # Login
    login_button = ttk.Button(root, text="Login", command=login_func)
    login_button.pack()
    # Register
    register_button = ttk.Button(master=root, text="Register", command=register_func)
    register_button.pack()
    # Quit
    button = ttk.Button(root, text='Quit', command=quit)
    button.pack()

    root.resizable(False, False)
    # Application(master=root)
    root.mainloop()

