import tkinter
import serial
import pygame
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import struct
import time

#---------------------------------HOME---------------------------------#

class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.place(relheight=1,relwidth=1)
        self.home()

    def home(self):
        #Change Background
        set_background_image(self,"ECGv1.png")
        # Heading
        self.label = ttk.Label(self, text="WELCOME", background=bg, foreground=fg, font=("Arial", 80))
        self.label.pack(pady=50)

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background=bg, foreground=fg, width=20, height=30, borderwidth=1, focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Login
        self.login_button = ttk.Button(self, text="Login", command=self.login_func)
        self.login_button.pack(pady=15)
        # Register
        self.register_button = ttk.Button(master=self, text="Register", command=self.register_func)
        self.register_button.pack(pady=15)
        # Quit
        self.quit_button = ttk.Button(self, text='Quit', command=quit)
        self.quit_button.pack(pady=15)

    def login_func(self):
        Login(master=self.master)
        self.destroy

    def register_func(self):
        Register(master=self.master)
        self.destroy

#---------------------------------LOGIN---------------------------------#

class Login(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.place(relheight=1, relwidth=1)
        self.login()


    def login(self):
        #Change Background
        set_background_image(self,"ECGv1.png")

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background=bg, foreground=fg, width=20, height=30, borderwidth=1,
                             focusthickness=3,
                             focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])
        # Heading
        self.label = ttk.Label(master=self, text="LOGIN", background=bg, foreground=fg, font=("Arial", 80))
        self.label.pack()

        # Changing Label
        self.changing_label = ttk.Label(master=self, text="Please Enter Your Information Below:", background=bg,
                                   foreground=fg, font=("Arial", 20))
        self.changing_label.pack(pady=10)

        # Username
        self.user_label = ttk.Label(master=self, text="Username:", background=bg, foreground=fg, font=("Arial", 20))
        self.user_label.pack(pady=20)
        self.user_text = Entry(master=self, width=50, font=("Arial", 20))
        self.user_text.pack()

        # Password
        self.password_label = ttk.Label(master=self, text="Password:", background=bg, foreground=fg, font=("Arial", 20))
        self.password_label.pack(pady=20)
        self.password_text = Entry(master=self, width=50, font=("Arial", 20), show="*")
        self.password_text.pack()

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=20, borderwidth=1, focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Submit Button
        self.submit_button = ttk.Button(master=self, text="Submit", command=self.login_submit)
        self.submit_button.pack(pady=20)

        # Back Button
        self.back_button = ttk.Button(master=self, text="Back", command=self.back)
        self.back_button.pack(pady=20)

        # Exit Button
        self.exit_button = ttk.Button(master=self, text="Exit", command=quit)
        self.exit_button.pack()

    def back(self):
        self.destroy()
        App(master=self.master)

    def login_submit(self):
        # Getting Username and Password from the Textboxes
        username = self.user_text.get()
        password = self.password_text.get()
        login_info = [username,password]
        if(login_info in users):
            #Go to the ACTUAL DO STUFF PAGE
            self.changing_label.configure(text="Information Recognized!")
            line_num = users.index(login_info)
            file = open("text.txt", "r")
            content = file.readlines()
            user, password, vals = content[line_num].strip("\n").split("|")
            # print(user,password,vals)
            file.close()

            self.destroy()
            pacing_modes(self.master, username, vals)

        else:
            self.changing_label.configure(text="No User Matches Your Input. Please Try Again.")

#---------------------------------REGISTER---------------------------------#

class Register(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.place(relheight=1,relwidth=1)
        self.register()

    def is_username_taken(self,username):
        try:
            # open the file anc check if the username has already been taken
            with open("text.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 2:  # make sure every line has two parts( username and password)
                        existing_username, _ = parts
                        if existing_username == username:
                            return True
        except Exception as e:
            print(f"Error checking username: {str(e)}")
        return False



    def register_submit(self):
        # print(len(users))

        if (len(users) < 10):
            # Getting Username and Password from the Textboxes
            username = self.user_text.get()
            password = self.password_text.get()
            if not username or not password:
                self.changing_label.configure(text="Username or password cannot be empty")
            elif self.is_username_taken(username):
                self.changing_label.configure(text="Username is already taken")
            else:
                default_vals = "{30, 50, 0, 0.05}{30,50,0,0.05,150}{30,50,0,0.05,0.25,150,150,0,0}{30,50,0,0.05,0.35,150,0,0}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}"
                # Creating a New Entry to be added to the file of Users (in the same format)
                new_entry = username + "|" + password + "|" + default_vals + "\n" #{30, 50, 0, 0.05}{30,50,0,0.05,150}{30,50,0,0.05,0.25,150,150,0,0}{30,50,0,0.05,0.35,150,0,0}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
                # Opening File in Append Mode (So as not to delete other users)
                file = open("text.txt", "a")
                # Adding Entry
                file.write(new_entry)
                # Closing file
                file.close()

                users.append([username, password])

                all_vals.append(default_vals)

                # Go to the ACTUAL DO STUFF PAGE
                self.changing_label.configure(text="Information Recognized!")
                self.destroy()
                pacing_modes(self.master, username, default_vals)
        else:
            self.changing_label.configure(text="Max Users Registered. Sorry!")

    # Register Function
    def register(self):
        # Change Background
        set_background_image(self,"ECGv1.png")

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background=bg, foreground=fg, width=20, height=30, borderwidth=1,
                             focusthickness=3,
                             focuscolor='none', font=('American typewriter', 20))

        # Heading
        self.label = ttk.Label(master=self, text="REGISTER", background=bg, foreground=fg, font=("Arial", 80))
        self.label.pack()

        # Changing Label
        self.changing_label = ttk.Label(master=self, text="Please Enter Your Information Below:", background=bg,
                                   foreground=fg,
                                   font=("Arial", 20))
        self.changing_label.pack(pady=10)

        # Username
        self.user_label = ttk.Label(master=self, text="Username:", background=bg, foreground=fg, font=("Arial", 20))
        self.user_label.pack(pady=20)
        self.user_text = Entry(master=self, width=50, font=("Arial", 20))
        self.user_text.pack()

        # Password
        self.password_label = ttk.Label(master=self, text="Password:", background=bg, foreground=fg, font=("Arial", 20))
        self.password_label.pack(pady=20)
        self.password_text = Entry(master=self, width=50, font=("Arial", 20), show="*")
        self.password_text.pack()

        # Style of Buttons
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TButton', background="black", foreground="white", width=20, borderwidth=1, focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        style.map('TButton', background=[('active', 'teal')])

        # Submit Button
        self.submit_button = ttk.Button(master=self, text="Submit", command=self.register_submit)
        self.submit_button.pack(pady=20)

        # Back Button
        self.back_button = ttk.Button(master=self, text="Back", command=self.back)
        self.back_button.pack(pady=20)

        # Exit Button
        self.exit_button = ttk.Button(master=self, text="Exit", command=quit)
        self.exit_button.pack()

    def back(self):
        self.destroy()
        App(master=self.master)

#---------------------------------PACING MODES---------------------------------#

class pacing_modes(tkinter.Frame):
    def __init__(self,master=None,user=None,vals=None):
        super().__init__(master)
        self.master = master
        self.user = user
        self.vals = vals
        self.place(relheight=1, relwidth=1)
        self.globalize_vals()
        self.pacingmodes()

    # Check if there is a connection to the DCM and if so, which port
    def check_connection(self):
        global port
        try:
            serial.Serial(port="COM6", baudrate=115200)
            port = 6
        except:
            try:
                serial.Serial(port="COM5", baudrate=115200)
                port = 5
            except:
                try:
                    serial.Serial(port="COM4", baudrate=115200)
                    port = 4
                except:
                    try:
                        serial.Serial(port="COM3", baudrate=115200)
                        port = 3
                    except:
                        port = 0  # not connected

    def connect(self):
        #Calling check_connection makes port a global variable that can be accessed anywhere
        self.check_connection()
        self.stat = Label(self, font=("Times New Roman", 12))
        if (port == 0):
            self.stat['text'] = "Pacemaker Connection: not connected"
        else:
            self.stat['text'] = "Pacemaker Connection: COM" + str(port)
        self.refresh = Button(self, text="Refresh", font=("Times New Roman", 12))
        self.refresh.place(x=10, y=20)
        self.refresh.bind("<Button-1>", self.refreshPressed)
        self.stat.place(x=10, y=0)

    def refreshPressed(self):
        self.check_connection()
        if (port == 0):
            self.connectivity.configure(text="No Connection")
        else:
            self.connectivity.configure(text=("Connection: COM" + str(port)))

    #Globalizing the variables to be used by all the modes
    def globalize_vals(self):
        aoo_vals_str,voo_vals_str,aai_vals_str,vvi_vals_str,aat_vals_str,vvt_vals_str,vdd_vals_str,doo_vals_str,ddi_vals_str,ddd_vals_str,ddd_vals_str,aoor_vals_str,aair_vals_str,voor_vals_str,vvir_vals_str,vddr_vals_str,door_vals_str,ddir_vals_str,dddr_vals_str = self.vals.split("}")
        aoo_vals_str = aoo_vals_str.strip("{")
        voo_vals_str = voo_vals_str.strip("{")
        aai_vals_str = aai_vals_str.strip("{")
        vvi_vals_str = vvi_vals_str.strip("{")
        aat_vals_str = aat_vals_str.strip("{")
        vvt_vals_str = vvt_vals_str.strip("{")
        vdd_vals_str = vdd_vals_str.strip("{")
        doo_vals_str = doo_vals_str.strip("{")
        ddi_vals_str = ddi_vals_str.strip("{")
        ddd_vals_str = ddd_vals_str.strip("{")
        aoor_vals_str = aoor_vals_str.strip("{")
        aair_vals_str = aair_vals_str.strip("{")
        voor_vals_str = voor_vals_str.strip("{")
        vvir_vals_str = vvir_vals_str.strip("{")
        vddr_vals_str = vddr_vals_str.strip("{")
        door_vals_str = door_vals_str.strip("{")
        ddir_vals_str = vddr_vals_str.strip("{")
        dddr_vals_str = door_vals_str.strip("{")
        global aoo_vals
        global voo_vals
        global aai_vals
        global vvi_vals
        global aat_vals
        global vvt_vals
        global vdd_vals
        global doo_vals
        global ddi_vals
        global ddd_vals
        global aoor_vals
        global aair_vals
        global voor_vals
        global vvir_vals
        global vddr_vals
        global door_vals
        global ddir_vals
        global dddr_vals
        aoo_vals = aoo_vals_str.split(",")
        voo_vals = voo_vals_str.split(",")
        aai_vals = aai_vals_str.split(",")
        vvi_vals = vvi_vals_str.split(",")
        aat_vals = aat_vals_str.split(",")
        vvt_vals = vvt_vals_str.split(",")
        vdd_vals = vdd_vals_str.split(",")
        doo_vals = doo_vals_str.split(",")
        ddi_vals = ddi_vals_str.split(",")
        ddd_vals = ddd_vals_str.split(",")
        aoor_vals = aoor_vals_str.split(",")
        aair_vals = aair_vals_str.split(",")
        voor_vals = voor_vals_str.split(",")
        vvir_vals = vvir_vals_str.split(",")
        vddr_vals = vddr_vals_str.split(",")
        door_vals = door_vals_str.split(",")
        ddir_vals = vddr_vals_str.split(",")
        dddr_vals = door_vals_str.split(",")
        # print(aoo_vals)
        # print(voo_vals)
        # print(aai_vals)
        # print(vvi_vals)

    # Takes the updated values and saves them into the text file
    def save(self):
        file = open("text.txt", "w")
        for i in range(len(users)):
            # print(user)
            if (users[i][0] == self.user):
                current_vals_str = "{"
                for val in aoo_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in voo_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in aai_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in vvi_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in aat_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in vvt_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in vdd_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in doo_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in ddi_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in ddd_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in aoor_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in aair_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in voor_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in vvir_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in vddr_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in door_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                all_vals[i] = current_vals_str
                for val in ddir_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}{"
                for val in dddr_vals:
                    current_vals_str += str(val)
                    current_vals_str += ","
                current_vals_str = current_vals_str[:len(current_vals_str) - 1]
                current_vals_str += "}"
                # current_vals_str += "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}"

                all_vals[i] = current_vals_str


            #     print (str(voo_vals))
            #     aoo_new_vals = ("{"+str(aoo_vals).strip("[]{}").replace("\' ", "")+"}")
            #     voo_new_vals = ("{"+str(voo_vals).strip("[{}]").replace("\' ", "")+"}")
            #     aai_new_vals = ("{"+str(aai_vals).strip("[]{}").replace("\' ", "")+"}")
            #     vvi_new_vals = ("{"+str(vvi_vals).strip("[]{}").replace("\' ", "")+"}")
            #     #print (aoo_new_vals)
            # print (voo_new_vals)
            # print (aai_new_vals)
            # print (vvi_new_vals)

            # entry = (str(users[i][0])+"|"+users[i][1]+"|"+aoo_new_vals+voo_new_vals+aai_new_vals+vvi_new_vals)
            # Reorder Structure with New Values
            #   pass
            # else:

            # print(all_vals[i])
            entry = (str(users[i][0]) + "|" + users[i][1] + "|" + all_vals[i] + "\n")

            file.write(entry)
        file.close()


    def save_and_logout(self):
        self.save()
        self.destroy()
        App(master=self.master)

    def save_and_quit(self):
        self.save()
        self.destroy()
        quit()

    #Display
    def pacingmodes(self):
        # Change Background
        set_background_image(self,"ECGv1.png")

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background=bg, foreground=fg, width=20, height=30, borderwidth=1, focusthickness=3,
                             focuscolor='none', font=('American typewriter', 20))
        # Heading
        self.label = ttk.Label(master=self, text="Pacing Modes", background=bg, foreground=fg, font=("Arial", 80))
        self.label.grid(row=0,column = 1,columnspan=3, padx=10,pady=10)

        # Create a frame to contain the buttons
        #button_frame = ttk.Frame(self, padding=300)
        #button_frame.pack(fill="both", expand=True)

        self.new_old = ttk.Label(master=self, text="New Pacemaker Detected", background=bg, foreground=fg, font=("Arial", 20))
        self.new_old.grid(row=1,column = 1)

        self.connectivity = ttk.Label(master=self, text="No Connection", background=bg, foreground=fg,
                                      font=("Arial", 20))
        self.connectivity.grid(row=2,column = 1)

        self.refresh_button = ttk.Button(master=self, text="Refresh", style='Pacing.TButton', command=self.refreshPressed)
        self.refresh_button.grid(row=3,column = 1)


        self.refreshPressed()

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=10, height =30, borderwidth=1, focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create buttons and add them to the frame

        self.button1 = ttk.Button(master = self, text="AOO", style='Pacing.TButton',command=self.AOOPressed)
        self.button1.grid(row=4,column = 0)

        # self.button1.grid(row=0,column=0,columnspan=2,padx=10,pady=10)
        self.button2 = ttk.Button(master = self, text="VOO", style='Pacing.TButton',command=self.VOOPressed)
        self.button2.grid(row=4,column = 2)
        self.button3 = ttk.Button(master = self, text="AAI", style='Pacing.TButton',command=self.AAIPressed)
        self.button3.grid(row=5,column = 0)
        self.button4 = ttk.Button(master = self, text="VVI", style='Pacing.TButton',command=self.VVIPressed)
        self.button4.grid(row=5,column = 2)
        self.button5 = ttk.Button(master = self, text="AAT", style='Pacing.TButton',command=self.AATPressed)
        self.button5.grid(row=6,column = 0)
        self.button6 = ttk.Button(master = self, text="VVT", style='Pacing.TButton',command=self.VVTPressed)
        self.button6.grid(row=6,column = 2)
        self.button7 = ttk.Button(master = self, text="VDD", style='Pacing.TButton',command=self.VDDPressed)
        self.button7.grid(row=7,column = 0)
        self.button8 = ttk.Button(master = self, text="DOO", style='Pacing.TButton',command=self.DOOPressed)
        self.button8.grid(row=7,column = 2)
        self.button9 = ttk.Button(master = self, text="DDI", style='Pacing.TButton',command=self.DDIPressed)
        self.button9.grid(row=8,column = 0)
        self.button10 = ttk.Button(master = self, text="DDD", style='Pacing.TButton',command=self.DDDPressed)
        self.button10.grid(row=8,column = 2)
        self.button11 = ttk.Button(master = self, text="AOOR", style='Pacing.TButton',command=self.AOORPressed)
        self.button11.grid(row=9,column = 0)
        self.button12 = ttk.Button(master = self, text="AAIR", style='Pacing.TButton',command=self.AAIRPressed)
        self.button12.grid(row=9,column = 2)
        self.button13 = ttk.Button(master = self, text="VOOR", style='Pacing.TButton',command=self.VOORPressed)
        self.button13.grid(row=10,column = 0)
        self.button14 = ttk.Button(master = self, text="VVIR", style='Pacing.TButton',command=self.VVIRPressed)
        self.button14.grid(row=10,column = 2)
        self.button15 = ttk.Button(master = self, text="VDDR", style='Pacing.TButton',command=self.VDDRPressed)
        self.button15.grid(row=11,column = 0)
        self.button16 = ttk.Button(master = self, text="DOOR", style='Pacing.TButton',command=self.DOORPressed)
        self.button16.grid(row=11,column = 2)
        self.button17 = ttk.Button(master = self, text="DDIR", style='Pacing.TButton',command=self.DDIRPressed)
        self.button17.grid(row=12,column = 0)
        self.button18 = ttk.Button(master = self, text="DDDR", style='Pacing.TButton',command=self.DDDRPressed)
        self.button18.grid(row=12,column = 2)
        self.button19 = ttk.Button(master=self, text="EGRAM", style='Pacing.TButton', command=show_egram_page)
        self.button19.grid(row=13,column = 1)
        self.logout = ttk.Button(master=self, text="Logout", style='Pacing.TButton', command=self.save_and_logout)
        self.logout.grid(row=14,column = 1)

        # Exit Button33
        self.exit_button = ttk.Button(master=self, text="Exit", command=self.save_and_quit)
        self.exit_button.grid(row=15,column = 1)




    #---DIFFERENT MODES---#
    def AOOPressed(self):
        AOO_Mode(master=self.master)


    def AAIPressed(self):
         AAI_Mode(master=self.master)

    def VOOPressed(self):
        VOO_Mode(master=self.master)


    def VVIPressed(self):
        VVI_Mode(master=self.master)

    def AATPressed(self):
        AAT_Mode(master=self.master)
    def VVTPressed(self):
        VVT_Mode(master=self.master)
    def VDDPressed(self):
        VDD_Mode(master=self.master)
    def DOOPressed(self):
        DOO_Mode(master=self.master)
    def DDIPressed(self):
        DDI_Mode(master=self.master)
    def DDDPressed(self):
        DDD_Mode(master=self.master)
    def AOORPressed(self):
        AOOR_Mode(master=self.master)
    def AAIRPressed(self):
        AAIR_Mode(master=self.master)
    def VOORPressed(self):
        VOOR_Mode(master=self.master)
    def VVIRressed(self):
        VVIR_Mode(master=self.master)
    def VDDRPressed(self):
        VDDR_Mode(master=self.master)
    def DOORPressed(self):
        DOOR_Mode(master=self.master)
    def DDIRPressed(self):
        DDIR_Mode(master=self.master)
    def DDDRPressed(self):
        DDDR_Mode(master=self.master)


