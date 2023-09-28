import pygame
from tkinter import *


# creating and naming window
window = Tk()
window.title("First Window")
# Changing background colour
# window.configure(background="black")

# Changing window size
width, height = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry('%dx%d+0+0' % (width, height))

# Background Image
#bg = PhotoImage(file="Sad_Background.gif")
#label1 = Label(window, image=bg)
#label1.place(x=0, y=0)
#label1.lower()
#bg_order = 0

pygame.init()

window.mainloop()