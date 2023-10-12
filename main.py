import tkinter

import pygame
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


def show_aoo_mode_page():
    aoo_window = Tk()
    aoo_window.geometry('%dx%d+0+0' % (width, height))
    aoo_window.title("AOO Mode")
    aoo_window.configure(background="black")

    # Add a title
    aoo_label = ttk.Label(aoo_window, text="AOO Mode Information", background="black", foreground="white", font=("Arial", 20))
    aoo_label.pack()

    # Add the parameter here
    lower_rate_label = ttk.Label(aoo_window, text="Lower Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    lower_rate_entry = Entry(aoo_window, font=("Arial", 16))
    lower_rate_label.pack(pady=10)
    lower_rate_entry.pack(pady=10)

    upper_rate_label = ttk.Label(aoo_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(aoo_window, font=("Arial", 16))
    upper_rate_label.pack(pady=10)
    upper_rate_entry.pack(pady=10)

    atrial_amplitude_label = ttk.Label(aoo_window, text="Atrial Amplitude:", background="black", foreground="white", font=("Arial", 16))
    atrial_amplitude_entry = Entry(aoo_window, font=("Arial", 16))
    atrial_amplitude_label.pack(pady=10)
    atrial_amplitude_entry.pack(pady=10)

    atrial_pulse_width_label = ttk.Label(aoo_window, text="Atrial Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    atrial_pulse_width_entry = Entry(aoo_window, font=("Arial", 16))
    atrial_pulse_width_label.pack(pady=10)
    atrial_pulse_width_entry.pack(pady=10)

#    ventricular_amplitude_label = ttk.Label(aoo_window, text="Ventricular Amplitude:", background="black", foreground="white", font=("Arial", 16))
#    ventricular_amplitude_entry = Entry(aoo_window, font=("Arial", 16))
#    ventricular_amplitude_label.pack(pady=10)
#    ventricular_amplitude_entry.pack(pady=10)

#    ventricular_pulse_width_label = ttk.Label(aoo_window, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
#    ventricular_pulse_width_entry = Entry(aoo_window, font=("Arial", 16))
#    ventricular_pulse_width_label.pack(pady=10)
#    ventricular_pulse_width_entry.pack(pady=10)

    #vrp_label = ttk.Label(aoo_window, text="VRP:", background="black", foreground="white", font=("Arial", 16))
    #vrp_entry = Entry(aoo_window, font=("Arial", 16))
    #vrp_label.pack(pady=10)
    #vrp_entry.pack(pady=10)

    #arp_label = ttk.Label(aoo_window, text="ARP:", background="black", foreground="white", font=("Arial", 16))
    #arp_entry = Entry(aoo_window, font=("Arial", 16))
    #arp_label.pack(pady=10)
    #arp_entry.pack(pady=10)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                    focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

    # Create a "Save" button
    save_button = ttk.Button(master=aoo_window, text="Save")
    save_button.pack(pady=10)

    # Create a "back" button to return to "Pacing mode"
    back_button = ttk.Button(master=aoo_window, text="Back to Pacing Modes", command=aoo_window.destroy)
    back_button.pack(pady=5)
def show_voo_mode_page():
    voo_window = Tk()
    voo_window.geometry('%dx%d+0+0' % (width, height))
    voo_window.title("VOO Mode")
    voo_window.configure(background="black")

    # Add a title
    voo_label = ttk.Label(voo_window, text="VOO Mode Information", background="black", foreground="white", font=("Arial", 20))
    voo_label.pack()

    # Add the parameter here
    lower_rate_label = ttk.Label(voo_window, text="Lower Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    lower_rate_entry = Entry(voo_window, font=("Arial", 16))
    lower_rate_label.pack(pady=10)
    lower_rate_entry.pack(pady=10)

    upper_rate_label = ttk.Label(voo_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(voo_window, font=("Arial", 16))
    upper_rate_label.pack(pady=10)
    upper_rate_entry.pack(pady=10)

    #atrial_amplitude_label = ttk.Label(voo_window, text="Atrial Amplitude:", background="black", foreground="white", font=("Arial", 16))
    #atrial_amplitude_entry = Entry(voo_window, font=("Arial", 16))
    #atrial_amplitude_label.pack(pady=10)
    #atrial_amplitude_entry.pack(pady=10)

    #atrial_pulse_width_label = ttk.Label(voo_window, text="Atrial Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    #atrial_pulse_width_entry = Entry(voo_window, font=("Arial", 16))
    #atrial_pulse_width_label.pack(pady=10)
    #atrial_pulse_width_entry.pack(pady=10)

    ventricular_amplitude_label = ttk.Label(voo_window, text="Ventricular Amplitude:", background="black", foreground="white", font=("Arial", 16))
    ventricular_amplitude_entry = Entry(voo_window, font=("Arial", 16))
    ventricular_amplitude_label.pack(pady=10)
    ventricular_amplitude_entry.pack(pady=10)

    ventricular_pulse_width_label = ttk.Label(voo_window, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    ventricular_pulse_width_entry = Entry(voo_window, font=("Arial", 16))
    ventricular_pulse_width_label.pack(pady=10)
    ventricular_pulse_width_entry.pack(pady=10)

    #vrp_label = ttk.Label(voo_window, text="VRP:", background="black", foreground="white", font=("Arial", 16))
    #vrp_entry = Entry(voo_window, font=("Arial", 16))
    #vrp_label.pack(pady=10)
    #vrp_entry.pack(pady=10)

    arp_label = ttk.Label(voo_window, text="ARP:", background="black", foreground="white", font=("Arial", 16))
    arp_entry = Entry(voo_window, font=("Arial", 16))
    arp_label.pack(pady=10)
    arp_entry.pack(pady=10)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                    focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

     # Create a "Save" button
    save_button = ttk.Button(voo_window, text="Save")
    save_button.pack(pady=10)

    # Create a "back" button to return to "Pacing mode"
    back_button = ttk.Button(voo_window, text="Back to Pacing Modes", command=voo_window.destroy)
    back_button.pack(pady=5)
def show_aai_mode_page():
    aai_window = Tk()
    aai_window.geometry('%dx%d+0+0' % (width, height))
    aai_window.title("AAI Mode")
    aai_window.configure(background="black")

    # Add label
    aai_label = ttk.Label(aai_window, text="AAI Mode Information", background="black", foreground="white",font=("Arial", 20))
    aai_label.grid(row=0, column=0, columnspan=2, pady=10, padx =10)

    # Add the parameter here
    lower_rate_label = ttk.Label(aai_window, text="Lower Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    lower_rate_label.grid(row=1, column=0, pady=10, padx =10)
    lower_rate_entry = Entry(aai_window, font=("Arial", 16))
    lower_rate_entry.grid(row=2, column=0, pady=10, padx =10)

    upper_rate_label = ttk.Label(aai_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(aai_window, font=("Arial", 16))
    upper_rate_label.grid(row=1, column=1, pady=10, padx =10)
    upper_rate_entry.grid(row=2, column=1, pady=10, padx =10)

    atrial_amplitude_label = ttk.Label(aai_window, text="Atrial Amplitude:", background="black", foreground="white", font=("Arial", 16))
    atrial_amplitude_entry = Entry(aai_window, font=("Arial", 16))
    atrial_amplitude_label.grid(row=3, column=0, pady=10, padx =10)
    atrial_amplitude_entry.grid(row=4, column=0, pady=10, padx =10)

    atrial_pulse_width_label = ttk.Label(aai_window, text="Atrial Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    atrial_pulse_width_entry = Entry(aai_window, font=("Arial", 16))
    atrial_pulse_width_label.grid(row=3, column=1, pady=10, padx =10)
    atrial_pulse_width_entry.grid(row=4, column=1, pady=10, padx =10)

    atrial_sensitivity_label = ttk.Label(aai_window, text="Atrial Sensitivity:", background="black", foreground="white", font=("Arial", 16))
    atrial_sensitivity_entry = Entry(aai_window, font=("Arial", 16))
    atrial_sensitivity_label.grid(row=5, column=0, pady=10, padx =10)
    atrial_sensitivity_entry.grid(row=6, column=0, pady=10, padx =10)

    #ventricular_amplitude_label = ttk.Label(aai_window, text="Ventricular Amplitude:", background="black", foreground="white", font=("Arial", 16))
    #ventricular_amplitude_entry = Entry(aai_window, font=("Arial", 16))
    #ventricular_amplitude_label.pack(pady=10)
    #ventricular_amplitude_entry.pack(pady=10)

    #ventricular_pulse_width_label = ttk.Label(aai_window, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    #ventricular_pulse_width_entry = Entry(aai_window, font=("Arial", 16))
    #ventricular_pulse_width_label.pack(pady=10)
    #ventricular_pulse_width_entry.pack(pady=10)

    #vrp_label = ttk.Label(aai_window, text="VRP:", background="black", foreground="white", font=("Arial", 16))
    #vrp_entry = Entry(aai_window, font=("Arial", 16))
    #vrp_label.pack(pady=10)
    #vrp_entry.pack(pady=10)

    arp_label = ttk.Label(aai_window, text="ARP:", background="black", foreground="white", font=("Arial", 16))
    arp_entry = Entry(aai_window, font=("Arial", 16))
    arp_label.grid(row=5, column=1, pady=10, padx =10)
    arp_entry.grid(row=6, column=1, pady=10, padx =10)

    pvarp_label = ttk.Label(aai_window, text="PVARP:", background="black", foreground="white", font=("Arial", 16))
    pvarp_entry = Entry(aai_window, font=("Arial", 16))
    pvarp_label.grid(row=7, column=0, pady=10, padx =10)
    pvarp_entry.grid(row=8, column=0, pady=10, padx =10)

    hysteresis_label = ttk.Label(aai_window, text="Hysteresis:", background="black", foreground="white", font=("Arial", 16))
    hysteresis_entry = Entry(aai_window, font=("Arial", 16))
    hysteresis_label.grid(row=7, column=1, pady=10, padx =10)
    hysteresis_entry.grid(row=8, column=1, pady=10, padx=10 )

    rate_smoothing_label = ttk.Label(aai_window, text="Rate Smoothing:", background="black", foreground="white", font=("Arial", 16))
    rate_smoothing_entry = Entry(aai_window, font=("Arial", 16))
    rate_smoothing_label.grid(row=9, column=0, pady=10)
    rate_smoothing_entry.grid(row=10, column=0, pady=10)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                    focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

     # Create a "Save" button
    save_button = ttk.Button(aai_window, text="Save")
    save_button.grid(row=12, column=0, pady=10)

    # Creat3 a "back" button to return to "Pacing mode"
    back_button = ttk.Button(aai_window, text="Back to Pacing Modes", command=aai_window.destroy)
    back_button.grid(row=12, column=1, pady=10)
def show_vvi_mode_page():
    vvi_window = Tk()
    vvi_window.geometry('%dx%d+0+0' % (width, height))
    vvi_window.title("VVI Mode")
    vvi_window.configure(background="black")

    # Add label
    vvi_label = ttk.Label(vvi_window, text="VVI Mode Information", background="black", foreground="white", font=("Arial", 20))
    vvi_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Add the parameter here
    lower_rate_label = ttk.Label(vvi_window, text="Lower Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    lower_rate_entry = Entry(vvi_window, font=("Arial", 16))
    lower_rate_label.grid(row=1, column=0, pady=10, padx =10)
    lower_rate_entry.grid(row=2, column=0, pady=10, padx =10)

    upper_rate_label = ttk.Label(vvi_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(vvi_window, font=("Arial", 16))
    upper_rate_label.grid(row=1, column=1, pady=10, padx =10)
    upper_rate_entry.grid(row=2, column=1, pady=10, padx =10)

    #atrial_amplitude_label = ttk.Label(vvi_window, text="Atrial Amplitude:", background="black", foreground="white", font=("Arial", 16))
    #atrial_amplitude_entry = Entry(vvi_window, font=("Arial", 16))
    #atrial_amplitude_label.pack(pady=10)
    #atrial_amplitude_entry.pack(pady=10)

    #atrial_pulse_width_label = ttk.Label(vvi_window, text="Atrial Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    #atrial_pulse_width_entry = Entry(vvi_window, font=("Arial", 16))
    #atrial_pulse_width_label.pack(pady=10)
    #atrial_pulse_width_entry.pack(pady=10)

    ventricular_amplitude_label = ttk.Label(vvi_window, text="Ventricular Amplitude:", background="black", foreground="white", font=("Arial", 16))
    ventricular_amplitude_entry = Entry(vvi_window, font=("Arial", 16))
    ventricular_amplitude_label.grid(row=3, column=0, pady=10, padx =10)
    ventricular_amplitude_entry.grid(row=4, column=0, pady=10, padx =10)

    ventricular_pulse_width_label = ttk.Label(vvi_window, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    ventricular_pulse_width_entry = Entry(vvi_window, font=("Arial", 16))
    ventricular_pulse_width_label.grid(row=3, column=1, pady=10, padx =10)
    ventricular_pulse_width_entry.grid(row=4, column=1, pady=10, padx =10)


    ventricular_sensitivity_label = ttk.Label(vvi_window, text="Ventricular Sensitivity:", background="black", foreground="white", font=("Arial", 16))
    ventricular_sensitivity_entry = Entry(vvi_window, font=("Arial", 16))
    ventricular_sensitivity_label.grid(row=5, column=0, pady=10, padx =10)
    ventricular_sensitivity_entry.grid(row=6, column=0, pady=10, padx =10)

    vrp_label = ttk.Label(vvi_window, text="VRP:", background="black", foreground="white", font=("Arial", 16))
    vrp_entry = Entry(vvi_window, font=("Arial", 16))
    vrp_label.grid(row=5, column=1, pady=10, padx =10)
    vrp_entry.grid(row=6, column=1, pady=10, padx =10)

    hysteresis_label = ttk.Label(vvi_window, text="Hysteresis:", background="black", foreground="white", font=("Arial", 16))
    hysteresis_entry = Entry(vvi_window, font=("Arial", 16))
    hysteresis_label.grid(row=7, column=0, pady=10, padx =10)
    hysteresis_entry.grid(row=8, column=0, pady=10, padx =10)

    rate_smoothing_label = ttk.Label(vvi_window, text="Rate Smoothing:", background="black", foreground="white", font=("Arial", 16))
    rate_smoothing_entry = Entry(vvi_window, font=("Arial", 16))
    rate_smoothing_label.grid(row=7, column=1, pady=10, padx =10)
    rate_smoothing_entry.grid(row=8, column=1, pady=10, padx =10)

    #arp_label = ttk.Label(vvi_window, text="ARP:", background="black", foreground="white", font=("Arial", 16))
    #arp_entry = Entry(vvi_window, font=("Arial", 16))
    #arp_label.pack(pady=10)
    #arp_entry.pack(pady=10)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                    focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

    # Create a "Save" button
    save_button = ttk.Button(vvi_window, text="Save")
    save_button.grid(row=12, column=0, pady=10, padx =10)

    # Creat a "back" button to return to "Pacing mode"
    back_button = ttk.Button(vvi_window, text="Back to Pacing Modes", command=vvi_window.destroy)
    back_button.grid(row=12, column=1, pady=10, padx =10)

def pacing_modes():
    pacing_modes = Tk()
    pacing_modes.master = root
    pacing_modes.title("Pacemaker GUI")
    # Changing background colour
    pacing_modes.configure(background="black")

    # Changing window size
    width, height = pacing_modes.winfo_screenwidth(), pacing_modes.winfo_screenheight()
    pacing_modes.geometry('%dx%d+0+0' % (width, height))

    # Heading
    label = ttk.Label(master=pacing_modes, text="Pacing Modes", background=bg, foreground=fg, font=("Arial", 80))
    label.pack(pady=30)

    # Create a frame to contain the buttons
    #button_frame = ttk.Frame(pacing_modes, padding=300)
    #button_frame.pack(fill="both", expand=True)


    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=10, height =30, borderwidth=1, focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

    # Create buttons and add them to the frame

    button1 = ttk.Button(master = pacing_modes, text="AOO", style='Pacing.TButton',command=show_aoo_mode_page)
    button1.pack(pady=20)

    button2 = ttk.Button(master = pacing_modes, text="VOO", style='Pacing.TButton',command=show_voo_mode_page)
    button2.pack(pady=20)
    button3 = ttk.Button(master = pacing_modes, text="AAI", style='Pacing.TButton',command=show_aai_mode_page)
    button3.pack(pady=20)
    button4 = ttk.Button(master = pacing_modes, text="VVI", style='Pacing.TButton',command=show_vvi_mode_page)
    button4.pack(pady=20)

    # Exit Button33
    exit_button = ttk.Button(master=pacing_modes, text="Exit", command=quit)
    exit_button.pack(pady=100)

    # Use the grid layout manager to arrange the buttons in columns
    #button1.grid(row=0, column=0, padx=30, pady=30)
    #button2.grid(row=0, column=1, padx=30, pady=30)
    #button3.grid(row=1, column=0, padx=30, pady=30)
    #button4.grid(row=1, column=1, padx=30, pady=30)


#Login Function
def login_func():
    def login_submit():
        # Getting Username and Password from the Textboxes
        username = user_text.get(1.0, "end-1c")
        password = password_text.get(1.0, "end-1c")
        login_info = [username,password]
        if(login_info in users):
            #Go to the ACTUAL DO STUFF PAGE
            changing_label.configure(text="Information Recognized!")
            login.destroy()
            pacing_modes()
        else:
            changing_label.configure(text="No User Matches Your Input. Please Try Again.")
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
    label = ttk.Label(master=login, text="LOGIN", background=bg, foreground=fg, font=("Arial", 80))
    label.pack()

    # Changing Label
    changing_label = ttk.Label(master=login, text="Please Enter Your Information Below:", background=bg, foreground=fg, font=("Arial", 20))
    changing_label.pack(pady=10)

    # Username
    user_label = ttk.Label(master=login, text="Username:", background=bg, foreground=fg, font=("Arial", 20))
    user_label.pack(pady=20)
    user_text = Text(master=login, height=1, width=50, font=("Arial", 20))
    user_text.pack()

    # Password
    password_label = ttk.Label(master=login, text="Password:", background=bg, foreground=fg, font=("Arial", 20))
    password_label.pack(pady=20)
    password_text = Text(master=login, height=1, width=50, font=("Arial", 20))
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
    submit_button.pack(pady=20)

    # Exit Button
    exit_button = ttk.Button(master=login, text="Exit", command=quit)
    exit_button.pack()

#Register Function
def register_func():
    def is_username_taken(username):
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
    def register_submit():
        print(len(users))

        if (len(users) <10):
            #Getting Username and Password from the Textboxes
            username = user_text.get(1.0, "end-1c")
            password = password_text.get(1.0, "end-1c")
            if not username or not password:
                changing_label.configure(text="Username or password cannot be empty")
            elif is_username_taken(username):
                changing_label.configure(text="Username is already taken")
            else:
            #Creating a New Entry to be added to the file of Users (in the same format)
                new_entry = "\n"+username+","+password
            #Opening File in Append Mode (So as not to delete other users)
                file = open("text.txt", "a")
            #Adding Entry
                file.write(new_entry)
            #Closing file
                file.close()
            # Go to the ACTUAL DO STUFF PAGE
                changing_label.configure(text="Information Recognized!")
                register.destroy()
                pacing_modes()
        else:
            changing_label.configure(text="Max Users Registered. Sorry!")

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

    # Changing Label
    changing_label = ttk.Label(master=register, text="Please Enter Your Information Below:", background=bg, foreground=fg,
                               font=("Arial", 20))
    changing_label.pack(pady=10)

    # Username
    user_label = ttk.Label(master=register, text="Username:", background=bg, foreground=fg, font=("Arial", 20))
    user_label.pack(pady=20)
    user_text = Text(master=register, height=1, width=50, font=("Arial", 20))
    user_text.pack()

    # Password
    password_label = ttk.Label(master=register, text="Password:", background=bg, foreground=fg, font=("Arial", 20))
    password_label.pack(pady=20)
    password_text = Text(master=register, height=1, width=50, font=("Arial", 20))
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
    submit_button.pack(pady=20)

    #Home Button
    exit_button = ttk.Button(master=register, text="Exit", command=quit)
    exit_button.pack()








# Background Image
#bg = PhotoImage(file="Sad_Background.gif")
#label1 = Label(window, image=bg)
#label1.place(x=0, y=0)
#label1.lower()
#bg_order = 0

def set_background_image(window, image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    label = Label(window, image=photo)
    label.image = photo
    label.place(x=0, y=0, relwidth=1, relheight=1)


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

    background_image_path = "heart.png"
    set_background_image(root, background_image_path)

    # Changing window size
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))

    # Widget Options
    bg = "black"
    fg = "white"

    # Heading
    label = ttk.Label(master=root, text="WELCOME", background=bg, foreground=fg, font=("Arial", 80))
    label.pack(pady=50)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background=bg, foreground=fg, width=50, height =30, borderwidth=1, focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'red')])

    # Login
    login_button = ttk.Button(root, text="Login", command=login_func)
    login_button.pack(pady=20)
    # Register
    register_button = ttk.Button(master=root, text="Register", command=register_func)
    register_button.pack(pady=20)
    # Quit
    quit_button = ttk.Button(root, text='Quit', command=quit)
    quit_button.pack(pady=20)

    root.resizable(False, False)
    root.mainloop()