class AOO_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayAOO()

    def update_aoo(self):
        global aoo_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aoo_vals
                aoo_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get()]
                Communicate(0, self.lower_rate_entry.get(), self.atrial_pulse_width_entry.get(), 0, 0, 0, 0, self.atrial_amplitude_entry.get(), 0, 0,
                                     175, 0, 7, 0, 2.5, 2.5)


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")

    def displayAOO(self):
        self.aoo_window = Tk()
        self.aoo_window.geometry('%dx%d+0+0' % (width, height))
        self.aoo_window.title("AOO Mode")
        self.aoo_window.configure(background="black")

        # Add a title
        self.aoo_label = ttk.Label(self.aoo_window, text="AOO Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.aoo_label.grid(row = 0, column = 0, columnspan = 5, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.aoo_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.aoo_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, aoo_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.aoo_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.aoo_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, aoo_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.aoo_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.aoo_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, aoo_vals[2])
        self.atrial_amplitude_label.grid(row = 3, column = 0)
        self.atrial_amplitude_entry.grid(row = 4, column = 0)

        self.atrial_pulse_width_label = ttk.Label(self.aoo_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.aoo_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, aoo_vals[3])
        self.atrial_pulse_width_label.grid(row = 3, column = 1)
        self.atrial_pulse_width_entry.grid(row = 4, column = 1)

        #    ventricular_amplitude_label = ttk.Label(self, text="Ventricular Amplitude:", background="black", foreground="white", font=("Arial", 16))
        #    ventricular_amplitude_entry = Entry(self, font=("Arial", 16))
        #    ventricular_amplitude_label.pack(pady=10)
        #    ventricular_amplitude_entry.pack(pady=10)

        #    ventricular_pulse_width_label = ttk.Label(self, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
        #    ventricular_pulse_width_entry = Entry(self, font=("Arial", 16))
        #    ventricular_pulse_width_label.pack(pady=10)
        #    ventricular_pulse_width_entry.pack(pady=10)

        # vrp_label = ttk.Label(self, text="VRP:", background="black", foreground="white", font=("Arial", 16))
        # vrp_entry = Entry(self, font=("Arial", 16))
        # vrp_label.pack(pady=10)
        # vrp_entry.pack(pady=10)

        # arp_label = ttk.Label(self, text="ARP:", background="black", foreground="white", font=("Arial", 16))
        # arp_entry = Entry(self, font=("Arial", 16))
        # arp_label.pack(pady=10)
        # arp_entry.pack(pady=10)

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.aoo_window, text="Save", style='TButton', command=self.update_aoo)
        self.save_button.grid(row = 5, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.aoo_window, text="Back to Pacing Modes", command=self.aoo_window.destroy)
        self.back_button.grid(row = 5, column = 1)



