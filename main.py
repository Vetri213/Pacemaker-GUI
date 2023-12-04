import tkinter
import serial
import pygame
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
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
        print(username)
        try:
            # open the file anc check if the username has already been taken
            with open("text.txt", "r") as file:
                for user in users[0]:
                    print(user)
                    if username == user:
                        return True
        except Exception as e:
            print(f"Error checking username: {str(e)}")
        return False



    def register_submit(self):
        # print(len(users))

        if (len(users) < 3):
            # Getting Username and Password from the Textboxes
            username = self.user_text.get()
            password = self.password_text.get()
            if not username or not password:
                self.changing_label.configure(text="Username or password cannot be empty")
            if self.is_username_taken(username):
                self.changing_label.configure(text="Username is already taken")
            else:
                default_vals = "{30,50,0,1}{30,50,0,1}{30,50,0,1,0.25,150,150,0,0}{30,50,0,1,0.35,150,0,0}{30,50,0,1,0.25,150,150}{30,50,0,1,0.25,150}{30,50,70,0,0.0,1,0.25,150,0,0.0,10,1,1}{30,50,70,0,0,1,1}{30,50,70,0,0,1,1,0.25,0.25,150,150,150}{30,50,70,0,0,0,0,1,1,0.25,0.25,150,150,150,0,0,0,10,0,1}{30,50,50,0.0,1,0,10,1,2}{30,50,50,0,1,0.25,150,150,0,0,0,10,1,2}{30,50,50,0,1,0,10,1,2}{30,50,50,0,1,0.25,150,0,0,0,10,1,2}{30,50,50,70,0,0,1,0.25,150,0,0,10,0,1,0,10,1,2}{30,50,50,70,0,0,1,1,0,10,1,2}{30,50,50,70,0,0,1,1,0.25,0.25,150,150,150,0,10,1,2}{30,50,50,70,0,0,0,0,1,1,0.25,0.25,150,150,150,0,0,0,10,0,1,0,10,1,2}"
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
        # Check if there is a connection to the DCM and if so, which port
    def check_connection(self):
        global port
        try:
            ser = serial.Serial(port="COM3", baudrate=115200)
            port = 3 #4
            print(3333333333)
            ser.close()
        except:
            try:
                ser = serial.Serial(port="COM4", baudrate=115200)
                port = 4  # 4
                print(444444)
                ser.close()
            except:
                port = 0
        port_candidates = "COM3"

        #ser.open()  # Open the serial port
        # global port
        # for port_candidate in port_candidates:
        #     try:
        #         ser = serial.Serial(port=COM3, baudrate=115200)
        #         ser.open()  # Open the serial port
        #
        #         # Add additional checks if needed, e.g., sending a test command
        #         # If successful, set the port and break out of the loop
        #         port = port_candidate
        #         ser.close()  # Close the serial port
        #         break
        #     except:
        #         port = 0
        #
        # # Optionally, check if self.port is still 0 to determine if not connected
        # if port == 0:
        #     print("Not connected")
        # else:
        #     print(f"Connected to port {port}")

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
        aoo_vals_str,voo_vals_str,aai_vals_str,vvi_vals_str,aat_vals_str,vvt_vals_str,vdd_vals_str,doo_vals_str,ddi_vals_str,ddd_vals_str,aoor_vals_str,aair_vals_str,voor_vals_str,vvir_vals_str,vddr_vals_str,door_vals_str,ddir_vals_str,dddr_vals_str,temp = self.vals.split("}")
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
        ddir_vals_str = ddir_vals_str.strip("{")
        dddr_vals_str = dddr_vals_str.strip("{")
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
        ddir_vals = ddir_vals_str.split(",")
        dddr_vals = dddr_vals_str.split(",")
        #print(dddr_vals)
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
        self.egrambutton = ttk.Button(master=self, text="EGRAM", style='Pacing.TButton', command=self.egramPressed)
        self.egrambutton.grid(row=13,column = 1)
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
    def VVIRPressed(self):
        VVIR_Mode(master=self.master)
    def VDDRPressed(self):
        VDDR_Mode(master=self.master)
    def DOORPressed(self):
        DOOR_Mode(master=self.master)
    def DDIRPressed(self):
        DDIR_Mode(master=self.master)
    def DDDRPressed(self):
        DDDR_Mode(master=self.master)
    def egramPressed(self):
        egram(master = self.master,mode = 0)


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
                #Communicate(mode = 0 ,APW = self.atrial_pulse_width_entry.get(), VPW = 0, LR =self.lower_rate_entry.get() ,AA = self.atrial_amplitude_entry.get(), VA = 0, ARP =0, VRP=0,AVD=0, AS = 0, VS = 0, RecovTime=0, RF=0, UR= self.upper_rate_entry.get(),  AT=0, ReactTime=0)
                Communicate()
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

#

class AAI_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayAAI()

    def update_aai(self):
        global aai_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 and 50 <= int(self.upper_rate_entry.get()) <= 175 and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 and 0.0 <= float(self.atrial_sensitivity_entry.get()) <= 10 and 150<= int(self.arp_entry.get()) <= 500 \
                and 150<= int(self.pvarp_entry.get()) <= 500 and (int(self.hysteresis_entry.get() )== 0 or 30<= int(self.hysteresis_entry.get()) <= 175) and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aai_vals
                aai_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.arp_entry.get(),self.pvarp_label.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get()]


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
        self.rate_smoothing_entry = Entry(self.aai_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, aai_vals[8])
        self.rate_smooth_label.grid(row = 9, column = 0)
        self.rate_smoothing_entry.grid(row = 9, column = 1)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9:
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and (int(self.hysteresis_entry.get() )== 0 or 30<= int(self.hysteresis_entry.get()) <= 175) \
            and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vvi_vals
                vvi_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get()]


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
        self.rate_smoothing_entry = Entry(self.vvi_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, vvi_vals[7])
        self.rate_smooth_label.grid(row = 7, column = 1)
        self.rate_smoothing_entry.grid(row = 8, column = 1)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.atrial_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.arp_entry.get()) <= 500 \
            and 150<= int(self.pvarp_entry.get()) <= 500:
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
        self.save_button.grid(row = 9, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.aat_window, text="Back to Pacing Modes", command=self.aat_window.destroy)
        self.back_button.grid(row = 9, column = 1)

