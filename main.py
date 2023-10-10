import pygame
from tkinter import *



# Background Image
#bg = PhotoImage(file="Sad_Background.gif")
#label1 = Label(window, image=bg)
#label1.place(x=0, y=0)
#label1.lower()
#bg_order = 0

if __name__=='__main__':
    #Get Users List
    file = open("text.txt","r")
    users = []

    for line in file.readlines():
        user = line.strip("\n").split(",")
        users.append(user)
    #Number of Users
    count = len(users)

    # creating and naming window
    root = Tk()
    root.title("Pacemaker GUI")
    # Changing background colour
    root.configure(background="black")

    # Changing window size
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))

    root.resizable(False, False)
    #Application(master=root)
    root.mainloop()