class AAI_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayAAI()

    def update_aai(self):
        global aai_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aai_vals
                aai_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.arp_entry.get(),self.pvarp_label.get(),self.hysteresis_entry.get(),self.rate_smooth_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.aai_window.destroy()

    def displayAAI(self):
        self.aai_window = Tk()
        self.aai_window.geometry('%dx%d+0+0' % (width, height))
        self.aai_window.title("AAI Mode")
        self.aai_window.configure(background="black")

        # Add a title
        self.aai_label = ttk.Label(self.aai_window, text="AAI Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.aai_label.grid(row = 0, column = 0, columnspan = 10, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.aai_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.aai_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, aai_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.aai_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.aai_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, aai_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.aai_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.aai_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, aai_vals[2])
        self.atrial_amplitude_label.grid(row = 3, column = 0)
        self.atrial_amplitude_entry.grid(row = 4, column = 0)

        self.atrial_pulse_width_label = ttk.Label(self.aai_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.aai_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, aai_vals[3])
        self.atrial_pulse_width_label.grid(row = 3, column = 1)
        self.atrial_pulse_width_entry.grid(row = 4, column = 1)

        self.atrial_sensitivity_label = ttk.Label(self.aai_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.aai_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, aai_vals[4])
        self.atrial_sensitivity_label.grid(row = 5, column = 0)
        self.atrial_sensitivity_entry.grid(row = 6, column = 0)

        self.arp_label = ttk.Label(self.aai_window, text="ARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.arp_entry = Entry(self.aai_window, font=("Arial", 16))
        self.arp_entry.insert(0, aai_vals[5])
        self.arp_label.grid(row = 5, column = 1)
        self.arp_entry.grid(row = 6, column = 1)

        self.pvarp_label = ttk.Label(self.aai_window, text="PVARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_entry = Entry(self.aai_window, font=("Arial", 16))
        self.pvarp_entry.insert(0, aai_vals[6])
        self.pvarp_label.grid(row = 7, column = 0)
        self.pvarp_entry.grid(row = 8, column = 0)

        self.hysteresis_label = ttk.Label(self.aai_window, text="Hysteresis:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.hysteresis_entry = Entry(self.aai_window, font=("Arial", 16))
        self.hysteresis_entry.insert(0, aai_vals[7])
        self.hysteresis_label.grid(row = 7, column = 1)
        self.hysteresis_entry.grid(row = 8, column = 1)

        self.rate_smooth_label = ttk.Label(self.aai_window, text="Rate Smooth:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smooth_entry = Entry(self.aai_window, font=("Arial", 16))
        self.rate_smooth_entry.insert(0, aai_vals[8])
        self.rate_smooth_label.grid(row = 9, column = 0)
        self.rate_smooth_entry.grid(row = 9, column = 1)
        #    ventricular_amplitude_label = ttk.Label(self, text="Ventricular Amplitude:", background="black", foreground="white", font=("Arial", 16))
        #    ventricular_amplitude_entry = Entry(self, font=("Arial", 16))
        #    ventricular_amplitude_label.grid(row = 0, column = 1)
        #    ventricular_amplitude_entry.grid(row = 0, column = 1)

        #    ventricular_pulse_width_label = ttk.Label(self, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
        #    ventricular_pulse_width_entry = Entry(self, font=("Arial", 16))
        #    ventricular_pulse_width_label.grid(row = 0, column = 1)
        #    ventricular_pulse_width_entry.grid(row = 0, column = 1)

        # vrp_label = ttk.Label(self, text="VRP:", background="black", foreground="white", font=("Arial", 16))
        # vrp_entry = Entry(self, font=("Arial", 16))
        # vrp_label.grid(row = 0, column = 1)
        # vrp_entry.grid(row = 0, column = 1)

        # arp_label = ttk.Label(self, text="ARP:", background="black", foreground="white", font=("Arial", 16))
        # arp_entry = Entry(self, font=("Arial", 16))
        # arp_label.grid(row = 0, column = 1)
        # arp_entry.grid(row = 0, column = 1)

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.aai_window, text="Save", style='TButton', command=self.update_aai)
        self.save_button.grid(row = 10, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.aai_window, text="Back to Pacing Modes", command=self.aai_window.destroy)
        self.back_button.grid(row = 10, column = 1)
class VOO_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVOO()

    def update_voo(self):
        global voo_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global voo_vals
                voo_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.voo_window.destroy()

    def displayVOO(self):
        self.voo_window = Tk()
        self.voo_window.geometry('%dx%d+0+0' % (width, height))
        self.voo_window.title("VOO Mode")
        self.voo_window.configure(background="black")

        # Add a title
        self.voo_label = ttk.Label(self.voo_window, text="VOO Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.voo_label.grid(row = 0, column = 0, columnspan = 5, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.voo_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.voo_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, voo_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.voo_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.voo_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, voo_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.voo_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.voo_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, voo_vals[2])
        self.ventricular_amplitude_label.grid(row = 3, column = 0)
        self.ventricular_amplitude_entry.grid(row = 4, column = 0)

        self.ventricular_pulse_width_label = ttk.Label(self.voo_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.voo_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, voo_vals[3])
        self.ventricular_pulse_width_label.grid(row = 3, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 4, column = 1)



        # self.ventricular_sensitivity_label = ttk.Label(self.voo_window, text="Ventricular Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_sensitivity_entry = Entry(self.voo_window, font=("Arial", 16))
        # self.ventricular_sensitivity_entry.insert(0, voo_vals[4])
        # self.ventricular_sensitivity_label.grid(row = 0, column = 1)
        # self.ventricular_sensitivity_entry.grid(row = 0, column = 1)
        #
        # self.vrp_label = ttk.Label(self.voo_window, text="VRP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.vrp_entry = Entry(self.voo_window, font=("Arial", 16))
        # self.vrp_entry.insert(0, voo_vals[5])
        # self.vrp_label.grid(row = 0, column = 1)
        # self.vrp_entry.grid(row = 0, column = 1)

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.voo_window, text="Save", style='TButton', command=self.update_voo)
        self.save_button.grid(row = 5, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.voo_window, text="Back to Pacing Modes", command=self.voo_window.destroy)
        self.back_button.grid(row = 5, column = 1)

class VVI_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVVI()

    def update_vvi(self):
        global vvi_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vvi_vals
                vvi_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.hysteresis_entry.get(),self.rate_smooth_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.vvi_window.destroy()

    def displayVVI(self):
        self.vvi_window = Tk()
        self.vvi_window.geometry('%dx%d+0+0' % (width, height))
        self.vvi_window.title("VVI Mode")
        self.vvi_window.configure(background="black")

        # Add a title
        self.vvi_label = ttk.Label(self.vvi_window, text="VVI Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.vvi_label.grid(row = 0, column = 0, columnspan = 9, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.vvi_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, vvi_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.vvi_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, vvi_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.vvi_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, vvi_vals[2])
        self.ventricular_amplitude_label.grid(row = 3, column = 0)
        self.ventricular_amplitude_entry.grid(row = 4, column = 0)

        self.ventricular_pulse_width_label = ttk.Label(self.vvi_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, vvi_vals[3])
        self.ventricular_pulse_width_label.grid(row = 3, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 4, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.vvi_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, vvi_vals[4])
        self.ventricular_sensitivity_label.grid(row = 5, column = 0)
        self.ventricular_sensitivity_entry.grid(row = 6, column = 0)

        self.vrp_label = ttk.Label(self.vvi_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.vrp_entry.insert(0, vvi_vals[5])
        self.vrp_label.grid(row = 5, column = 1)
        self.vrp_entry.grid(row = 6, column = 1)

        self.hysteresis_label = ttk.Label(self.vvi_window, text="Hysteresis:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.hysteresis_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.hysteresis_entry.insert(0, vvi_vals[6])
        self.hysteresis_label.grid(row = 7, column = 0)
        self.hysteresis_entry.grid(row = 8, column = 0)

        self.rate_smooth_label = ttk.Label(self.vvi_window, text="Rate Smooth:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smooth_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.rate_smooth_entry.insert(0, vvi_vals[7])
        self.rate_smooth_label.grid(row = 7, column = 1)
        self.rate_smooth_entry.grid(row = 8, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.vvi_window, text="Save", style='TButton', command=self.update_vvi)
        self.save_button.grid(row =9 , column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.vvi_window, text="Back to Pacing Modes", command=self.vvi_window.destroy)
        self.back_button.grid(row = 9, column = 1)

class AAT_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayAAT()

    def update_aat(self):
        global aat_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aat_vals
                aat_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.arp_entry.get(),self.pv_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.aat_window.destroy()

    def displayAAT(self):
        self.aat_window = Tk()
        self.aat_window.geometry('%dx%d+0+0' % (width, height))
        self.aat_window.title("AAT Mode")
        self.aat_window.configure(background="black")

        # Add a title
        self.aat_label = ttk.Label(self.aat_window, text="AAT Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.aat_label.grid(row = 0, column = 0, columnspan = 9, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.aat_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.aat_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, aat_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.aat_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.aat_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, aat_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.aat_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.aat_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, aat_vals[2])
        self.atrial_amplitude_label.grid(row = 3, column = 0)
        self.atrial_amplitude_entry.grid(row = 4, column = 0)

        self.atrial_pulse_width_label = ttk.Label(self.aat_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.aat_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, aat_vals[3])
        self.atrial_pulse_width_label.grid(row = 3, column = 1)
        self.atrial_pulse_width_entry.grid(row = 4, column = 1)

        self.atrial_sensitivity_label = ttk.Label(self.aat_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.aat_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, aat_vals[4])
        self.atrial_sensitivity_label.grid(row = 5, column = 0)
        self.atrial_sensitivity_entry.grid(row = 6, column = 0)

        self.arp_label = ttk.Label(self.aat_window, text="ARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.arp_entry = Entry(self.aat_window, font=("Arial", 16))
        self.arp_entry.insert(0, aat_vals[5])
        self.arp_label.grid(row = 5, column = 1)
        self.arp_entry.grid(row = 6, column = 1)

        self.pvarp_label = ttk.Label(self.aat_window, text="PVARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_entry = Entry(self.aat_window, font=("Arial", 16))
        self.pvarp_entry.insert(0, aat_vals[6])
        self.pvarp_label.grid(row = 7, column = 0)
        self.pvarp_entry.grid(row = 8, column = 0)

        #    ventricular_amplitude_label = ttk.Label(self, text="Ventricular Amplitude:", background="black", foreground="white", font=("Arial", 16))
        #    ventricular_amplitude_entry = Entry(self, font=("Arial", 16))
        #    ventricular_amplitude_label.grid(row = 0, column = 1)
        #    ventricular_amplitude_entry.grid(row = 0, column = 1)

        #    ventricular_pulse_width_label = ttk.Label(self, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
        #    ventricular_pulse_width_entry = Entry(self, font=("Arial", 16))
        #    ventricular_pulse_width_label.grid(row = 0, column = 1)
        #    ventricular_pulse_width_entry.grid(row = 0, column = 1)

        # vrp_label = ttk.Label(self, text="VRP:", background="black", foreground="white", font=("Arial", 16))
        # vrp_entry = Entry(self, font=("Arial", 16))
        # vrp_label.grid(row = 0, column = 1)
        # vrp_entry.grid(row = 0, column = 1)

        # arp_label = ttk.Label(self, text="ARP:", background="black", foreground="white", font=("Arial", 16))
        # arp_entry = Entry(self, font=("Arial", 16))
        # arp_label.grid(row = 0, column = 1)
        # arp_entry.grid(row = 0, column = 1)

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.aat_window, text="Save", style='TButton', command=self.update_aat)
        self.save_button.grid(row = 9, column = 1)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.aat_window, text="Back to Pacing Modes", command=self.aat_window.destroy)
        self.back_button.grid(row = 9, column = 1)

class VVT_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVVT()

    def update_vvt(self):
        global vvt_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vvt_vals
                vvt_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.vvt_window.destroy()

    def displayVVT(self):
        self.vvt_window = Tk()
        self.vvt_window.geometry('%dx%d+0+0' % (width, height))
        self.vvt_window.title("VVT Mode")
        self.vvt_window.configure(background="black")

        # Add a title
        self.vvt_label = ttk.Label(self.vvt_window, text="VVT Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.vvt_label.grid(row = 0, column = 0, columnspan = 8, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.vvt_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.vvt_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, vvt_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.vvt_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.vvt_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, vvt_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.vvt_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.vvt_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, vvt_vals[2])
        self.ventricular_amplitude_label.grid(row = 3, column = 0)
        self.ventricular_amplitude_entry.grid(row = 4, column = 0)

        self.ventricular_pulse_width_label = ttk.Label(self.vvt_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.vvt_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, vvt_vals[3])
        self.ventricular_pulse_width_label.grid(row = 3, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 4, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.vvt_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.vvt_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, vvt_vals[4])
        self.ventricular_sensitivity_label.grid(row = 5, column = 0)
        self.ventricular_sensitivity_entry.grid(row = 6, column = 0)

        self.vrp_label = ttk.Label(self.vvt_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.vvt_window, font=("Arial", 16))
        self.vrp_entry.insert(0, vvt_vals[5])
        self.vrp_label.grid(row = 5, column = 1)
        self.vrp_entry.grid(row = 6, column = 1)

        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.vvt_window, text="Save", style='TButton', command=self.update_vvt)
        self.save_button.grid(row = 7, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.vvt_window, text="Back to Pacing Modes", command=self.vvt_window.destroy)
        self.back_button.grid(row = 8, column = 1)

class VDD_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVDD()

    def update_vdd(self):
        global vdd_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vdd_vals
                vdd_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.fixed_av_delay_entry.get(),self.dynamic_av_delay_entryself.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.pvarp_extension_entry.get(),self.rate_smoothing_entry.get(),self.atr_duration_entry.get(),self.atr_fallback_mode_entry.get(),self.atr_fallback_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.vdd_window.destroy()

    def displayVDD(self):
        self.vdd_window = Tk()
        self.vdd_window.geometry('%dx%d+0+0' % (width, height))
        self.vdd_window.title("VDD Mode")
        self.vdd_window.configure(background="black")

        # Add a title
        self.vdd_label = ttk.Label(self.vdd_window, text="VDD Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.vdd_label.grid(row = 0, column = 0, columnspan = 15, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.vdd_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, vdd_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.vdd_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, vdd_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.fixed_av_delay_label = ttk.Label(self.vdd_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, vdd_vals[1])
        self.fixed_av_delay.grid(row = 3, column = 0)
        self.fixed_av_delay.grid(row = 4, column = 0)

        self.dynamic_av_delay_label = ttk.Label(self.vdd_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, vdd_vals[1])
        self.dynamic_av_delay.grid(row = 3, column = 1)
        self.dynamic_av_delay.grid(row = 4, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.vdd_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, vdd_vals[2])
        self.ventricular_amplitude_label.grid(row = 5, column = 0)
        self.ventricular_amplitude_entry.grid(row = 6, column = 0)

        self.ventricular_pulse_width_label = ttk.Label(self.vdd_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, vdd_vals[3])
        self.ventricular_pulse_width_label.grid(row = 5, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 6, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.vdd_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, vdd_vals[3])
        self.ventricular_sensitivity_label.grid(row = 7, column = 0)
        self.ventricular_sensitivity_entry.grid(row = 8, column = 0)

        self.vrp_label = ttk.Label(self.vdd_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.vrp_entry.insert(0, vdd_vals[3])
        self.vrp_label.grid(row = 7, column = 1)
        self.vrp_entry.grid(row = 8, column = 1)

        self.pvarp_extension_label = ttk.Label(self.vdd_window, text="PVARP Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_extension_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.pvarp_extension_entry.insert(0, vdd_vals[3])
        self.pvarp_extension_label.grid(row = 9, column = 0)
        self.pvarp_extension_entry.grid(row = 10, column = 0)

        self.rate_smoothing_label = ttk.Label(self.vdd_window, text="Rate Smoothing:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smoothing_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, vdd_vals[3])
        self.rate_smoothing_label.grid(row = 9, column = 1)
        self.rate_smoothing_entry.grid(row = 10, column = 1)

        self.atr_duration_label = ttk.Label(self.vdd_window, text="ATR Duration:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_duration_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.atr_duration_entry.insert(0, vdd_vals[3])
        self.atr_duration_label.grid(row = 11, column = 0)
        self.atr_duration_entry.grid(row = 12, column = 0)

        self.atr_fallback_mode_label = ttk.Label(self.vdd_window, text="ATR Fallback Mode:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_mode_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.atr_fallback_mode_entry.insert(0, vdd_vals[3])
        self.atr_fallback_mode_label.grid(row = 11, column = 1)
        self.atr_fallback_mode_entry.grid(row = 12, column = 1)

        self.atr_fallback_time_label = ttk.Label(self.vdd_window, text="ATR Fallback Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_time_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.atr_fallback_time_entry.insert(0, vdd_vals[3])
        self.atr_fallback_time_label.grid(row = 13, column = 0)
        self.atr_fallback_time_entry.grid(row = 14, column = 0)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.vdd_window, text="Save", style='TButton', command=self.update_vdd)
        self.save_button.grid(row = 15, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.vdd_window, text="Back to Pacing Modes", command=self.vdd_window.destroy)
        self.back_button.grid(row = 15, column = 1)


class DOO_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayDOO()

    def update_doo(self):
        global doo_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global doo_vals
                doo_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.fixed_av_delay_entry.get(),self.atrial_amplitude_entry.get(),self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.doo_window.destroy()

    def DOO_Mode(self):
        self.doo_window = Tk()
        self.doo_window.geometry('%dx%d+0+0' % (width, height))
        self.doo_window.title("DOO Mode")
        self.doo_window.configure(background="black")

        # Add a title
        self.doo_label = ttk.Label(self.doo_window, text="DOO Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.doo_label.grid(row = 0, column = 0, columnspan = 9, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.doo_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.doo_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, doo_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.doo_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.doo_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, doo_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        # self.maximum_sensor_rate_label = ttk.Label(self.doo_window, text="Maximum Sensor Rate:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.maximum_sensor_rate_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.maximum_sensor_rate_entry.insert(0, doo_vals[2])
        # self.maximum_sensor_rate.grid(row = 0, column = 1)
        # self.maximum_sensor_rate.grid(row = 0, column = 1)


        self.fixed_av_delay_label = ttk.Label(self.doo_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.doo_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, doo_vals[2])
        self.fixed_av_delay.grid(row = 3, column = 0)
        self.fixed_av_delay.grid(row = 4, column = 0)

        # self.dynamic_av_delay_label = ttk.Label(self.doo_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, doo_vals[3])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        #
        # self.sensed_av_delay_offset_label = ttk.Label(self.doo_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, doo_vals[4])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.doo_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.doo_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, doo_vals[3])
        self.atrial_amplitude_label.grid(row = 3, column = 1)
        self.atrial_amplitude_entry.grid(row = 4, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.doo_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.doo_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, doo_vals[4])
        self.ventricular_amplitude_label.grid(row = 5, column = 0)
        self.ventricular_amplitude_entry.grid(row = 6, column = 0)

        self.atrial_pulse_width_label = ttk.Label(self.doo_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.doo_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, doo_vals[5])
        self.atrial_pulse_width_label.grid(row = 5, column = 1)
        self.atrial_pulse_width_entry.grid(row = 6, column = 1)
        self.ventricular_pulse_width_label = ttk.Label(self.doo_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.doo_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, doo_vals[6])
        self.ventricular_pulse_width_label.grid(row = 7, column = 0)
        self.ventricular_pulse_width_entry.grid(row = 8, column = 0)

        # self.atrial_sensitivity_label = ttk.Label(self.doo_window, text="Atrial Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_sensitivity_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.atrial_sensitivity_entry.insert(0, aat_vals[7])
        # self.atrial_sensitivity_label.grid(row = 0, column = 1)
        # self.atrial_sensitivity_entry.grid(row = 0, column = 1)
        #
        # self.ventricular_sensitivity_label = ttk.Label(self.doo_window, text="Ventricular Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_sensitivity_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.ventricular_sensitivity_entry.insert(0, doo_vals[8])
        # self.ventricular_sensitivity_label.grid(row = 0, column = 1)
        # self.ventricular_sensitivity_entry.grid(row = 0, column = 1)
        #
        # self.vrp_label = ttk.Label(self.doo_window, text="VRP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.vrp_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.vrp_entry.insert(0, doo_vals[9])
        # self.vrp_label.grid(row = 0, column = 1)
        # self.vrp_entry.grid(row = 0, column = 1)
        #
        # self.arp_label = ttk.Label(self.doo_window, text="ARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.arp_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.arp_entry.insert(0, doo_vals[10])
        # self.arp_label.grid(row = 0, column = 1)
        # self.arp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_label = ttk.Label(self.doo_window, text="PVARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.pvarp_entry.insert(0, doo_vals[11])
        # self.pvarp_label.grid(row = 0, column = 1)
        # self.pvarp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_extension_label = ttk.Label(self.doo_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, doo_vals[14])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)
        #
        # self.hysteresis_label = ttk.Label(self.doo_window, text="Hysteresis Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.hysteresis_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.hysteresis_entry.insert(0, doo_vals[15])
        # self.hysteresis_label.grid(row = 0, column = 1)
        # self.hysteresis_entry.grid(row = 0, column = 1)
        #
        # self.rate_smoothing_label = ttk.Label(self.doo_window, text="Rate Smoothing:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.rate_smoothing_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.rate_smoothing_entry.insert(0, doo_vals[16])
        # self.rate_smoothing_label.grid(row = 0, column = 1)
        # self.rate_smoothing_entry.grid(row = 0, column = 1)
        #
        # self.atr_duration_label = ttk.Label(self.doo_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, doo_vals[17])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.doo_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, doo_vals[18])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.doo_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, doo_vals[19])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        # self.activity_threshold_label = ttk.Label(self.doo_window, text="Activity Threshold:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.activity_threshold_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.activity_threshold_entry.insert(0, doo_vals[21])
        # self.activity_threshold_label.grid(row = 0, column = 1)
        # self.activity_threshold_entry.grid(row = 0, column = 1)
        #
        # self.reaction_time_label = ttk.Label(self.doo_window, text="Reaction Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.reaction_time_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.reaction_time_entry.insert(0, doo_vals[22])
        # self.reaction_time_label.grid(row = 0, column = 1)
        # self.reaction_time_entry.grid(row = 0, column = 1)
        #
        # self.response_factor_label = ttk.Label(self.doo_window, text="Response Factor:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.response_factor_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.response_factor_entry.insert(0, doo_vals[23])
        # self.response_factor_label.grid(row = 0, column = 1)
        # self.response_factor_entry.grid(row = 0, column = 1)
        #
        # self.recovery_time_label = ttk.Label(self.doo_window, text="Recovery_ Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.recovery__time_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.recovery__time_entry.insert(0, doo_vals[24])
        # self.recovery__time_label.grid(row = 0, column = 1)
        # self.recovery__time_entry.grid(row = 0, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.doo_window, text="Save", style='TButton', command=self.update_doo)
        self.save_button.grid(row = 9, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.doo_window, text="Back to Pacing Modes", command=self.doo_window.destroy)
        self.back_button.grid(row = 9, column = 1)

class DDI_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayDDI()

    def update_ddi(self):
        global ddi_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global ddi_vals
                ddi_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.fixed_av_delay_entry.get(),self.atrial_amplitude_entry.get(),
                          self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.arp_entry.get(),self.pvarp_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.ddi_window.destroy()

    def displayDDI(self):
        self.ddi_window = Tk()
        self.ddi_window.geometry('%dx%d+0+0' % (width, height))
        self.ddi_window.title("DDI Mode")
        self.ddi_window.configure(background="black")

        # Add a title
        self.ddi_label = ttk.Label(self.ddi_window, text="DDI Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.ddi_label.grid(row = 0, column = 0, columnspan = 13, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.ddi_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, ddi_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.ddi_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, ddi_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        # self.maximum_sensor_rate_label = ttk.Label(self.ddi_window, text="Maximum Sensor Rate:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.maximum_sensor_rate_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.maximum_sensor_rate_entry.insert(0, ddi_vals[2])
        # self.maximum_sensor_rate.grid(row = 0, column = 1)
        # self.maximum_sensor_rate.grid(row = 0, column = 1)


        self.fixed_av_delay_label = ttk.Label(self.ddi_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, ddi_vals[2])
        self.fixed_av_delay.grid(row = 3, column = 0)
        self.fixed_av_delay.grid(row = 4, column = 0)

        # self.dynamic_av_delay_label = ttk.Label(self.ddi_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, ddi_vals[3])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        #
        # self.sensed_av_delay_offset_label = ttk.Label(self.ddi_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, ddi_vals[4])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.ddi_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, ddi_vals[3])
        self.atrial_amplitude_label.grid(row = 3, column = 1)
        self.atrial_amplitude_entry.grid(row = 4, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.ddi_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, ddi_vals[4])
        self.ventricular_amplitude_label.grid(row = 5, column = 0)
        self.ventricular_amplitude_entry.grid(row = 6, column = 0)

        self.atrial_pulse_width_label = ttk.Label(self.ddi_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, ddi_vals[5])
        self.atrial_pulse_width_label.grid(row = 5, column = 1)
        self.atrial_pulse_width_entry.grid(row = 6, column = 1)
        self.ventricular_pulse_width_label = ttk.Label(self.ddi_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, ddi_vals[6])
        self.ventricular_pulse_width_label.grid(row = 7, column = 0)
        self.ventricular_pulse_width_entry.grid(row = 8, column = 0)

        self.atrial_sensitivity_label = ttk.Label(self.ddi_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, ddi_vals[7])
        self.atrial_sensitivity_label.grid(row = 7, column = 1)
        self.atrial_sensitivity_entry.grid(row = 8, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.ddi_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, ddi_vals[8])
        self.ventricular_sensitivity_label.grid(row = 9, column = 0)
        self.ventricular_sensitivity_entry.grid(row = 10, column = 0)

        self.vrp_label = ttk.Label(self.ddi_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.vrp_entry.insert(0, ddi_vals[9])
        self.vrp_label.grid(row = 9, column = 1)
        self.vrp_entry.grid(row = 10, column = 1)

        self.arp_label = ttk.Label(self.ddi_window, text="ARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.arp_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.arp_entry.insert(0, ddi_vals[10])
        self.arp_label.grid(row = 11, column = 0)
        self.arp_entry.grid(row = 12, column = 0)

        self.pvarp_label = ttk.Label(self.ddi_window, text="PVARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_entry = Entry(self.ddi_window, font=("Arial", 16))
        self.pvarp_entry.insert(0, ddi_vals[11])
        self.pvarp_label.grid(row = 11, column = 1)
        self.pvarp_entry.grid(row = 12, column = 1)
        #
        # self.pvarp_extension_label = ttk.Label(self.ddi_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, ddi_vals[14])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)
        #
        # self.hysteresis_label = ttk.Label(self.ddi_window, text="Hysteresis Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.hysteresis_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.hysteresis_entry.insert(0, ddi_vals[15])
        # self.hysteresis_label.grid(row = 0, column = 1)
        # self.hysteresis_entry.grid(row = 0, column = 1)
        #
        # self.rate_smoothing_label = ttk.Label(self.ddi_window, text="Rate Smoothing:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.rate_smoothing_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.rate_smoothing_entry.insert(0, ddi_vals[16])
        # self.rate_smoothing_label.grid(row = 0, column = 1)
        # self.rate_smoothing_entry.grid(row = 0, column = 1)
        #
        # self.atr_duration_label = ttk.Label(self.ddi_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, ddi_vals[17])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.ddi_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, ddi_vals[18])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.ddi_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, ddi_vals[19])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        # self.activity_threshold_label = ttk.Label(self.ddi_window, text="Activity Threshold:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.activity_threshold_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.activity_threshold_entry.insert(0, ddi_vals[21])
        # self.activity_threshold_label.grid(row = 0, column = 1)
        # self.activity_threshold_entry.grid(row = 0, column = 1)
        #
        # self.reaction_time_label = ttk.Label(self.ddi_window, text="Reaction Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.reaction_time_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.reaction_time_entry.insert(0, ddi_vals[22])
        # self.reaction_time_label.grid(row = 0, column = 1)
        # self.reaction_time_entry.grid(row = 0, column = 1)
        #
        # self.response_factor_label = ttk.Label(self.ddi_window, text="Response Factor:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.response_factor_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.response_factor_entry.insert(0, ddi_vals[23])
        # self.response_factor_label.grid(row = 0, column = 1)
        # self.response_factor_entry.grid(row = 0, column = 1)
        #
        # self.recovery_time_label = ttk.Label(self.ddi_window, text="Recovery_ Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.recovery__time_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.recovery__time_entry.insert(0, ddi_vals[24])
        # self.recovery__time_label.grid(row = 0, column = 1)
        # self.recovery__time_entry.grid(row = 0, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.ddi_window, text="Save", style='TButton', command=self.update_ddi)
        self.save_button.grid(row = 13, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.ddi_window, text="Back to Pacing Modes", command=self.ddi_window.destroy)
        self.back_button.grid(row = 13, column = 1)

class DDD_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayDDD()

    def update_ddd(self):
        global ddd_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global ddd_vals
                ddd_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.fixed_av_delay_entry.get(),self.dynamic_av_delay_entry.get(),self.sensed_av_delay_offset_entry.get(),self.atrial_amplitude_entry.get(),
                            self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.arp_entry.get(),
                            self.pvarp_entry.get(),self.pvarp_extension_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get(),self.atr_duration_entry.get(),self.atr_fallback_mode_entry.get(),self.atr_fallback_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.ddd_window.destroy()

    def displayDDD(self):
        self.ddd_window = Tk()
        self.ddd_window.geometry('%dx%d+0+0' % (width, height))
        self.ddd_window.title("DDD Mode")
        self.ddd_window.configure(background="black")

        # Add a title
        self.ddd_label = ttk.Label(self.ddd_window, text="DDD Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.ddd_label.grid(row = 0, column = 0, columnspan = 21, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.ddd_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, ddd_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.ddd_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, ddd_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        # self.maximum_sensor_rate_label = ttk.Label(self.ddd_window, text="Maximum Sensor Rate:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.maximum_sensor_rate_entry = Entry(self.ddd_window, font=("Arial", 16))
        # self.maximum_sensor_rate_entry.insert(0, ddd_vals[2])
        # self.maximum_sensor_rate.grid(row = 0, column = 1)
        # self.maximum_sensor_rate.grid(row = 0, column = 1)


        self.fixed_av_delay_label = ttk.Label(self.ddd_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, ddd_vals[2])
        self.fixed_av_delay.grid(row = 3, column = 0)
        self.fixed_av_delay.grid(row = 4, column = 0)

        self.dynamic_av_delay_label = ttk.Label(self.ddd_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, ddd_vals[3])
        self.dynamic_av_delay.grid(row = 3, column = 1)
        self.dynamic_av_delay.grid(row = 4, column = 1)

        self.sensed_av_delay_offset_label = ttk.Label(self.ddd_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.sensed_av_delay_offset_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.sensed_av_delay_offset_entry.insert(0, ddd_vals[4])
        self.sensed_av_delay_offset.grid(row = 5, column = 0)
        self.sensed_av_delay_offset.grid(row = 6, column = 0)

        self.atrial_amplitude_label = ttk.Label(self.ddd_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, ddd_vals[5])
        self.atrial_amplitude_label.grid(row = 5, column = 1)
        self.atrial_amplitude_entry.grid(row = 6, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.ddd_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, ddd_vals[6])
        self.ventricular_amplitude_label.grid(row = 7, column = 0)
        self.ventricular_amplitude_entry.grid(row = 8, column = 0)

        self.atrial_pulse_width_label = ttk.Label(self.ddd_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, ddd_vals[7])
        self.atrial_pulse_width_label.grid(row = 7, column = 1)
        self.atrial_pulse_width_entry.grid(row = 8, column = 1)
        self.ventricular_pulse_width_label = ttk.Label(self.ddd_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, ddd_vals[8])
        self.ventricular_pulse_width_label.grid(row = 9, column = 0)
        self.ventricular_pulse_width_entry.grid(row = 10, column = 0)

        self.atrial_sensitivity_label = ttk.Label(self.ddd_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, ddd_vals[9])
        self.atrial_sensitivity_label.grid(row = 9, column = 1)
        self.atrial_sensitivity_entry.grid(row = 10, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.ddd_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, ddd_vals[10])
        self.ventricular_sensitivity_label.grid(row = 11, column = 0)
        self.ventricular_sensitivity_entry.grid(row = 12, column = 0)

        self.vrp_label = ttk.Label(self.ddd_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.vrp_entry.insert(0, ddd_vals[11])
        self.vrp_label.grid(row = 11, column = 1)
        self.vrp_entry.grid(row = 12, column = 1)

        self.arp_label = ttk.Label(self.ddd_window, text="ARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.arp_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.arp_entry.insert(0, ddd_vals[12])
        self.arp_label.grid(row = 13, column = 0)
        self.arp_entry.grid(row = 14, column = 0)

        self.pvarp_label = ttk.Label(self.ddd_window, text="PVARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.pvarp_entry.insert(0, ddd_vals[13])
        self.pvarp_label.grid(row = 13, column =1)
        self.pvarp_entry.grid(row = 14, column =1)

        self.pvarp_extension_label = ttk.Label(self.ddd_window, text="PVARP Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_extension_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.pvarp_extension_entry.insert(0, ddd_vals[14])
        self.pvarp_extension_label.grid(row = 15, column = 0)
        self.pvarp_extension_entry.grid(row = 16, column = 0)

        self.hysteresis_label = ttk.Label(self.ddd_window, text="Hysteresis Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.hysteresis_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.hysteresis_entry.insert(0, ddd_vals[15])
        self.hysteresis_label.grid(row = 15, column = 1)
        self.hysteresis_entry.grid(row = 16, column = 1)

        self.rate_smoothing_label = ttk.Label(self.ddd_window, text="Rate Smoothing:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smoothing_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, ddd_vals[16])
        self.rate_smoothing_label.grid(row = 17, column = 0)
        self.rate_smoothing_entry.grid(row = 18, column = 0)

        self.atr_duration_label = ttk.Label(self.ddd_window, text="ATR Duration:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_duration_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.atr_duration_entry.insert(0, ddd_vals[17])
        self.atr_duration_label.grid(row = 17, column = 1)
        self.atr_duration_entry.grid(row = 18, column = 1)

        self.atr_fallback_mode_label = ttk.Label(self.ddd_window, text="ATR Fallback Mode:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_mode_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.atr_fallback_mode_entry.insert(0, ddd_vals[18])
        self.atr_fallback_mode_label.grid(row = 19, column = 0)
        self.atr_fallback_mode_entry.grid(row = 20, column = 0)

        self.atr_fallback_time_label = ttk.Label(self.ddd_window, text="ATR Fallback Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_time_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.atr_fallback_time_entry.insert(0, ddd_vals[19])
        self.atr_fallback_time_label.grid(row = 19, column = 1)
        self.atr_fallback_time_entry.grid(row = 20, column = 1)

        # self.activity_threshold_label = ttk.Label(self.ddd_window, text="Activity Threshold:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.activity_threshold_entry = Entry(self.ddd_window, font=("Arial", 16))
        # self.activity_threshold_entry.insert(0, ddd_vals[21])
        # self.activity_threshold_label.grid(row = 0, column = 1)
        # self.activity_threshold_entry.grid(row = 0, column = 1)
        #
        # self.reaction_time_label = ttk.Label(self.ddd_window, text="Reaction Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.reaction_time_entry = Entry(self.ddd_window, font=("Arial", 16))
        # self.reaction_time_entry.insert(0, ddd_vals[22])
        # self.reaction_time_label.grid(row = 0, column = 1)
        # self.reaction_time_entry.grid(row = 0, column = 1)
        #
        # self.response_factor_label = ttk.Label(self.ddd_window, text="Response Factor:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.response_factor_entry = Entry(self.ddd_window, font=("Arial", 16))
        # self.response_factor_entry.insert(0, ddd_vals[23])
        # self.response_factor_label.grid(row = 0, column = 1)
        # self.response_factor_entry.grid(row = 0, column = 1)
        #
        # self.recovery_time_label = ttk.Label(self.ddd_window, text="Recovery_ Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.recovery__time_entry = Entry(self.ddd_window, font=("Arial", 16))
        # self.recovery__time_entry.insert(0, ddd_vals[24])
        # self.recovery__time_label.grid(row = 0, column = 1)
        # self.recovery__time_entry.grid(row = 0, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.ddd_window, text="Save", style='TButton', command=self.update_ddd)
        self.save_button.grid(row = 21, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.ddd_window, text="Back to Pacing Modes", command=self.ddd_window.destroy)
        self.back_button.grid(row = 21, column = 1)

class AOOR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayAOOR()

    def update_aoor(self):
        global aoor_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aoor_vals
                aoor_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),
                            self.acticity_threshold_entry.get(),
                            self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.aoor_window.destroy()

    def displayAOOR(self):
        self.aoor_window = Tk()
        self.aoor_window.geometry('%dx%d+0+0' % (width, height))
        self.aoor_window.title("AOOR Mode")
        self.aoor_window.configure(background="black")

        # Add a title
        self.aoor_label = ttk.Label(self.aoor_window, text="AOOR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.aoor_label.grid(row = 0, column = 0, columnspan = 11, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.aoor_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, aoor_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.aoor_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, aoor_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.aoor_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, aoor_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        # self.fixed_av_delay_label = ttk.Label(self.aoor_window, text="Fixed AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.fixed_av_delay_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.fixed_av_delay_entry.insert(0, aoor_vals[3])
        # self.fixed_av_delay.grid(row = 0, column = 1)
        # self.fixed_av_delay.grid(row = 0, column = 1)
        #
        # self.dynamic_av_delay_label = ttk.Label(self.aoor_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, aoor_vals[4])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        #
        # self.sensed_av_delay_offset_label = ttk.Label(self.aoor_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, aoor_vals[5])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.aoor_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, aoor_vals[3])
        self.atrial_amplitude_label.grid(row = 3, column = 1)
        self.atrial_amplitude_entry.grid(row = 4, column = 1)

        # self.ventricular_amplitude_label = ttk.Label(self.aoor_window, text="Ventricular Amplitude:", background="black", foreground="white",
        #                                    font=("Arial", 16))
        # self.ventricular_amplitude_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.ventricular_amplitude_entry.insert(0, aoor_vals[7])
        # self.ventricular_amplitude_label.grid(row = 0, column = 1)
        # self.ventricular_amplitude_entry.grid(row = 0, column = 1)

        self.atrial_pulse_width_label = ttk.Label(self.aoor_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, aoor_vals[4])
        self.atrial_pulse_width_label.grid(row = 5, column = 0)
        self.atrial_pulse_width_entry.grid(row = 6, column = 0)
        # self.ventricular_pulse_width_label = ttk.Label(self.aoor_window, text="Ventricular Pulse Width:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_pulse_width_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.ventricular_pulse_width_entry.insert(0, aoor_vals[9])
        # self.ventricular_pulse_width_label.grid(row = 0, column = 1)
        # self.ventricular_pulse_width_entry.grid(row = 0, column = 1)

        self.atrial_sensitivity_label = ttk.Label(self.aoor_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, aoor_vals[5])
        self.atrial_sensitivity_label.grid(row = 5, column = 1)
        self.atrial_sensitivity_entry.grid(row = 6, column = 1)

        # self.ventricular_sensitivity_label = ttk.Label(self.aoor_window, text="Ventricular Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_sensitivity_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.ventricular_sensitivity_entry.insert(0, aoor_vals[11])
        # self.ventricular_sensitivity_label.grid(row = 0, column = 1)
        # self.ventricular_sensitivity_entry.grid(row = 0, column = 1)

        # self.vrp_label = ttk.Label(self.aoor_window, text="VRP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.vrp_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.vrp_entry.insert(0, aoor_vals[12])
        # self.vrp_label.grid(row = 0, column = 1)
        # self.vrp_entry.grid(row = 0, column = 1)

        # self.arp_label = ttk.Label(self.aoor_window, text="ARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.arp_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.arp_entry.insert(0, aoor_vals[6])
        # self.arp_label.grid(row = 0, column = 1)
        # self.arp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_label = ttk.Label(self.aoor_window, text="PVARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.pvarp_entry.insert(0, aoor_vals[7])
        # self.pvarp_label.grid(row = 0, column = 1)
        # self.pvarp_entry.grid(row = 0, column = 1)

        # self.pvarp_extension_label = ttk.Label(self.aoor_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, aoor_vals[15])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)

        # self.hysteresis_label = ttk.Label(self.aoor_window, text="Hysteresis Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.hysteresis_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.hysteresis_entry.insert(0, aoor_vals[8])
        # self.hysteresis_label.grid(row = 0, column = 1)
        # self.hysteresis_entry.grid(row = 0, column = 1)
        #
        # self.rate_smoothing_label = ttk.Label(self.aoor_window, text="Rate Smoothing:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.rate_smoothing_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.rate_smoothing_entry.insert(0, aoor_vals[9])
        # self.rate_smoothing_label.grid(row = 0, column = 1)
        # self.rate_smoothing_entry.grid(row = 0, column = 1)

        # self.atr_duration_label = ttk.Label(self.aoor_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, aoor_vals[18])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.aoor_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, aoor_vals[19])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.aoor_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.aoor_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, aoor_vals[20])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        self.activity_threshold_label = ttk.Label(self.aoor_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, aoor_vals[6])
        self.activity_threshold_label.grid(row = 7, column = 0)
        self.activity_threshold_entry.grid(row = 8, column = 0)

        self.reaction_time_label = ttk.Label(self.aoor_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, aoor_vals[7])
        self.reaction_time_label.grid(row = 7, column = 1)
        self.reaction_time_entry.grid(row = 8, column = 1)

        self.response_factor_label = ttk.Label(self.aoor_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, aoor_vals[8])
        self.response_factor_label.grid(row = 9, column = 0)
        self.response_factor_entry.grid(row = 10, column = 0)

        self.recovery_time_label = ttk.Label(self.aoor_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, aoor_vals[9])
        self.recovery__time_label.grid(row = 9, column = 1)
        self.recovery__time_entry.grid(row = 10, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.aoor_window, text="Save", style='TButton', command=self.update_aoor)
        self.save_button.grid(row = 11, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.aoor_window, text="Back to Pacing Modes", command=self.aoor_window.destroy)
        self.back_button.grid(row = 11, column = 1)


class AAIR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayAAIR()

    def update_aair(self):
        global aair_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aair_vals
                aair_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.arp_entry.get(),self.pvarp_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get(),
                            self.acticity_threshold_entry.get(),
                            self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]



        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.aair_window.destroy()

    def displayAAIR(self):
        self.aair_window = Tk()
        self.aair_window.geometry('%dx%d+0+0' % (width, height))
        self.aair_window.title("AAIR Mode")
        self.aair_window.configure(background="black")

        # Add a title
        self.aair_label = ttk.Label(self.aair_window, text="AAIR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.aair_label.grid(row = 0, column = 0, columnspan = 15, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.aair_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.aair_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, aair_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.aair_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.aair_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, aair_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.aair_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.aair_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, aair_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        # self.fixed_av_delay_label = ttk.Label(self.aair_window, text="Fixed AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.fixed_av_delay_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.fixed_av_delay_entry.insert(0, aair_vals[3])
        # self.fixed_av_delay.grid(row = 0, column = 1)
        # self.fixed_av_delay.grid(row = 0, column = 1)
        #
        # self.dynamic_av_delay_label = ttk.Label(self.aair_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, aair_vals[4])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        #
        # self.sensed_av_delay_offset_label = ttk.Label(self.aair_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, aair_vals[5])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.aair_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.aair_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, aair_vals[3])
        self.atrial_amplitude_label.grid(row = 3, column = 1)
        self.atrial_amplitude_entry.grid(row = 4, column = 1)

        # self.ventricular_amplitude_label = ttk.Label(self.aair_window, text="Ventricular Amplitude:", background="black", foreground="white",
        #                                    font=("Arial", 16))
        # self.ventricular_amplitude_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.ventricular_amplitude_entry.insert(0, aair_vals[7])
        # self.ventricular_amplitude_label.grid(row = 0, column = 1)
        # self.ventricular_amplitude_entry.grid(row = 0, column = 1)

        self.atrial_pulse_width_label = ttk.Label(self.aair_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.aair_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, aair_vals[4])
        self.atrial_pulse_width_label.grid(row = 5, column = 0)
        self.atrial_pulse_width_entry.grid(row = 6, column = 0)
        # self.ventricular_pulse_width_label = ttk.Label(self.aair_window, text="Ventricular Pulse Width:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_pulse_width_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.ventricular_pulse_width_entry.insert(0, aair_vals[9])
        # self.ventricular_pulse_width_label.grid(row = 0, column = 1)
        # self.ventricular_pulse_width_entry.grid(row = 0, column = 1)

        self.atrial_sensitivity_label = ttk.Label(self.aair_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.aair_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, aair_vals[5])
        self.atrial_sensitivity_label.grid(row = 5, column = 1)
        self.atrial_sensitivity_entry.grid(row = 6, column = 1)

        # self.ventricular_sensitivity_label = ttk.Label(self.aair_window, text="Ventricular Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_sensitivity_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.ventricular_sensitivity_entry.insert(0, aair_vals[11])
        # self.ventricular_sensitivity_label.grid(row = 0, column = 1)
        # self.ventricular_sensitivity_entry.grid(row = 0, column = 1)

        # self.vrp_label = ttk.Label(self.aair_window, text="VRP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.vrp_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.vrp_entry.insert(0, aair_vals[12])
        # self.vrp_label.grid(row = 0, column = 1)
        # self.vrp_entry.grid(row = 0, column = 1)

        self.arp_label = ttk.Label(self.aair_window, text="ARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.arp_entry = Entry(self.aair_window, font=("Arial", 16))
        self.arp_entry.insert(0, aair_vals[6])
        self.arp_label.grid(row = 7, column = 0)
        self.arp_entry.grid(row = 8, column = 0)

        self.pvarp_label = ttk.Label(self.aair_window, text="PVARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_entry = Entry(self.aair_window, font=("Arial", 16))
        self.pvarp_entry.insert(0, aair_vals[7])
        self.pvarp_label.grid(row = 7, column = 1)
        self.pvarp_entry.grid(row = 8, column = 1)

        # self.pvarp_extension_label = ttk.Label(self.aair_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, aair_vals[15])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)

        self.hysteresis_label = ttk.Label(self.aair_window, text="Hysteresis Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.hysteresis_entry = Entry(self.aair_window, font=("Arial", 16))
        self.hysteresis_entry.insert(0, aair_vals[8])
        self.hysteresis_label.grid(row = 9, column = 0)
        self.hysteresis_entry.grid(row = 10, column = 0)

        self.rate_smoothing_label = ttk.Label(self.aair_window, text="Rate Smoothing:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smoothing_entry = Entry(self.aair_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, aair_vals[9])
        self.rate_smoothing_label.grid(row = 9, column = 1)
        self.rate_smoothing_entry.grid(row = 10, column = 1)

        # self.atr_duration_label = ttk.Label(self.aair_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, aair_vals[18])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.aair_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, aair_vals[19])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.aair_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.aair_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, aair_vals[20])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        self.activity_threshold_label = ttk.Label(self.aair_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.aair_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, aair_vals[10])
        self.activity_threshold_label.grid(row = 11, column = 0)
        self.activity_threshold_entry.grid(row = 12, column = 0)

        self.reaction_time_label = ttk.Label(self.aair_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.aair_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, aair_vals[11])
        self.reaction_time_label.grid(row = 11, column = 1)
        self.reaction_time_entry.grid(row = 12, column = 1)

        self.response_factor_label = ttk.Label(self.aair_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.aair_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, aair_vals[12])
        self.response_factor_label.grid(row = 13, column = 0)
        self.response_factor_entry.grid(row = 14, column = 0)

        self.recovery_time_label = ttk.Label(self.aair_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.aair_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, aair_vals[13])
        self.recovery__time_label.grid(row = 13, column = 1)
        self.recovery__time_entry.grid(row = 14, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.aairr_window, text="Save", style='TButton', command=self.update_aair)
        self.save_button.grid(row = 15, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.aair_window, text="Back to Pacing Modes", command=self.aair_window.destroy)
        self.back_button.grid(row = 15, column = 1)

class VOOR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVOOR()

    def update_voor(self):
        global voor_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global voor_vals
                voor_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),
                            self.acticity_threshold_entry.get(),
                            self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.voor_window.destroy()

    def displayVOOR(self):
        self.voor_window = Tk()
        self.voor_window.geometry('%dx%d+0+0' % (width, height))
        self.voor_window.title("VOOR Mode")
        self.voor_window.configure(background="black")

        # Add a title
        self.voor_label = ttk.Label(self.voor_window, text="VOOR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.voor_label.grid(row = 0, column = 0, columnspan = 11, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.voor_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.voor_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, voor_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.voor_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.voor_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, voor_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.voor_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.voor_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, voor_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        # self.fixed_av_delay_label = ttk.Label(self.voor_window, text="Fixed AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.fixed_av_delay_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.fixed_av_delay_entry.insert(0, voor_vals[3])
        # self.fixed_av_delay.grid(row = 0, column = 1)
        # self.fixed_av_delay.grid(row = 0, column = 1)

        # self.dynamic_av_delay_label = ttk.Label(self.voor_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, voor_vals[4])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)

        # self.sensed_av_delay_offset_label = ttk.Label(self.voor_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, voor_vals[5])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        #
        # self.atrial_amplitude_label = ttk.Label(self.voor_window, text="Atrial Amplitude:", background="black", foreground="white",
        #                                    font=("Arial", 16))
        # self.atrial_amplitude_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.atrial_amplitude_entry.insert(0, voor_vals[6])
        # self.atrial_amplitude_label.grid(row = 0, column = 1)
        # self.atrial_amplitude_entry.grid(row = 0, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.voor_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.voor_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, voor_vals[3])
        self.ventricular_amplitude_label.grid(row = 3, column = 1)
        self.ventricular_amplitude_entry.grid(row = 4, column = 1)

        # self.atrial_pulse_width_label = ttk.Label(self.voor_window, text="Atrial Pulse Width:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_pulse_width_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.atrial_pulse_width_entry.insert(0, voor_vals[8])
        # self.atrial_pulse_width_label.grid(row = 0, column = 1)
        # self.atrial_pulse_width_entry.grid(row = 0, column = 1)
        self.ventricular_pulse_width_label = ttk.Label(self.voor_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.voor_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, voor_vals[4])
        self.ventricular_pulse_width_label.grid(row = 5, column = 0)
        self.ventricular_pulse_width_entry.grid(row = 6, column = 0)

        # self.atrial_sensitivity_label = ttk.Label(self.voor_window, text="Atrial Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_sensitivity_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.atrial_sensitivity_entry.insert(0, aat_vals[10])
        # self.atrial_sensitivity_label.grid(row = 0, column = 1)
        # self.atrial_sensitivity_entry.grid(row = 0, column = 1)

        # self.ventricular_sensitivity_label = ttk.Label(self.voor_window, text="Ventricular Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_sensitivity_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.ventricular_sensitivity_entry.insert(0, voor_vals[5])
        # self.ventricular_sensitivity_label.grid(row = 0, column = 1)
        # self.ventricular_sensitivity_entry.grid(row = 0, column = 1)
        #
        # self.vrp_label = ttk.Label(self.voor_window, text="VRP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.vrp_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.vrp_entry.insert(0, voor_vals[6])
        # self.vrp_label.grid(row = 0, column = 1)
        # self.vrp_entry.grid(row = 0, column = 1)

        # self.arp_label = ttk.Label(self.voor_window, text="ARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.arp_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.arp_entry.insert(0, voor_vals[13])
        # self.arp_label.grid(row = 0, column = 1)
        # self.arp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_label = ttk.Label(self.voor_window, text="PVARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.pvarp_entry.insert(0, voor_vals[14])
        # self.pvarp_label.grid(row = 0, column = 1)
        # self.pvarp_entry.grid(row = 0, column = 1)

        # self.pvarp_extension_label = ttk.Label(self.voor_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, voor_vals[9])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)

        # self.hysteresis_label = ttk.Label(self.voor_window, text="Hysteresis Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.hysteresis_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.hysteresis_entry.insert(0, voor_vals[7])
        # self.hysteresis_label.grid(row = 0, column = 1)
        # self.hysteresis_entry.grid(row = 0, column = 1)
        #
        # self.rate_smoothing_label = ttk.Label(self.voor_window, text="Rate Smoothing:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.rate_smoothing_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.rate_smoothing_entry.insert(0, voor_vals[8])
        # self.rate_smoothing_label.grid(row = 0, column = 1)
        # self.rate_smoothing_entry.grid(row = 0, column = 1)

        # self.atr_duration_label = ttk.Label(self.voor_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, voor_vals[11])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.voor_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, voor_vals[12])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.voor_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.voor_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, voor_vals[13])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        self.activity_threshold_label = ttk.Label(self.voor_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.voor_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, voor_vals[5])
        self.activity_threshold_label.grid(row = 5, column = 1)
        self.activity_threshold_entry.grid(row = 6, column = 1)

        self.reaction_time_label = ttk.Label(self.voor_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.voor_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, voor_vals[6])
        self.reaction_time_label.grid(row = 7, column = 0)
        self.reaction_time_entry.grid(row = 8, column = 0)

        self.response_factor_label = ttk.Label(self.voor_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.voor_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, voor_vals[7])
        self.response_factor_label.grid(row = 7, column = 1)
        self.response_factor_entry.grid(row = 8, column = 1)

        self.recovery_time_label = ttk.Label(self.voor_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.voor_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, voor_vals[8])
        self.recovery__time_label.grid(row = 9, column = 0)
        self.recovery__time_entry.grid(row = 10, column = 0)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.voor_window, text="Save", style='TButton', command=self.update_voor)
        self.save_button.grid(row = 11, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.voor_window, text="Back to Pacing Modes", command=self.voor_window.destroy)
        self.back_button.grid(row = 11, column = 1)


class VVIR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVVIR()

    def update_vvir(self):
        global vvir_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vvir_vals
                vvir_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get(),
                            self.acticity_threshold_entry.get(),
                            self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.vvir_window.destroy()

    def displayVVIR(self):
        self.vvir_window = Tk()
        self.vvir_window.geometry('%dx%d+0+0' % (width, height))
        self.vvir_window.title("VVIR Mode")
        self.vvir_window.configure(background="black")

        # Add a title
        self.vvir_label = ttk.Label(self.vvir_window, text="VVIR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.vvir_label.grid(row = 0, column = 0, columnspan = 15, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.vvir_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, vvir_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.vvir_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, vvir_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.vvir_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, vvir_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        # self.fixed_av_delay_label = ttk.Label(self.vvir_window, text="Fixed AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.fixed_av_delay_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.fixed_av_delay_entry.insert(0, vvir_vals[3])
        # self.fixed_av_delay.grid(row = 0, column = 1)
        # self.fixed_av_delay.grid(row = 0, column = 1)

        # self.dynamic_av_delay_label = ttk.Label(self.vvir_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, vvir_vals[4])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)

        # self.sensed_av_delay_offset_label = ttk.Label(self.vvir_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, vvir_vals[5])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        #
        # self.atrial_amplitude_label = ttk.Label(self.vvir_window, text="Atrial Amplitude:", background="black", foreground="white",
        #                                    font=("Arial", 16))
        # self.atrial_amplitude_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.atrial_amplitude_entry.insert(0, vvir_vals[6])
        # self.atrial_amplitude_label.grid(row = 0, column = 1)
        # self.atrial_amplitude_entry.grid(row = 0, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.vvir_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, vvir_vals[3])
        self.ventricular_amplitude_label.grid(row = 3, column = 1)
        self.ventricular_amplitude_entry.grid(row = 4, column = 1)

        # self.atrial_pulse_width_label = ttk.Label(self.vvir_window, text="Atrial Pulse Width:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_pulse_width_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.atrial_pulse_width_entry.insert(0, vvir_vals[8])
        # self.atrial_pulse_width_label.grid(row = 0, column = 1)
        # self.atrial_pulse_width_entry.grid(row = 0, column = 1)
        self.ventricular_pulse_width_label = ttk.Label(self.vvir_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, vvir_vals[4])
        self.ventricular_pulse_width_label.grid(row = 5, column = 0)
        self.ventricular_pulse_width_entry.grid(row = 6, column = 0)

        # self.atrial_sensitivity_label = ttk.Label(self.vvir_window, text="Atrial Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_sensitivity_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.atrial_sensitivity_entry.insert(0, aat_vals[10])
        # self.atrial_sensitivity_label.grid(row = 0, column = 1)
        # self.atrial_sensitivity_entry.grid(row = 0, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.vvir_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, vvir_vals[5])
        self.ventricular_sensitivity_label.grid(row = 5, column = 1)
        self.ventricular_sensitivity_entry.grid(row = 6, column = 1)

        self.vrp_label = ttk.Label(self.vvir_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.vrp_entry.insert(0, vvir_vals[6])
        self.vrp_label.grid(row = 7, column = 0)
        self.vrp_entry.grid(row = 8, column = 0)

        # self.arp_label = ttk.Label(self.vvir_window, text="ARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.arp_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.arp_entry.insert(0, vvir_vals[13])
        # self.arp_label.grid(row = 0, column = 1)
        # self.arp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_label = ttk.Label(self.vvir_window, text="PVARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.pvarp_entry.insert(0, vvir_vals[14])
        # self.pvarp_label.grid(row = 0, column = 1)
        # self.pvarp_entry.grid(row = 0, column = 1)

        # self.pvarp_extension_label = ttk.Label(self.vvir_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, vvir_vals[9])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)

        self.hysteresis_label = ttk.Label(self.vvir_window, text="Hysteresis Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.hysteresis_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.hysteresis_entry.insert(0, vvir_vals[7])
        self.hysteresis_label.grid(row = 7, column = 1)
        self.hysteresis_entry.grid(row = 8, column = 1)

        self.rate_smoothing_label = ttk.Label(self.vvir_window, text="Rate Smoothing:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smoothing_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, vvir_vals[8])
        self.rate_smoothing_label.grid(row = 9, column = 0)
        self.rate_smoothing_entry.grid(row = 10, column = 0)

        # self.atr_duration_label = ttk.Label(self.vvir_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, vvir_vals[11])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.vvir_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, vvir_vals[12])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.vvir_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.vvir_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, vvir_vals[13])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        self.activity_threshold_label = ttk.Label(self.vvir_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, vvir_vals[9])
        self.activity_threshold_label.grid(row = 9, column = 1)
        self.activity_threshold_entry.grid(row = 10, column = 1)

        self.reaction_time_label = ttk.Label(self.vvir_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, vvir_vals[10])
        self.reaction_time_label.grid(row = 11, column = 0)
        self.reaction_time_entry.grid(row = 12, column = 0)

        self.response_factor_label = ttk.Label(self.vvir_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, vvir_vals[11])
        self.response_factor_label.grid(row = 11, column = 1)
        self.response_factor_entry.grid(row = 12, column = 1)

        self.recovery_time_label = ttk.Label(self.vvir_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, vvir_vals[12])
        self.recovery__time_label.grid(row = 13, column = 0)
        self.recovery__time_entry.grid(row = 14, column = 0)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.vvir_window, text="Save", style='TButton', command=self.update_vvir)
        self.save_button.grid(row = 15, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.vvir_window, text="Back to Pacing Modes", command=self.vvir_window.destroy)
        self.back_button.grid(row = 15, column = 1)


class VDDR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVDDR()

    def update_vddr(self):
        global vddr_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vddr_vals
                vddr_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.fixed_av_delay_entry.get(),self.dynamic_av_delay_entry.get(),
                            self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),
                            self.pvarp_extension_entry.get(),self.rate_smoothing_entry.get(),self.atr_duration_entry.get(),self.atr_fallback_mode_entry.get(),self.atr_fallback_time_entry.get(),self.acticity_threshold_entry.get(),
                            self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.vddr_window.destroy()

    def displayVDDR(self):
        self.vddr_window = Tk()
        self.vddr_window.geometry('%dx%d+0+0' % (width, height))
        self.vddr_window.title("VDDR Mode")
        self.vddr_window.configure(background="black")

        # Add a title
        self.vddr_label = ttk.Label(self.vddr_window, text="VDDR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.vddr_label.pgrid(row = 0, column = 0, columnspan = 19, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.vddr_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, vddr_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.vddr_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, vddr_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.vddr_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, vddr_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.vddr_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, vddr_vals[3])
        self.fixed_av_delay.grid(row = 3, column = 1)
        self.fixed_av_delay.grid(row = 4, column = 1)

        self.dynamic_av_delay_label = ttk.Label(self.vddr_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, vddr_vals[4])
        self.dynamic_av_delay.grid(row = 5, column = 0)
        self.dynamic_av_delay.grid(row = 6, column = 0)

        # self.sensed_av_delay_offset_label = ttk.Label(self.vddr_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.vddr_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, vddr_vals[5])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        #
        # self.atrial_amplitude_label = ttk.Label(self.vddr_window, text="Atrial Amplitude:", background="black", foreground="white",
        #                                    font=("Arial", 16))
        # self.atrial_amplitude_entry = Entry(self.vddr_window, font=("Arial", 16))
        # self.atrial_amplitude_entry.insert(0, vddr_vals[6])
        # self.atrial_amplitude_label.grid(row = 0, column = 1)
        # self.atrial_amplitude_entry.grid(row = 0, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.vddr_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, vddr_vals[5])
        self.ventricular_amplitude_label.grid(row = 5, column = 1)
        self.ventricular_amplitude_entry.grid(row = 6, column = 1)

        # self.atrial_pulse_width_label = ttk.Label(self.vddr_window, text="Atrial Pulse Width:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_pulse_width_entry = Entry(self.vddr_window, font=("Arial", 16))
        # self.atrial_pulse_width_entry.insert(0, vddr_vals[8])
        # self.atrial_pulse_width_label.grid(row = 0, column = 1)
        # self.atrial_pulse_width_entry.grid(row = 0, column = 1)
        self.ventricular_pulse_width_label = ttk.Label(self.vddr_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, vddr_vals[6])
        self.ventricular_pulse_width_label.grid(row = 7, column = 0)
        self.ventricular_pulse_width_entry.grid(row = 8, column = 0)

        # self.atrial_sensitivity_label = ttk.Label(self.vddr_window, text="Atrial Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_sensitivity_entry = Entry(self.vddr_window, font=("Arial", 16))
        # self.atrial_sensitivity_entry.insert(0, aat_vals[10])
        # self.atrial_sensitivity_label.grid(row = 0, column = 1)
        # self.atrial_sensitivity_entry.grid(row = 0, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.vddr_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, vddr_vals[7])
        self.ventricular_sensitivity_label.grid(row = 7, column = 1)
        self.ventricular_sensitivity_entry.grid(row = 8, column = 1)

        self.vrp_label = ttk.Label(self.vddr_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.vrp_entry.insert(0, vddr_vals[8])
        self.vrp_label.grid(row = 9, column = 0)
        self.vrp_entry.grid(row = 10, column = 0)

        # self.arp_label = ttk.Label(self.vddr_window, text="ARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.arp_entry = Entry(self.vddr_window, font=("Arial", 16))
        # self.arp_entry.insert(0, vddr_vals[13])
        # self.arp_label.grid(row = 0, column = 1)
        # self.arp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_label = ttk.Label(self.vddr_window, text="PVARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_entry = Entry(self.vddr_window, font=("Arial", 16))
        # self.pvarp_entry.insert(0, vddr_vals[14])
        # self.pvarp_label.grid(row = 0, column = 1)
        # self.pvarp_entry.grid(row = 0, column = 1)

        self.pvarp_extension_label = ttk.Label(self.vddr_window, text="PVARP Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_extension_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.pvarp_extension_entry.insert(0, vddr_vals[9])
        self.pvarp_extension_label.grid(row = 9, column = 1)
        self.pvarp_extension_entry.grid(row = 10, column = 1)

        # self.hysteresis_label = ttk.Label(self.vddr_window, text="Hysteresis Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.hysteresis_entry = Entry(self.vddr_window, font=("Arial", 16))
        # self.hysteresis_entry.insert(0, vddr_vals[16])
        # self.hysteresis_label.grid(row = 0, column = 1)
        # self.hysteresis_entry.grid(row = 0, column = 1)

        self.rate_smoothing_label = ttk.Label(self.vddr_window, text="Rate Smoothing:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smoothing_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, vddr_vals[10])
        self.rate_smoothing_label.grid(row = 11, column = 0)
        self.rate_smoothing_entry.grid(row = 12, column = 0)

        self.atr_duration_label = ttk.Label(self.vddr_window, text="ATR Duration:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_duration_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.atr_duration_entry.insert(0, vddr_vals[11])
        self.atr_duration_label.grid(row = 11, column = 1)
        self.atr_duration_entry.grid(row = 12, column = 1)

        self.atr_fallback_mode_label = ttk.Label(self.vddr_window, text="ATR Fallback Mode:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_mode_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.atr_fallback_mode_entry.insert(0, vddr_vals[12])
        self.atr_fallback_mode_label.grid(row = 13, column = 0)
        self.atr_fallback_mode_entry.grid(row = 14, column = 0)

        self.atr_fallback_time_label = ttk.Label(self.vddr_window, text="ATR Fallback Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_time_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.atr_fallback_time_entry.insert(0, vddr_vals[13])
        self.atr_fallback_time_label.grid(row = 13, column = 1)
        self.atr_fallback_time_entry.grid(row = 14, column = 1)

        self.activity_threshold_label = ttk.Label(self.vddr_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, vddr_vals[14])
        self.activity_threshold_label.grid(row = 15, column = 0)
        self.activity_threshold_entry.grid(row = 16, column = 0)

        self.reaction_time_label = ttk.Label(self.vddr_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, vddr_vals[15])
        self.reaction_time_label.grid(row = 15, column = 1)
        self.reaction_time_entry.grid(row = 16, column = 1)

        self.response_factor_label = ttk.Label(self.vddr_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, vddr_vals[16])
        self.response_factor_label.grid(row = 17, column = 0)
        self.response_factor_entry.grid(row = 18, column = 0)

        self.recovery_time_label = ttk.Label(self.vddr_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, vddr_vals[17])
        self.recovery__time_label.grid(row = 17, column = 1)
        self.recovery__time_entry.grid(row = 18, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.vddr_window, text="Save", style='TButton', command=self.update_vddr)
        self.save_button.grid(row = 19, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.vddr_window, text="Back to Pacing Modes", command=self.vddr_window.destroy)
        self.back_button.grid(row = 19, column = 1)

class DOOR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayDOOR()

    def update_door(self):
        global door_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global door_vals
                door_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.fixed_av_delay_entry.get(),
                             self.atrial_amplitude_entry.get(),
                             self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.acticity_threshold_entry.get(),
                             self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.door_window.destroy()

    def displayDOOR(self):
        self.door_window = Tk()
        self.door_window.geometry('%dx%d+0+0' % (width, height))
        self.door_window.title("DOOR Mode")
        self.door_window.configure(background="black")

        # Add a title
        self.door_label = ttk.Label(self.door_window, text="DOOR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.door_label.grid(row = 0, column = 0, columnspan = 13, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.door_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.door_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, door_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.door_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.door_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, door_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.door_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.door_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, door_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.door_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.door_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, door_vals[3])
        self.fixed_av_delay.grid(row = 3, column = 1)
        self.fixed_av_delay.grid(row = 4, column = 1)

        # self.dynamic_av_delay_label = ttk.Label(self.door_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.door_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, door_vals[4])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        #
        # self.sensed_av_delay_offset_label = ttk.Label(self.door_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.door_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, door_vals[5])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.door_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.door_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, door_vals[4])
        self.atrial_amplitude_label.grid(row = 5, column = 0)
        self.atrial_amplitude_entry.grid(row = 6, column = 0)

        self.ventricular_amplitude_label = ttk.Label(self.door_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.door_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, door_vals[5])
        self.ventricular_amplitude_label.grid(row = 5, column = 1)
        self.ventricular_amplitude_entry.grid(row = 6, column = 1)

        self.atrial_pulse_width_label = ttk.Label(self.door_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.door_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, door_vals[6])
        self.atrial_pulse_width_label.grid(row = 7, column = 0)
        self.atrial_pulse_width_entry.grid(row = 8, column = 0)
        self.ventricular_pulse_width_label = ttk.Label(self.door_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.door_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, door_vals[7])
        self.ventricular_pulse_width_label.grid(row = 7, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 8, column = 1)

        # self.atrial_sensitivity_label = ttk.Label(self.door_window, text="Atrial Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atrial_sensitivity_entry = Entry(self.door_window, font=("Arial", 16))
        # self.atrial_sensitivity_entry.insert(0, aat_vals[10])
        # self.atrial_sensitivity_label.grid(row = 0, column = 1)
        # self.atrial_sensitivity_entry.grid(row = 0, column = 1)
        #
        # self.ventricular_sensitivity_label = ttk.Label(self.door_window, text="Ventricular Sensitivity:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.ventricular_sensitivity_entry = Entry(self.door_window, font=("Arial", 16))
        # self.ventricular_sensitivity_entry.insert(0, door_vals[11])
        # self.ventricular_sensitivity_label.grid(row = 0, column = 1)
        # self.ventricular_sensitivity_entry.grid(row = 0, column = 1)
        #
        # self.vrp_label = ttk.Label(self.door_window, text="VRP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.vrp_entry = Entry(self.door_window, font=("Arial", 16))
        # self.vrp_entry.insert(0, door_vals[12])
        # self.vrp_label.grid(row = 0, column = 1)
        # self.vrp_entry.grid(row = 0, column = 1)
        #
        # self.arp_label = ttk.Label(self.door_window, text="ARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.arp_entry = Entry(self.door_window, font=("Arial", 16))
        # self.arp_entry.insert(0, door_vals[13])
        # self.arp_label.grid(row = 0, column = 1)
        # self.arp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_label = ttk.Label(self.door_window, text="PVARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_entry = Entry(self.door_window, font=("Arial", 16))
        # self.pvarp_entry.insert(0, door_vals[14])
        # self.pvarp_label.grid(row = 0, column = 1)
        # self.pvarp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_extension_label = ttk.Label(self.door_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.door_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, door_vals[15])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)
        #
        # self.hysteresis_label = ttk.Label(self.door_window, text="Hysteresis Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.hysteresis_entry = Entry(self.door_window, font=("Arial", 16))
        # self.hysteresis_entry.insert(0, door_vals[16])
        # self.hysteresis_label.grid(row = 0, column = 1)
        # self.hysteresis_entry.grid(row = 0, column = 1)
        #
        # self.rate_smoothing_label = ttk.Label(self.door_window, text="Rate Smoothing:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.rate_smoothing_entry = Entry(self.door_window, font=("Arial", 16))
        # self.rate_smoothing_entry.insert(0, door_vals[17])
        # self.rate_smoothing_label.grid(row = 0, column = 1)
        # self.rate_smoothing_entry.grid(row = 0, column = 1)
        #
        # self.atr_duration_label = ttk.Label(self.door_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.door_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, door_vals[18])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.door_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.door_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, door_vals[19])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.door_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.door_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, door_vals[20])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        self.activity_threshold_label = ttk.Label(self.door_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.door_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, door_vals[8])
        self.activity_threshold_label.grid(row = 9, column = 0)
        self.activity_threshold_entry.grid(row = 10, column = 0)

        self.reaction_time_label = ttk.Label(self.door_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.door_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, door_vals[9])
        self.reaction_time_label.grid(row = 9, column = 1)
        self.reaction_time_entry.grid(row = 10, column = 1)

        self.response_factor_label = ttk.Label(self.door_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.door_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, door_vals[10])
        self.response_factor_label.grid(row = 11, column = 0)
        self.response_factor_entry.grid(row = 12, column = 0)

        self.recovery_time_label = ttk.Label(self.door_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.door_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, door_vals[11])
        self.recovery__time_label.grid(row = 11, column = 1)
        self.recovery__time_entry.grid(row = 12, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.door_window, text="Save", style='TButton', command=self.update_door)
        self.save_button.grid(row = 13, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.door_window, text="Back to Pacing Modes", command=self.door_window.destroy)
        self.back_button.grid(row = 13, column = 1)


class DDIR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayddir()

    def update_ddir(self):
        global ddir_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global ddir_vals
                ddir_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.fixed_av_delay_entry.get(),self.atrial_amplitude_entry.get(),
                            self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.arp_entry.get(),
                            self.pvarp_entry.get(),self.acticity_threshold_entry.get(),
                            self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.ddir_window.destroy()

    def displayddir(self):
        self.ddir_window = Tk()
        self.ddir_window.geometry('%dx%d+0+0' % (width, height))
        self.ddir_window.title("DDIR Mode")
        self.ddir_window.configure(background="black")


    def DDIR_Mode(self):
        self.ddir_window = Tk()
        self.ddir_window.geometry('%dx%d+0+0' % (width, height))
        self.ddir_window.title("DDIR Mode")
        self.ddir_window.configure(background="black")

        # Add a title
        self.ddir_label = ttk.Label(self.ddir_window, text="DDIR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.ddir_label.grid(row = 0, column = 0, columnspan = 17, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.ddir_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, ddir_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.ddir_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, ddir_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.ddir_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, ddir_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.ddir_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, ddir_vals[3])
        self.fixed_av_delay.grid(row = 3, column = 1)
        self.fixed_av_delay.grid(row = 4, column = 1)

        # self.dynamic_av_delay_label = ttk.Label(self.ddir_window, text="Dynamic AV Delay:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.dynamic_av_delay_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.dynamic_av_delay_entry.insert(0, ddir_vals[4])
        # self.dynamic_av_delay.grid(row = 0, column = 1)
        # self.dynamic_av_delay.grid(row = 0, column = 1)

        # self.sensed_av_delay_offset_label = ttk.Label(self.ddir_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
        #                              font=("Arial", 16))
        # self.sensed_av_delay_offset_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.sensed_av_delay_offset_entry.insert(0, ddir_vals[5])
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)
        # self.sensed_av_delay_offset.grid(row = 0, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.ddir_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, ddir_vals[4])
        self.atrial_amplitude_label.grid(row = 5, column = 0)
        self.atrial_amplitude_entry.grid(row = 6, column = 0)

        self.ventricular_amplitude_label = ttk.Label(self.ddir_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, ddir_vals[5])
        self.ventricular_amplitude_label.grid(row = 5, column = 1)
        self.ventricular_amplitude_entry.grid(row = 6, column = 1)

        self.atrial_pulse_width_label = ttk.Label(self.ddir_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, ddir_vals[6])
        self.atrial_pulse_width_label.grid(row = 7, column = 0)
        self.atrial_pulse_width_entry.grid(row = 8, column = 0)
        self.ventricular_pulse_width_label = ttk.Label(self.ddir_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, ddir_vals[7])
        self.ventricular_pulse_width_label.grid(row = 7, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 8, column = 1)

        self.atrial_sensitivity_label = ttk.Label(self.ddir_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, ddir_vals[8])
        self.atrial_sensitivity_label.grid(row = 9, column = 0)
        self.atrial_sensitivity_entry.grid(row = 10, column = 0)

        self.ventricular_sensitivity_label = ttk.Label(self.ddir_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, ddir_vals[9])
        self.ventricular_sensitivity_label.grid(row = 9, column = 1)
        self.ventricular_sensitivity_entry.grid(row = 10, column = 1)

        self.vrp_label = ttk.Label(self.ddir_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.vrp_entry.insert(0, ddir_vals[10])
        self.vrp_label.grid(row = 11, column = 0)
        self.vrp_entry.grid(row = 12, column = 0)

        self.arp_label = ttk.Label(self.ddir_window, text="ARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.arp_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.arp_entry.insert(0, ddir_vals[11])
        self.arp_label.grid(row = 11, column = 1)
        self.arp_entry.grid(row = 12, column = 1)

        # self.pvarp_label = ttk.Label(self.ddir_window, text="PVARP:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.pvarp_entry.insert(0, ddir_vals[14])
        # self.pvarp_label.grid(row = 0, column = 1)
        # self.pvarp_entry.grid(row = 0, column = 1)
        #
        # self.pvarp_extension_label = ttk.Label(self.ddir_window, text="PVARP Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.pvarp_extension_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.pvarp_extension_entry.insert(0, ddir_vals[15])
        # self.pvarp_extension_label.grid(row = 0, column = 1)
        # self.pvarp_extension_entry.grid(row = 0, column = 1)
        #
        # self.hysteresis_label = ttk.Label(self.ddir_window, text="Hysteresis Extension:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.hysteresis_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.hysteresis_entry.insert(0, ddir_vals[15])
        # self.hysteresis_label.grid(row = 0, column = 1)
        # self.hysteresis_entry.grid(row = 0, column = 1)
        #
        # self.rate_smoothing_label = ttk.Label(self.ddir_window, text="Rate Smoothing:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.rate_smoothing_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.rate_smoothing_entry.insert(0, ddir_vals[16])
        # self.rate_smoothing_label.grid(row = 0, column = 1)
        # self.rate_smoothing_entry.grid(row = 0, column = 1)
        #
        # self.atr_duration_label = ttk.Label(self.ddir_window, text="ATR Duration:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_duration_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.atr_duration_entry.insert(0, ddir_vals[17])
        # self.atr_duration_label.grid(row = 0, column = 1)
        # self.atr_duration_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_mode_label = ttk.Label(self.ddir_window, text="ATR Fallback Mode:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_mode_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.atr_fallback_mode_entry.insert(0, ddir_vals[18])
        # self.atr_fallback_mode_label.grid(row = 0, column = 1)
        # self.atr_fallback_mode_entry.grid(row = 0, column = 1)
        #
        # self.atr_fallback_time_label = ttk.Label(self.ddir_window, text="ATR Fallback Time:", background="black",
        #                                      foreground="white", font=("Arial", 16))
        # self.atr_fallback_time_entry = Entry(self.ddir_window, font=("Arial", 16))
        # self.atr_fallback_time_entry.insert(0, ddir_vals[19])
        # self.atr_fallback_time_label.grid(row = 0, column = 1)
        # self.atr_fallback_time_entry.grid(row = 0, column = 1)

        self.activity_threshold_label = ttk.Label(self.ddir_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, ddir_vals[12])
        self.activity_threshold_label.grid(row = 13, column = 0)
        self.activity_threshold_entry.grid(row = 14, column = 0)

        self.reaction_time_label = ttk.Label(self.ddir_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, ddir_vals[13])
        self.reaction_time_label.grid(row = 13, column = 1)
        self.reaction_time_entry.grid(row = 14, column = 1)

        self.response_factor_label = ttk.Label(self.ddir_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, ddir_vals[14])
        self.response_factor_label.grid(row = 15, column = 0)
        self.response_factor_entry.grid(row = 16, column = 0)

        self.recovery_time_label = ttk.Label(self.ddir_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, ddir_vals[15])
        self.recovery__time_label.grid(row = 15, column = 1)
        self.recovery__time_entry.grid(row = 16, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.ddir_window, text="Save", style='TButton', command=self.update_ddir)
        self.save_button.grid(row = 17, column = 1)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.ddir_window, text="Back to Pacing Modes", command=self.ddir_window.destroy)
        self.back_button.grid(row = 17, column = 1)


class DDDR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayDDDR()

    def update_dddr(self):
        global dddr_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global dddr_vals
                dddr_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.fixed_av_delay_entry.get(),self.dynamic_av_delay_entry.get(),self.sensed_av_delay_offset_entry.get(),self.atrial_amplitude_entry.get(),
                            self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.arp_entry.get(),
                            self.pvarp_entry.get(),self.pvarp_extension_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get(),self.atr_duration_entry.get(),self.atr_fallback_mode_entry.get(),self.atr_fallback_time_entry.get(),self.acticity_threshold_entry.get(),
                            self.reaction_time_emrty.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.dddr_window.destroy()

    def displayDDDR(self):
        self.dddr_window = Tk()
        self.dddr_window.geometry('%dx%d+0+0' % (width, height))
        self.dddr_window.title("DDDR Mode")
        self.dddr_window.configure(background="black")

        # Add a title
        self.dddr_label = ttk.Label(self.dddr_window, text="DDDR Mode Information", background="black", foreground="white",
                              font=("Arial", 20))
        self.dddr_label.grid(row = 0, column = 0, columnspan = 27, pady = 10, padx = 10)

        # Add the parameter here
        self.lower_rate_label = ttk.Label(self.dddr_window, text="Lower Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.lower_rate_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.lower_rate_entry.insert(0, dddr_vals[0])
        self.lower_rate_label.grid(row = 1, column = 0)
        self.lower_rate_entry.grid(row = 2, column = 0)

        self.upper_rate_label = ttk.Label(self.dddr_window, text="Upper Rate Limit:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.upper_rate_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.upper_rate_entry.insert(0, dddr_vals[1])
        self.upper_rate_label.grid(row = 1, column = 1)
        self.upper_rate_entry.grid(row = 2, column = 1)

        self.maximum_sensor_rate_label = ttk.Label(self.dddr_window, text="Maximum Sensor Rate:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.maximum_sensor_rate_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.maximum_sensor_rate_entry.insert(0, dddr_vals[2])
        self.maximum_sensor_rate.grid(row = 3, column = 0)
        self.maximum_sensor_rate.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.dddr_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, dddr_vals[3])
        self.fixed_av_delay.grid(row = 3, column = 1)
        self.fixed_av_delay.grid(row = 4, column = 1)

        self.dynamic_av_delay_label = ttk.Label(self.dddr_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, dddr_vals[4])
        self.dynamic_av_delay.grid(row = 5, column = 0)
        self.dynamic_av_delay.grid(row = 6, column = 0)

        self.sensed_av_delay_offset_label = ttk.Label(self.dddr_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.sensed_av_delay_offset_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.sensed_av_delay_offset_entry.insert(0, dddr_vals[5])
        self.sensed_av_delay_offset.grid(row = 5, column = 1)
        self.sensed_av_delay_offset.grid(row = 6, column = 1)

        self.atrial_amplitude_label = ttk.Label(self.dddr_window, text="Atrial Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.atrial_amplitude_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.atrial_amplitude_entry.insert(0, dddr_vals[6])
        self.atrial_amplitude_label.grid(row = 7, column = 0)
        self.atrial_amplitude_entry.grid(row = 8, column = 0)

        self.ventricular_amplitude_label = ttk.Label(self.dddr_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, dddr_vals[7])
        self.ventricular_amplitude_label.grid(row = 7, column = 1)
        self.ventricular_amplitude_entry.grid(row = 8, column = 1)

        self.atrial_pulse_width_label = ttk.Label(self.dddr_window, text="Atrial Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_pulse_width_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.atrial_pulse_width_entry.insert(0, dddr_vals[8])
        self.atrial_pulse_width_label.grid(row = 9, column = 0)
        self.atrial_pulse_width_entry.grid(row = 10, column = 0)
        self.ventricular_pulse_width_label = ttk.Label(self.dddr_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, dddr_vals[9])
        self.ventricular_pulse_width_label.grid(row = 9, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 10, column = 1)

        self.atrial_sensitivity_label = ttk.Label(self.dddr_window, text="Atrial Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atrial_sensitivity_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.atrial_sensitivity_entry.insert(0, dddr_vals[10])
        self.atrial_sensitivity_label.grid(row = 11, column = 0)
        self.atrial_sensitivity_entry.grid(row = 12, column = 0)

        self.ventricular_sensitivity_label = ttk.Label(self.dddr_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, dddr_vals[11])
        self.ventricular_sensitivity_label.grid(row = 11, column = 1)
        self.ventricular_sensitivity_entry.grid(row = 12, column = 1)

        self.vrp_label = ttk.Label(self.dddr_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.vrp_entry.insert(0, dddr_vals[12])
        self.vrp_label.grid(row = 13, column = 0)
        self.vrp_entry.grid(row = 14, column = 0)

        self.arp_label = ttk.Label(self.dddr_window, text="ARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.arp_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.arp_entry.insert(0, dddr_vals[13])
        self.arp_label.grid(row = 13, column = 1)
        self.arp_entry.grid(row = 14, column = 1)

        self.pvarp_label = ttk.Label(self.dddr_window, text="PVARP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.pvarp_entry.insert(0, dddr_vals[14])
        self.pvarp_label.grid(row = 15, column = 0)
        self.pvarp_entry.grid(row = 16, column = 0)

        self.pvarp_extension_label = ttk.Label(self.dddr_window, text="PVARP Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_extension_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.pvarp_extension_entry.insert(0, dddr_vals[15])
        self.pvarp_extension_label.grid(row = 15, column = 1)
        self.pvarp_extension_entry.grid(row = 16, column = 1)

        self.hysteresis_label = ttk.Label(self.dddr_window, text="Hysteresis Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.hysteresis_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.hysteresis_entry.insert(0, dddr_vals[16])
        self.hysteresis_label.grid(row = 17, column = 0)
        self.hysteresis_entry.grid(row = 18, column = 0)

        self.rate_smoothing_label = ttk.Label(self.dddr_window, text="Rate Smoothing:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smoothing_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, dddr_vals[17])
        self.rate_smoothing_label.grid(row = 17, column = 1)
        self.rate_smoothing_entry.grid(row = 18, column = 1)

        self.atr_duration_label = ttk.Label(self.dddr_window, text="ATR Duration:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_duration_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.atr_duration_entry.insert(0, dddr_vals[18])
        self.atr_duration_label.grid(row = 19, column = 0)
        self.atr_duration_entry.grid(row = 20, column = 0)

        self.atr_fallback_mode_label = ttk.Label(self.dddr_window, text="ATR Fallback Mode:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_mode_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.atr_fallback_mode_entry.insert(0, dddr_vals[19])
        self.atr_fallback_mode_label.grid(row = 19, column = 1)
        self.atr_fallback_mode_entry.grid(row = 20, column = 1)

        self.atr_fallback_time_label = ttk.Label(self.dddr_window, text="ATR Fallback Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_time_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.atr_fallback_time_entry.insert(0, dddr_vals[20])
        self.atr_fallback_time_label.grid(row = 21, column = 0)
        self.atr_fallback_time_entry.grid(row = 22, column = 0)

        self.activity_threshold_label = ttk.Label(self.dddr_window, text="Activity Threshold:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.activity_threshold_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.activity_threshold_entry.insert(0, dddr_vals[21])
        self.activity_threshold_label.grid(row = 21, column = 1)
        self.activity_threshold_entry.grid(row = 22, column = 1)

        self.reaction_time_label = ttk.Label(self.dddr_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, dddr_vals[22])
        self.reaction_time_label.grid(row = 23, column = 0)
        self.reaction_time_entry.grid(row = 24, column = 0)

        self.response_factor_label = ttk.Label(self.dddr_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, dddr_vals[23])
        self.response_factor_label.grid(row = 23, column = 1)
        self.response_factor_entry.grid(row = 24, column = 1)

        self.recovery_time_label = ttk.Label(self.dddr_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery__time_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.recovery__time_entry.insert(0, dddr_vals[24])
        self.recovery__time_label.grid(row = 25, column = 0)
        self.recovery__time_entry.grid(row = 26, column = 0)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.dddr_window, text="Save", style='TButton', command=self.update_dddr)
        self.save_button.grid(row = 27, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.dddr_window, text="Back to Pacing Modes", command=self.dddr_window.destroy)
        self.back_button.grid(row = 27, column = 1)

def show_egram_page():
    width, height = 800, 600

    egram_window = Tk()
    egram_window.attributes('-fullscreen', True)
    egram_window.title("AOO Mode")
    egram_window.configure(background="black")

    # Add a title
    egram_label = ttk.Label(egram_window, text="EGRAM", background="black", foreground="white",
                          font=("Arial", 80))
    egram_label.pack()

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                    focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'teal')])

    # Sample data for time and voltage
    time = np.linspace(0, 1, 1000)  # 1 second, 1000 points
    voltage = 0.5 * np.sin(2 * np.pi * 5 * time)  # Example sine wave

    # Create a figure and plot the E-gram graph
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time, voltage, label='E-gram Signal', color='blue')
    ax.set_title('Electrogram (E-gram) Signal')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (mV)')
    ax.legend()
    ax.grid(True)

    # Embed the matplotlib figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=egram_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Create a "back" button to return to "Pacing mode"
    back_button = ttk.Button(egram_window, text="Back to Pacing Modes", command=egram_window.destroy)
    back_button.pack(pady=20)

    # Display the Tkinter window
    egram_window.mainloop()






#Communicating with the Pace Maker
def Communicate(mode, LR=0, APW=0, VPW=0, VA=0, ARP=0, VRP=0, AA=0, RecovTime=0, RF=0, MSR=0, AVD=0, AT=0, ReactTime=0, ATSats=0, VS=0):
    if (port == 0):
        return "Pace Maker Not Connected"
    else:
        pace_maker = serial.Serial(port="COM" + str(port), baudrate=115200)

    pace_maker.open
    Header = '<2B4Hf2Hf4HfH2f'
    if (AA == 'OFF'):
        AA = 0
    if (VA == 'OFF'):
        VA = 0
    data = struct.pack(Header, 0x16, 0x55, mode, LR, APW, VPW, VA, ARP, VRP, AA, RecovTime, RF, MSR, AVD, AT, ReactTime, ATS,
                     VS)
    print(len(data))
    pace_maker.write(data)
    print(len(data))
    time.sleep(0.5)
    serialdata = pace_maker.read(58)
    pace_maker.close
    print(len(data))
    mode_pacemaker = struct.unpack('H', serialdata[16:18])
    LR_pacemaker = struct.unpack('H', serialdata[18:20])
    APW_pacemaker = struct.unpack('H', serialdata[20:22])
    VPW_pacemaker = struct.unpack('H', serialdata[22:24])
    VA_pacemaker = struct.unpack('f', serialdata[24:28])
    ARP_pacemaker = struct.unpack('H', serialdata[28:30])
    VRP_pacemaker = struct.unpack('H', serialdata[30:32])
    AA_pacemaker = struct.unpack('f', serialdata[32:36])
    RecovTime_pacemaker = struct.unpack('H', serialdata[36:38])
    RF_pacemaker = struct.unpack('H', serialdata[38:40])
    MSR_pacemaker = struct.unpack('H', serialdata[40:42])
    AVD_pacemaker = struct.unpack('H', serialdata[42:44])
    AT_pacemaker = struct.unpack('f', serialdata[44:48])
    ReactTime_pacemaker = struct.unpack('H', serialdata[48:50])
    ATS_pacemaker = struct.unpack('f', serialdata[50:54])
    VS_pacemaker = struct.unpack('f', serialdata[54:58])
    print(mode_pacemaker[0], LR_pacemaker[0], APW_pacemaker[0], VPW_pacemaker[0], VA_pacemaker[0], ARP_pacemaker[0], VRP_pacemaker[0], AA_pacemaker[0], RecovTime_pacemaker[0], RF_pacemaker[0], MSR_pacemaker[0],
          AVD_pacemaker[0], AT_pacemaker[0], ReactTime_pacemaker[0], ATS_pacemaker[0], VS_pacemaker[0])
    if (mode_pacemaker[0] == mode and LR_pacemaker[0] == LR and APW_pacemaker[0] == APW and VPW_pacemaker[0] == VPW and (VA_pacemaker[0] - VA < 0.01) and ARP_pacemaker[
        0] == ARP and VRP_pacemaker[0] == VRP
            and (AA_pacemaker[0] - AA < 0.01) and RecovTime_pacemaker[0] == RecovTime and RF_pacemaker[0] == RF and MSR_pacemaker[0] == MSR and AVD_pacemaker[
                0] == AVD and (AT_pacemaker[0] - AT < 0.01) and ReactTime_pacemaker[0] == ReactTime and (ATS_pacemaker[0] - ATS < 0.01) and (
                    VS_pacemaker[0] - VS < 0.01)):
        return "Parameters Stored Successfully"
    else:
        return "Some Parameters Were Not Stored Correctly. Please Try Again."






# Background Image
#bg = PhotoImage(file="Sad_Background.gif")
#label1 = Label(window, image=bg)
#label1.place(x=0, y=0)
#label1.lower()
#bg_order = 0

def set_background_image(window, image_path):
    image = Image.open(image_path)
    image = image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
    photo = ImageTk.PhotoImage(image)


    label = Label(window, image=photo)
    label.image = photo
    label.place(x=0, y=0, relwidth=1, relheight=1)


if __name__=='__main__':
    # Get Users List
    file = open("text.txt", "r")
    users = []
    all_vals = []
    for line in file.readlines():
        user,password,vals = line.strip("\n").split("|")
        users.append([user,password])
        all_vals.append(vals)
    #print(users)
    # Number of Users
    count = len(users)
    # Close File
    file.close()
# ------------------------------------------------------------------------------------------------------------
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
    root.resizable(True, True)

    App(master=root)

    root.mainloop()



    # # Initializing lists for each pacing mode type
    # # AOO - Lower Rate Limit, Upper Rate Limit, Atrial Amplitude, Atrial Pulse Width
    # aoo_vals = [30, 50, 0, 0.05]
    # # VOO - Lower Rate Limit, Upper Rate Limit, Atrial Amplitude, Atrial Pulse Width, ARP
    # voo_vals = [30, 50, 0, 0.05, 150]
    # # AAI - Lower Rate Limit, Upper Rate Limit, Atrial Amplitude, Atrial Pulse Width, Atrial Sensitivty, ARP, PVARP, Hysterisis, Rate Smoothing
    # aai_vals = [30, 50, 0, 0.05, 0.25, 150, 150, 0, 0]
    # # VVI - Lower Rate Limit, Upper Rate Limit, Ventricular Amplitude, Ventricular Pulse Width, Ventricular Sensitivity, VRP, Hysterisis, Rate Smoothing
    # vvi_vals = [30, 50, 0, 0.05, 0.35, 150, 0, 0]