class VVT_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVVT()

    def update_vvt(self):
        global vvt_vals
        if  30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500:
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

    def update_vdd(self): #{30,50,70,0,0.0,0.05,0.25,150,0,0.0,10,1,1}
        global vdd_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and (int(self.dynamic_av_delay_entry.get()) == 0 or int(self.dynamic_av_delay_entry.get()== 1)) \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.25 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and 0<= int(self.pvarp_extension_entry.get()) <= 400 \
            and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25 \
            and 10 <= int(self.atr_duration_entry.get()) <= 2000 \
            and (int(self.atr_fallback_mode_entry.get()) == 0 or int(self.atr_fallback_mode_entry.get()== 1))\
            and 1<= int(self.atr_fallback_time_entry.get()) <= 5 :
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
        self.fixed_av_delay_entry.insert(0, vdd_vals[2])
        self.fixed_av_delay_label.grid(row = 3, column = 0)
        self.fixed_av_delay_entry.grid(row = 4, column = 0)

        self.dynamic_av_delay_label = ttk.Label(self.vdd_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, vdd_vals[3])
        self.dynamic_av_delay_label.grid(row = 3, column = 1)
        self.dynamic_av_delay_entry.grid(row = 4, column = 1)

        self.ventricular_amplitude_label = ttk.Label(self.vdd_window, text="Ventricular Amplitude:", background="black", foreground="white",
                                           font=("Arial", 16))
        self.ventricular_amplitude_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.ventricular_amplitude_entry.insert(0, vdd_vals[4])
        self.ventricular_amplitude_label.grid(row = 5, column = 0)
        self.ventricular_amplitude_entry.grid(row = 6, column = 0)

        self.ventricular_pulse_width_label = ttk.Label(self.vdd_window, text="Ventricular Pulse Width:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_pulse_width_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.ventricular_pulse_width_entry.insert(0, vdd_vals[5])
        self.ventricular_pulse_width_label.grid(row = 5, column = 1)
        self.ventricular_pulse_width_entry.grid(row = 6, column = 1)

        self.ventricular_sensitivity_label = ttk.Label(self.vdd_window, text="Ventricular Sensitivity:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.ventricular_sensitivity_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.ventricular_sensitivity_entry.insert(0, vdd_vals[6])
        self.ventricular_sensitivity_label.grid(row = 7, column = 0)
        self.ventricular_sensitivity_entry.grid(row = 8, column = 0)

        self.vrp_label = ttk.Label(self.vdd_window, text="VRP:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.vrp_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.vrp_entry.insert(0, vdd_vals[7])
        self.vrp_label.grid(row = 7, column = 1)
        self.vrp_entry.grid(row = 8, column = 1)

        self.pvarp_extension_label = ttk.Label(self.vdd_window, text="PVARP Extension:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.pvarp_extension_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.pvarp_extension_entry.insert(0, vdd_vals[8])
        self.pvarp_extension_label.grid(row = 9, column = 0)
        self.pvarp_extension_entry.grid(row = 10, column = 0)

        self.rate_smoothing_label = ttk.Label(self.vdd_window, text="Rate Smoothing:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.rate_smoothing_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.rate_smoothing_entry.insert(0, vdd_vals[9])
        self.rate_smoothing_label.grid(row = 9, column = 1)
        self.rate_smoothing_entry.grid(row = 10, column = 1)

        self.atr_duration_label = ttk.Label(self.vdd_window, text="ATR Duration:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_duration_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.atr_duration_entry.insert(0, vdd_vals[10])
        self.atr_duration_label.grid(row = 11, column = 0)
        self.atr_duration_entry.grid(row = 12, column = 0)

        self.atr_fallback_mode_label = ttk.Label(self.vdd_window, text="ATR Fallback Mode:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_mode_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.atr_fallback_mode_entry.insert(0, vdd_vals[11])
        self.atr_fallback_mode_label.grid(row = 11, column = 1)
        self.atr_fallback_mode_entry.grid(row = 12, column = 1)

        self.atr_fallback_time_label = ttk.Label(self.vdd_window, text="ATR Fallback Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.atr_fallback_time_entry = Entry(self.vdd_window, font=("Arial", 16))
        self.atr_fallback_time_entry.insert(0, vdd_vals[12])
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global doo_vals
                doo_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.fixed_av_delay_entry.get(),self.atrial_amplitude_entry.get(),self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get()]


        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            self.doo_window.destroy()

    def displayDOO(self):
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
        self.fixed_av_delay_label.grid(row = 3, column = 0)
        self.fixed_av_delay_entry.grid(row = 4, column = 0)

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
        # self.recovery_time_entry = Entry(self.doo_window, font=("Arial", 16))
        # self.recovery_time_entry.insert(0, doo_vals[24])
        # self.recovery_time_label.grid(row = 0, column = 1)
        # self.recovery_time_entry.grid(row = 0, column = 1)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.atrial_sensitivity_entry.get()) <= 10 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and 150<= int(self.arp_entry.get()) <= 500 \
            and 150<= int(self.pvarp_entry.get()) <= 500:
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
        self.fixed_av_delay_label.grid(row = 3, column = 0)
        self.fixed_av_delay_entry.grid(row = 4, column = 0)

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
        # self.recovery_time_entry = Entry(self.ddi_window, font=("Arial", 16))
        # self.recovery_time_entry.insert(0, ddi_vals[24])
        # self.recovery_time_label.grid(row = 0, column = 1)
        # self.recovery_time_entry.grid(row = 0, column = 1)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and (int(self.dynamic_av_delay_entry.get()) == 0 or int(self.dynamic_av_delay_entry.get()== 1)) \
            and (int(self.sensed_av_delay_offset_entry.get()) == 0 or -100 <=int(self.sensed_av_delay_offset_entry.get()) <= -10) \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.atrial_sensitivity_entry.get()) <= 10 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and 150<= int(self.arp_entry.get()) <= 500 \
            and 150<= int(self.pvarp_entry.get()) <= 500 \
            and 0<= int(self.pvarp_extension_entry.get()) <= 400 \
            and (int(self.hysteresis_entry.get() )== 0 or 30<= int(self.hysteresis_entry.get()) <= 175) \
            and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25 \
            and (int(self.atr_fallback_mode_entry.get()) == 0 or int(self.atr_fallback_mode_entry.get()== 1))\
            and 10 <= int(self.atr_duration_entry.get())<= 2000 \
            and 1<= int(self.atr_fallback_time_entry.get()) <= 5 :
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
        self.fixed_av_delay_label.grid(row = 3, column = 0)
        self.fixed_av_delay_entry.grid(row = 4, column = 0)

        self.dynamic_av_delay_label = ttk.Label(self.ddd_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, ddd_vals[3])
        self.dynamic_av_delay_label.grid(row = 3, column = 1)
        self.dynamic_av_delay_entry.grid(row = 4, column = 1)

        self.sensed_av_delay_offset_label = ttk.Label(self.ddd_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.sensed_av_delay_offset_entry = Entry(self.ddd_window, font=("Arial", 16))
        self.sensed_av_delay_offset_entry.insert(0, ddd_vals[4])
        self.sensed_av_delay_offset_label.grid(row = 5, column = 0)
        self.sensed_av_delay_offset_entry.grid(row = 6, column = 0)

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
        # self.recovery_time_entry = Entry(self.ddd_window, font=("Arial", 16))
        # self.recovery_time_entry.insert(0, ddd_vals[24])
        # self.recovery_time_label.grid(row = 0, column = 1)
        # self.recovery_time_entry.grid(row = 0, column = 1)
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
        global aoor_vals #{30,50,50,0.0,0.05,0,10,1,2}
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aoor_vals
                aoor_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entry.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),
                            self.activity_threshold_entry.get(), self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


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
        self.activity_threshold_entry.insert(0, aoor_vals[5])
        self.activity_threshold_label.grid(row = 7, column = 0)
        self.activity_threshold_entry.grid(row = 8, column = 0)

        self.reaction_time_label = ttk.Label(self.aoor_window, text="Reaction Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.reaction_time_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.reaction_time_entry.insert(0, aoor_vals[6])
        self.reaction_time_label.grid(row = 7, column = 1)
        self.reaction_time_entry.grid(row = 8, column = 1)

        self.response_factor_label = ttk.Label(self.aoor_window, text="Response Factor:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.response_factor_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.response_factor_entry.insert(0, aoor_vals[7])
        self.response_factor_label.grid(row = 9, column = 0)
        self.response_factor_entry.grid(row = 10, column = 0)

        self.recovery_time_label = ttk.Label(self.aoor_window, text="Recovery_ Time:", background="black",
                                             foreground="white", font=("Arial", 16))
        self.recovery_time_entry = Entry(self.aoor_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, aoor_vals[8])
        self.recovery_time_label.grid(row = 9, column = 1)
        self.recovery_time_entry.grid(row = 10, column = 1)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.atrial_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.arp_entry.get()) <= 500 \
            and 150<= int(self.pvarp_entry.get()) <= 500 \
            and (int(self.hysteresis_entry.get() )== 0 or 30<= int(self.hysteresis_entry.get()) <= 175) \
            and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global aair_vals
                aair_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.atrial_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.arp_entry.get(),self.pvarp_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get(),
                            self.activity_threshold_entry.get(),
                            self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]



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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


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
        self.recovery_time_entry = Entry(self.aair_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, aair_vals[13])
        self.recovery_time_label.grid(row = 13, column = 1)
        self.recovery_time_entry.grid(row = 14, column = 1)
        # Style of Buttons
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        self.style.map('TButton', background=[('active', 'teal')])

        # Create a "Save" button
        self.save_button = ttk.Button(master=self.aair_window, text="Save", style='TButton', command=self.update_aair)
        self.save_button.grid(row = 15, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.aair_window, text="Back to Pacing Modes", command=self.aair_window.destroy)
        self.back_button.grid(row = 15, column = 1)

class VOOR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayVOOR()

    def update_voor(self):
        global voor_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global voor_vals
                voor_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),
                            self.activity_threshold_entry.get(),
                            self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


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
        self.recovery_time_entry = Entry(self.voor_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, voor_vals[8])
        self.recovery_time_label.grid(row = 9, column = 0)
        self.recovery_time_entry.grid(row = 10, column = 0)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and (int(self.hysteresis_entry.get() )== 0 or 30<= int(self.hysteresis_entry.get()) <= 175) \
            and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vvir_vals
                vvir_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get(),
                            self.activity_threshold_entry.get(),
                            self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


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
        self.recovery_time_entry = Entry(self.vvir_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, vvir_vals[12])
        self.recovery_time_label.grid(row = 13, column = 0)
        self.recovery_time_entry.grid(row = 14, column = 0)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and (int(self.dynamic_av_delay_entry.get()) == 0 or int(self.dynamic_av_delay_entry.get()== 1)) \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and 0<= int(self.pvarp_extension_entry.get()) <= 400 \
            and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25 \
            and (int(self.atr_fallback_mode_entry.get()) == 0 or int(self.atr_fallback_mode_entry.get()== 1))\
            and 10 <= int(self.atr_duration_entry.get())<= 2000 \
            and 1<= int(self.atr_fallback_time_entry.get()) <= 5 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global vddr_vals
                vddr_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.fixed_av_delay_entry.get(),self.dynamic_av_delay_entry.get(),
                            self.ventricular_amplitude_entry.get(),self.ventricular_pulse_width_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),
                            self.pvarp_extension_entry.get(),self.rate_smoothing_entry.get(),self.atr_duration_entry.get(),self.atr_fallback_mode_entry.get(),self.atr_fallback_time_entry.get(),self.activity_threshold_entry.get(),
                            self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


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
        self.vddr_label.grid(row = 0, column = 0, columnspan = 19, pady = 10, padx = 10)

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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.vddr_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, vddr_vals[3])
        self.fixed_av_delay_label.grid(row = 3, column = 1)
        self.fixed_av_delay_entry.grid(row = 4, column = 1)

        self.dynamic_av_delay_label = ttk.Label(self.vddr_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, vddr_vals[4])
        self.dynamic_av_delay_label.grid(row = 5, column = 0)
        self.dynamic_av_delay_entry.grid(row = 6, column = 0)

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
        self.recovery_time_entry = Entry(self.vddr_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, vddr_vals[17])
        self.recovery_time_label.grid(row = 17, column = 1)
        self.recovery_time_entry.grid(row = 18, column = 1)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global door_vals
                door_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entr.get(),self.fixed_av_delay_entry.get(),
                             self.atrial_amplitude_entry.get(),
                             self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.activity_threshold_entry.get(),
                             self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.door_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.door_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, door_vals[3])
        self.fixed_av_delay_label.grid(row = 3, column = 1)
        self.fixed_av_delay_entry.grid(row = 4, column = 1)

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
        self.recovery_time_entry = Entry(self.door_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, door_vals[11])
        self.recovery_time_label.grid(row = 11, column = 1)
        self.recovery_time_entry.grid(row = 12, column = 1)
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
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.atrial_sensitivity_entry.get()) <= 10 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and 150<= int(self.arp_entry.get()) <= 500 \
            and 150<= int(self.pvarp_entry.get()) <= 500 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global ddir_vals
                ddir_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entry.get(),self.fixed_av_delay_entry.get(),self.atrial_amplitude_entry.get(),
                            self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.arp_entry.get(),
                            self.pvarp_entry.get(),self.activity_threshold_entry.get(),
                            self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.ddir_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, ddir_vals[3])
        self.fixed_av_delay_label.grid(row = 3, column = 1)
        self.fixed_av_delay_entry.grid(row = 4, column = 1)

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
        self.recovery_time_entry = Entry(self.ddir_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, ddir_vals[15])
        self.recovery_time_label.grid(row = 15, column = 1)
        self.recovery_time_entry.grid(row = 16, column = 1)
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
        self.save_button.grid(row = 17, column = 0)

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.ddir_window, text="Back to Pacing Modes", command=self.ddir_window.destroy)
        self.back_button.grid(row = 17, column = 1)


class DDDR_Mode(tkinter.Frame):
    def __init__(self,master=None):
        self.displayDDDR()

    def update_dddr(self):
        global dddr_vals
        if 30 <= int(self.lower_rate_entry.get()) <= 175 \
            and 50 <= int(self.upper_rate_entry.get()) <= 175 \
            and 50 <= int(self.maximum_sensor_rate_entry.get()) <= 175 \
            and 70 <= int(self.fixed_av_delay_entry.get()) <= 300 \
            and (int(self.dynamic_av_delay_entry.get()) == 0 or int(self.dynamic_av_delay_entry.get()== 1)) \
            and (int(self.sensed_av_delay_offset_entry.get()) == 0 or -100 <=int(self.sensed_av_delay_offset_entry.get()) <= -10) \
            and 0.0 <= float(self.atrial_amplitude_entry.get()) <= 7 \
            and 0.0 <= float(self.ventricular_amplitude_entry.get()) <= 7 \
            and 0.05 <= float(self.atrial_pulse_width_entry.get()) <= 1.9 \
            and 0.05 <= float(self.ventricular_pulse_width_entry.get()) <= 1.9 \
            and 0.0 <= float(self.atrial_sensitivity_entry.get()) <= 10 \
            and 0.0 <= float(self.ventricular_sensitivity_entry.get()) <= 10 \
            and 150<= int(self.vrp_entry.get()) <= 500 \
            and 150<= int(self.arp_entry.get()) <= 500 \
            and 150<= int(self.pvarp_entry.get()) <= 500 \
            and 0<= int(self.pvarp_extension_entry.get()) <= 400 \
            and (int(self.hysteresis_entry.get() )== 0 or 30<= int(self.hysteresis_entry.get()) <= 175) \
            and 0.0 <= float(self.rate_smoothing_entry.get()) <= 0.25 \
            and (int(self.atr_fallback_mode_entry.get()) == 0 or int(self.atr_fallback_mode_entry.get()== 1))\
            and 10 <= int(self.atr_duration_entry.get())<= 2000 \
            and 1<= int(self.atr_fallback_time_entry.get()) <= 5 \
            and 0 <= int(self.activity_threshold_entry.get()) <= 6 \
            and 10<= int(self.reaction_time_entry.get())<= 50 \
            and 1<= int(self.response_factor_entry.get()) <= 16\
            and 2 <=int(self.recovery_time_entry.get()) <= 16:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                global dddr_vals
                dddr_vals= [self.lower_rate_entry.get(),self.upper_rate_entry.get(),self.maximum_sensor_rate_entry.get(),self.fixed_av_delay_entry.get(),self.dynamic_av_delay_entry.get(),self.sensed_av_delay_offset_entry.get(),self.atrial_amplitude_entry.get(),
                            self.ventricular_amplitude_entry.get(),self.atrial_pulse_width_entry.get(),self.ventricular_pulse_width_entry.get(),self.atrial_sensitivity_entry.get(),self.ventricular_sensitivity_entry.get(),self.vrp_entry.get(),self.arp_entry.get(),
                            self.pvarp_entry.get(),self.pvarp_extension_entry.get(),self.hysteresis_entry.get(),self.rate_smoothing_entry.get(),self.atr_duration_entry.get(),self.atr_fallback_mode_entry.get(),self.atr_fallback_time_entry.get(),self.activity_threshold_entry.get(),
                            self.reaction_time_entry.get(),self.response_factor_entry.get(),self.recovery_time_entry.get()]


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
        self.maximum_sensor_rate_label.grid(row = 3, column = 0)
        self.maximum_sensor_rate_entry.grid(row = 4, column = 0)


        self.fixed_av_delay_label = ttk.Label(self.dddr_window, text="Fixed AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.fixed_av_delay_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.fixed_av_delay_entry.insert(0, dddr_vals[3])
        self.fixed_av_delay_label.grid(row = 3, column = 1)
        self.fixed_av_delay_entry.grid(row = 4, column = 1)

        self.dynamic_av_delay_label = ttk.Label(self.dddr_window, text="Dynamic AV Delay:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.dynamic_av_delay_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.dynamic_av_delay_entry.insert(0, dddr_vals[4])
        self.dynamic_av_delay_label.grid(row = 5, column = 0)
        self.dynamic_av_delay_entry.grid(row = 6, column = 0)

        self.sensed_av_delay_offset_label = ttk.Label(self.dddr_window, text="Sensed AV Delay Offset:", background="black", foreground="white",
                                     font=("Arial", 16))
        self.sensed_av_delay_offset_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.sensed_av_delay_offset_entry.insert(0, dddr_vals[5])
        self.sensed_av_delay_offset_label.grid(row = 5, column = 1)
        self.sensed_av_delay_offset_entry.grid(row = 6, column = 1)

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
        self.recovery_time_entry = Entry(self.dddr_window, font=("Arial", 16))
        self.recovery_time_entry.insert(0, dddr_vals[24])
        self.recovery_time_label.grid(row = 25, column = 0)
        self.recovery_time_entry.grid(row = 26, column = 0)
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


class egram(tkinter.Frame):
    def __init__(self, master=None, mode = 0):
        self.mode = mode
        self.AtrialData = np.array([])
        self.VentricleData = np.array([])
        self.TimeData = np.array([])
        self.cont = True
        self.vS = True
        self.aS = True
        self.avS = True
        self.egram_window = Tk()
        self.egram_window.geometry('%dx%d+0+0' % (width, height))
        self.egram_window.title("EGRAM")
        self.egram_window.configure(background="black")
        self.show_egram_page()

        self.egram_window.mainloop()


    def show_egram_page(self):



        #width, height = 800, 600
        # Add a title
        self.egram_label = ttk.Label(self.egram_window, text="EGRAM", background="black", foreground="white",
                              font=("Arial", 80))
        self.egram_label.pack()

        # Style of Buttons
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                        focusthickness=3,
                        focuscolor='none', font=('American typewriter', 20))
        # When Hovering
        style.map('TButton', background=[('active', 'teal')])

        # Create a "back" button to return to "Pacing mode"
        self.back_button = ttk.Button(master=self.egram_window, text="Back to Pacing Modes",
                                      command=self.egram_window.destroy)
        self.back_button.pack()



        # Sample data for time and voltage
        # time = np.linspace(0, 1, 1000)  # 1 second, 1000 points
        # voltage = 0.5 * np.sin(2 * np.pi * 5 * time)  # Example sine wave
    # ----------------------------------------------------------------------

        # the figure that will contain the plot
        self.fig = Figure(figsize=(7, 7), dpi=100)
        # adding the subplot
        #Top
        self.AtriumPlot = self.fig.add_subplot(311)
        #Middle
        self.VentriclePlot = self.fig.add_subplot(312)
        # Bottom
        self.AVPlot = self.fig.add_subplot(313)
        #Creating space between the plots
        self.fig.subplots_adjust(hspace=0.9)

        # plotting the graph

        #Atrium Plot
        self.AtriumPlot.set_title('Atrium Internal Electrogram', fontsize=12)
        self.AtriumPlot.set_xlabel("Time (sec)", fontsize=10)
        self.AtriumPlot.set_ylabel("Voltage (V)", fontsize=10)
        self.AtriumPlot.set_ylim(-6, 6)
        self.AtriumPlot.set_xlim(0, 16)
        self.linesA = self.AtriumPlot.plot([], [])[0]

        #Ventricle Plot
        self.VentriclePlot.set_title('Ventricle Internal Electrogram', fontsize=12)
        self.VentriclePlot.set_xlabel("Time (sec)", fontsize=10)
        self.VentriclePlot.set_ylabel("Voltage (V)", fontsize=10)
        self.VentriclePlot.set_ylim(-6, 6)
        self.VentriclePlot.set_xlim(0, 16)
        self.linesV = self.VentriclePlot.plot([], [])[0]

        #AV Plot
        self.AVPlot.set_title('Atrium/Ventricle Internal Electrogram', fontsize=12)
        self.AVPlot.set_xlabel("Time (sec)", fontsize=10)
        self.AVPlot.set_ylabel("Voltage (V)", fontsize=10)
        self.AVPlot.set_ylim(-6, 6)
        self.AVPlot.set_xlim(0, 16)
        self.linesAV = self.AtriumPlot.plot([], [])[0]

        # Tkinter canvas
        # Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig,master = self.egram_window)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.egram_window)
        self.toolbar.update()

        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()

        self.egram_window.update()
        self.abutton = tkinter.Button(self.egram_window, text="Atrial", font=('calbiri', 12), command=lambda: self.plot_a())
        self.abutton.place(x=100, y=280)

        self.egram_window.update()
        self.vbutton = tkinter.Button(self.egram_window, text="Ventricular", font=('calbiri', 12), command=lambda: self.plot_v())
        self.vbutton.place(x=self.abutton.winfo_x() + self.abutton.winfo_reqwidth() + 20, y=280)

        self.egram_window.update()
        self.avbutton = tkinter.Button(self.egram_window, text="Atrial/Ventricular", font=('calbiri', 12), command=lambda: self.plot_av())
        self.avbutton.place(x=self.abutton.winfo_x() + self.abutton.winfo_reqwidth() + 20, y=320)

        self.egram_window.update()
        self.stopbutton = tkinter.Button(self.egram_window, text="Start/Stop", font=('calbiri', 12), command=lambda: self.conti())
        self.stopbutton.place(x=self.vbutton.winfo_x() + self.vbutton.winfo_reqwidth(), y=320)
        self.egram_window.update()

        # Display the Tkinter window
        self.egram_window.update()
        # ser.reset_input_buffer()
        self.start = time.time()
        print("TIME SET")
        self.plot_vals()
    def plot_vals(self):
        if (self.cont):
            vals00 = self.pacemaker_write(mode=self.mode)
            print(vals00)
            try:
                a_val = float(vals00[0])
                v_val = float(vals00[1])
            except:
                print("Pacemaker not Connected")

            try:
                # pacemaker.reset_input_buffer()
                if (self.mode == 0):
                    a_val, v_val = self.pacemaker_write(mode = self.mode, LRL=aoo_vals[0], URL=aoo_vals[1], AA=aoo_vals[2], APW=aoo_vals[3])
                elif (self.mode == 1):
                    a_val, v_val = self.pacemaker_write(mode = self.mode, LRL=voo_vals[0], URL=voo_vals[1], VA=voo_vals[2], VPW=voo_vals[3])
                elif (self.mode == 2):
                    a_val, v_val = self.pacemaker_write(mode = self.mode, LRL=aai_vals[0], URL=aai_vals[1], AA=aai_vals[2], APW=aai_vals[3], AS=aai_vals[4], ARP=aai_vals[5], PVARP=aai_vals[6], H=aai_vals[7], RS=aai_vals[8])
                elif (self.mode == 3):
                    a_val, v_val = self.pacemaker_write(mode = self.mode, LRL=vvi_vals[0], URL=vvi_vals[1], VA=vvi_vals[2], VPW=vvi_vals[3], VS=vvi_vals[4], VRP=vvi_vals[5], PVARPext=vvi_vals[6], H=vvi_vals[7],RS=vvi_vals[8])
                elif (self.mode == 4):
                    a_val, v_val = self.pacemaker_write(mode = self.mode, LRL=aat_vals[0], URL=aat_vals[1], AA=aat_vals[2], APW=aat_vals[3], AS=aat_vals[4], ARP=aat_vals[5], PVARP=aat_vals[6])
                elif (self.mode == 5):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=vvt_vals[0], URL=vvt_vals[1], VA=vvt_vals[2], VPW=vvt_vals[3], VS=vvt_vals[4], VRP=vvt_vals[5])
                elif (self.mode == 6):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=vdd_vals[0], URL=vdd_vals[1], FAVD=vdd_vals[2],DAVD=vdd_vals[3], VA=vdd_vals[4],  VPW=vdd_vals[5], VS=vdd_vals[6], VRP=vdd_vals[7],PVARPext=vdd_vals[8], RS=vdd_vals[9], FBM=vdd_vals[10], ATRD=vdd_vals[11], ATRFB=vdd_vals[12])
                elif (self.mode == 7):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=doo_vals[0], URL=doo_vals[1], FAVD=doo_vals[2], AA=doo_vals[3],VA=doo_vals[4], APW=doo_vals[5], VPW=doo_vals[6])
                elif (self.mode == 8):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=ddi_vals[0], URL=ddi_vals[1], FAVD=ddi_vals[2], AA=ddi_vals[3],VA=ddi_vals[4], APW=ddi_vals[5], VPW=ddi_vals[6], AS=ddi_vals[7], VS=ddi_vals[8], VRP=ddi_vals[9], ARP=ddi_vals[10], PVARP=ddi_vals[11])
                elif (self.mode == 9):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=ddd_vals[0], URL=ddd_vals[1], FAVD=ddd_vals[2], DAVD=ddd_vals[3],SAVD=ddd_vals[4], AA=ddd_vals[5],VA=ddd_vals[5], APW=ddd_vals[6], VPW=ddd_vals[7], AS=ddd_vals[8], VS=ddd_vals[9], VRP=ddd_vals[10], ARP=ddd_vals[11], PVARP=ddd_vals[12], PVARPext=ddd_vals[13], H=ddd_vals[14], RS=ddd_vals[15], ATRFM=ddd_vals[16], ATRD=ddd_vals[17], ATRFB=ddd_vals[18])
                elif (self.mode == 10):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=aoor_vals[0], URL=aoor_vals[1], MSR=aoor_vals[2], AA=aoor_vals[3], APW=aoor_vals[4], ACTT=aoor_vals[5], RT=aoor_vals[6], RF=aoor_vals[7], RecT=aoor_vals[8])
                elif (self.mode == 11):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=aair_vals[0], URL=aair_vals[1], MSR=aair_vals[2], AA=aair_vals[3], APW=aair_vals[4], AS=aair_vals[5], ARP=aair_vals[6], PVARP=aair_vals[7], H=aair_vals[8], RS=aair_vals[9], ACTT=aair_vals[10], RT=aair_vals[11], RF=aair_vals[12], RecT=aair_vals[13])
                elif (self.mode == 12):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=voor_vals[0], URL=voor_vals[1], MSR=voor_vals[2], VA=voor_vals[3], VPW=voor_vals[4], ACTT=voor_vals[5], RT=voor_vals[6], RF=voor_vals[7], RecT=voor_vals[8])
                elif (self.mode == 13):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=vvir_vals[0], URL=vvir_vals[1], MSR=vvir_vals[2], VA=vvir_vals[3], VPW=vvir_vals[4],VS=vvir_vals[5], VRP=vvir_vals[6], H=vvir_vals[7], RS=vvir_vals[8], ACTT=vvir_vals[9], RT=vvir_vals[10], RF=vvir_vals[11], RecT=vvir_vals[12])
                elif (self.mode == 14):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=vddr_vals[0], URL=vddr_vals[1], MSR=vddr_vals[2], FAVD=vddr_vals[3], DAVD=vddr_vals[4], VA=vddr_vals[5], VPW=vddr_vals[6],VS=vddr_vals[7], VRP=vddr_vals[8], PVARPext=vddr_vals[9], RS=vddr_vals[10], FBM= vddr_vals[11],ATRD=vddr_vals[12], ATRFB=vddr_vals[13], ACTT=vddr_vals[14], RT=vddr_vals[15], RF=vddr_vals[16], RecT=vddr_vals[17])
                elif (self.mode == 15):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=door_vals[0], URL=door_vals[1], MSR=door_vals[2], FAVD=door_vals[3], AA=door_vals[4],VA=door_vals[5],APW=door_vals[6], VPW=door_vals[7],ACTT=door_vals[8], RT=door_vals[9], RF=door_vals[10], RecT=door_vals[11])
                elif (self.mode == 16):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=ddir_vals[0], URL=ddir_vals[1], MSR=ddir_vals[2], FAVD=ddir_vals[3], AA=ddir_vals[4],VA=ddir_vals[5],APW=ddir_vals[6], VPW=ddir_vals[7], AS=ddir_vals[8], VS=ddir_vals[9], VRP=ddir_vals[10], ARP=ddir_vals[11], PVARP=ddir_vals[12], ACTT=ddir_vals[13], RT=ddir_vals[14], RF=ddir_vals[15], RecT=ddir_vals[16])
                elif (self.mode == 17):
                    a_val, v_val = self.pacemaker_write(mode=self.mode, LRL=dddr_vals[0], URL=dddr_vals[1], MSR=dddr_vals[2], FAVD=dddr_vals[3], DAVD=dddr_vals[4], SAVD=dddr_vals[5], AA=dddr_vals[6],VA=dddr_vals[7],APW=dddr_vals[8], VPW=dddr_vals[9], AS=dddr_vals[10], VS=dddr_vals[11], VRP=dddr_vals[12], ARP=dddr_vals[13], PVARP=dddr_vals[14], PVARPext=dddr_vals[15], H=dddr_vals[16], RS=dddr_vals[17], FBM=dddr_vals[18], ATRD=dddr_vals[19], ATRFB=dddr_vals[20], ACTT=dddr_vals[21], RT=dddr_vals[22], RF=dddr_vals[23], RecT=dddr_vals[24])

            except:
                self.egram_window.destroy()
                messagebox.showinfo("Message", "Pacemaker not connected")
            a = -6.6 * (a_val - 0.5)
            v = -6.6 * (v_val - 0.5)
            if (len(self.AtrialData) < 300):
                self.AtrialData = np.append(self.AtrialData, a)
                self.VentricleData = np.append(self.VentricleData, v)
                self.TimeData = np.append(self.TimeData, time.time() - self.start)
            else:
                self.AtrialData[0:299] = self.AtrialData[1:300]
                self.VentricleData[0:299] = self.VentricleData[1:300]
                self.AtrialData[299] = a
                self.VentricleData[299] = v
                self.TimeData[0:299] = self.TimeData[1:300]
                self.TimeData[299] = time.time() - self.start
                self.AtriumPlot.set_xlim(self.TimeData[0], self.TimeData[299])
                self.VentriclePlot.set_xlim(self.TimeData[0], self.TimeData[299])
            self.linesA.set_xdata(self.TimeData)
            self.linesA.set_ydata(self.AtrialData)
            self.linesV.set_xdata(self.TimeData)
            self.linesV.set_ydata(self.VentricleData)
            self.canvas.draw()
            self.egram_window.after(5,self.plot_vals)

    def plot_a(self):
        self.aS = not self.aS
        self.AtriumPlot.set_visible(self.aS)

    def conti(self):
        self.cont = not self.cont
        if (self.cont):
            self.start = time.time() - self.TimeData[len(self.TimeData) - 1]

    def plot_v(self):
        self.vS = not self.vS
        self.VentriclePlot.set_visible(self.vS)

    def plot_av(self):
        self.avS = not self.avS
        self.AVPlot.set_visible(self.avS)


    def pacemaker_write(self, mode = 0 ,APW =0, VPW = 0, LRL = 0 ,AA = 0, VA = 0, ARP =0, VRP=0,AVD=0, AS = 0, VS = 0, RecovTime=0, RF=0, URL=0,  AT=0, ReactTime=0, MSR = 0):
        print("Port is:",port)
        if (port == 0):
            return (0,0) #"Pace Maker Not Connected"
        else:
            pace_maker = serial.Serial(port="COM" + str(port), baudrate=115200)
        #pace_maker.open()
        Header = '<2B4H2f3H2f3Hf2H'


        data = struct.pack(Header, 0x16, 0x55, int(mode), int(APW), int(VPW), int(LRL), float(AA), float(VA), int(ARP),
                           int(VRP), int(AVD), float(AS), float(VS), int(RecovTime), int(RF), int(MSR), float(AT),
                           int(ReactTime), int(URL))

        # print(len(data))
        pace_maker.write(data)

        print(len(data))

        try:
            serialdata = pace_maker.read(pace_maker.in_waiting)
            print(serialdata)
            pace_maker.close()
            unpacked_data = struct.unpack(Header, serialdata)
            print(unpacked_data)

            # ORDER IS CORRECT
            # THE FIRST TWO INPUTS ARE THE GRAPH DATA!!!!!!!!

            # print(len(data))
            graph1 = unpacked_data[0]  # struct.unpack('f', serialdata[0:4])#??
            graph2 = unpacked_data[1]  # struct.unpack('H', serialdata[0:2])#??

        except:
            graph1, graph2 = 0,0

        print("Graph1: ", graph1)
        print("Graph2: ", graph2)
        return(graph1,graph2)

    #-------------------------------------------------------------------------------------------








#Communicating with the Pace Maker
def Communicate(mode = 0 ,APW =0, VPW = 0, LRL = 0 ,AA = 0, VA = 0, ARP =0, VRP=0,AVD=0, AS = 0, VS = 0, RecovTime=0, RF=0, URL=0,  AT=0, ReactTime=0,MSR = 0):
    if (port == 0):
        return "Pace Maker Not Connected"
    else:
        pace_maker = serial.Serial(port="COM" + str(port), baudrate=115200)

    try:
        pace_maker.open()
    except:
        print("Already Open")
    Header = '<2B4H2f3H2f3Hf2H'
    #Header = '<2B4Hf2Hf4HfH3f'
    if (AA == 'OFF'):
        AA = 0
    if (VA == 'OFF'):
        VA = 0
    AA = float(AA)
    VA = float(VA)
    data = struct.pack(Header, 0x16, 0x55, int(mode),int(APW), int(VPW), int(LRL), float(AA), float(VA), int(ARP), int(VRP),int(AVD), float(AS), float(VS), int(RecovTime), int(RF), int(MSR),  float(AT), int(ReactTime),int(URL))
    #print(len(data))
    pace_maker.write(data)


    print(len(data))
    #time.sleep(0.5)
    print("1")

    serialdata = pace_maker.read(2)
    print("2")
    print(serialdata)
    #pace_maker.close()
    unpacked_data = struct.unpack(Header,serialdata)
    print(unpacked_data)


    #ORDER IS CORRECT
    #THE FIRST TWO INPUTS ARE THE GRAPH DATA!!!!!!!!


    #print(len(data))
    graph1 = unpacked_data[0]#struct.unpack('f', serialdata[0:4])#??
    graph2 = unpacked_data[1]#struct.unpack('H', serialdata[0:2])#??
    print("Graph1: ",graph1)
    print("Graph2: ",graph2)
    mode_pacemaker = struct.unpack('H', serialdata[2:4])
    APW_pacemaker = struct.unpack('H', serialdata[4:6])
    VPW_pacemaker = struct.unpack('H', serialdata[6:8])
    LR_pacemaker = struct.unpack('H', serialdata[8:10])
    AA_pacemaker = struct.unpack('f', serialdata[10:14])
    VA_pacemaker = struct.unpack('f', serialdata[14:18])
    ARP_pacemaker = struct.unpack('H', serialdata[18:20])
    VRP_pacemaker = struct.unpack('H', serialdata[20:22])
    AVD_pacemaker = struct.unpack('H', serialdata[22:24])
    AS_pacemaker = struct.unpack('f', serialdata[24:28])
    VS_pacemaker = struct.unpack('f', serialdata[28:32])
    RecovTime_pacemaker = struct.unpack('H', serialdata[32:34])
    RF_pacemaker = struct.unpack('H', serialdata[34:36])
    UR_pacemaker = struct.unpack('H', serialdata[36:38])
    AT_pacemaker = struct.unpack('f', serialdata[38:42])
    ReactTime_pacemaker = struct.unpack('H', serialdata[42:44])
    print(mode_pacemaker[0], APW_pacemaker[0], VPW_pacemaker[0], LR_pacemaker[0], AA_pacemaker[0], VA_pacemaker[0], ARP_pacemaker[0], VRP_pacemaker[0], AVD_pacemaker[0], AS_pacemaker[0], VS_pacemaker[0], RecovTime_pacemaker[0], RF_pacemaker[0], UR_pacemaker[0], AT_pacemaker[0], ReactTime_pacemaker[0])
    if (mode_pacemaker[0] == mode and LR_pacemaker[0] == LRL and APW_pacemaker[0] == APW and VPW_pacemaker[0] == VPW and (VA_pacemaker[0] - VA < 0.01) and ARP_pacemaker[
        0] == ARP and VRP_pacemaker[0] == VRP
            and (AA_pacemaker[0] - AA < 0.01) and RecovTime_pacemaker[0] == RecovTime and RF_pacemaker[0] == RF and UR_pacemaker[0] == URL and AVD_pacemaker[
                0] == AVD and (AT_pacemaker[0] - AT < 0.01) and ReactTime_pacemaker[0] == ReactTime and (VS_pacemaker[0] - VS < 0.01)):
        print("Parameters Stored Successfully")
    else:
        print("Some Parameters Were Not Stored Correctly. Please Try Again.")






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
    # aoo_vals = [30, 50, 0, 1]
    # # VOO - Lower Rate Limit, Upper Rate Limit, Atrial Amplitude, Atrial Pulse Width, ARP
    # voo_vals = [30, 50, 0, 1, 150]
    # # AAI - Lower Rate Limit, Upper Rate Limit, Atrial Amplitude, Atrial Pulse Width, Atrial Sensitivty, ARP, PVARP, Hysterisis, Rate Smoothing
    # aai_vals = [30, 50, 0, 1, 0.25, 150, 150, 0, 0]
    # # VVI - Lower Rate Limit, Upper Rate Limit, Ventricular Amplitude, Ventricular Pulse Width, Ventricular Sensitivity, VRP, Hysterisis, Rate Smoothing
    # vvi_vals = [30, 50, 0, 1, 0.35, 150, 0, 0]
