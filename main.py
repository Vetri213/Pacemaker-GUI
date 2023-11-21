import tkinter

import pygame
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.place(relheight=1,relwidth=1)
        self.home()

    def set_background_image(window, image_path):
        image = Image.open(image_path)
        image = image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)

        label = Label(window, image=photo)
        label.image = photo
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def home(self):
        #Change Background
        self.set_background_image("ECGv1.png")
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
        self.register_button = ttk.Button(master=self, text="Register", command=register_func)
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


#Login Function
class Login(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.place(relheight=1, relwidth=1)
        self.login()

    def set_background_image(window, image_path):
        image = Image.open(image_path)
        image = image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)

        label = Label(window, image=photo)
        label.image = photo
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def login(self):
        #Change Background
        self.set_background_image("ECGv1.png")

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

        # Exit Button
        self.exit_button = ttk.Button(master=self, text="Exit", command=quit)
        self.exit_button.pack()

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
            pacing_modes(username, vals)

        else:
            changing_label.configure(text="No User Matches Your Input. Please Try Again.")



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

def show_aoo_mode_page():
    def update_aoo():
        global aoo_vals
        if 30 <= int(lower_rate_entry.get()) <= 175 and 50 <= int(upper_rate_entry.get()) <= 175 and 0.0 <= float(atrial_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(atrial_pulse_width_entry.get()) <= 1.9:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                aoo_vals= [lower_rate_entry.get(),upper_rate_entry.get(),atrial_amplitude_entry.get(),atrial_pulse_width_entry.get()]

        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            aoo_window.destroy()

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
    lower_rate_entry.insert(0,aoo_vals[0])
    lower_rate_label.pack(pady=10)
    lower_rate_entry.pack(pady=10)

    upper_rate_label = ttk.Label(aoo_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(aoo_window, font=("Arial", 16))
    upper_rate_entry.insert(0, aoo_vals[1])
    upper_rate_label.pack(pady=10)
    upper_rate_entry.pack(pady=10)

    atrial_amplitude_label = ttk.Label(aoo_window, text="Atrial Amplitude:", background="black", foreground="white", font=("Arial", 16))
    atrial_amplitude_entry = Entry(aoo_window, font=("Arial", 16))
    atrial_amplitude_entry.insert(0, aoo_vals[2])
    atrial_amplitude_label.pack(pady=10)
    atrial_amplitude_entry.pack(pady=10)

    atrial_pulse_width_label = ttk.Label(aoo_window, text="Atrial Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    atrial_pulse_width_entry = Entry(aoo_window, font=("Arial", 16))
    atrial_pulse_width_entry.insert(0,aoo_vals[3])
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
    style.map('TButton', background=[('active', 'teal')])


    # Create a "Save" button
    save_button = ttk.Button(master=aoo_window, text="Save", style='TButton', command=update_aoo)
    save_button.pack(pady=10)

    # Create a "back" button to return to "Pacing mode"
    back_button = ttk.Button(master=aoo_window, text="Back to Pacing Modes", command=aoo_window.destroy)
    back_button.pack(pady=5)
def show_voo_mode_page():
    def update_voo():
        global voo_vals
        if 30 <= int(lower_rate_entry.get()) <= 175 and 50 <= int(upper_rate_entry.get()) <= 175 and 0.0 <= float(ventricular_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(ventricular_pulse_width_entry.get()) <= 1.9 and 150<=int(arp_entry.get())<=500:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                voo_vals= [lower_rate_entry.get(),upper_rate_entry.get(),ventricular_amplitude_entry.get(),
                       ventricular_pulse_width_entry.get(), arp_entry.get()]
                voo_window.destroy()
        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")

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
    lower_rate_entry.insert(0,voo_vals[0])
    lower_rate_label.pack(pady=10)
    lower_rate_entry.pack(pady=10)

    upper_rate_label = ttk.Label(voo_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(voo_window, font=("Arial", 16))
    upper_rate_entry.insert(0,voo_vals[1])
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
    ventricular_amplitude_entry.insert(0,voo_vals[2])
    ventricular_amplitude_label.pack(pady=10)
    ventricular_amplitude_entry.pack(pady=10)

    ventricular_pulse_width_label = ttk.Label(voo_window, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    ventricular_pulse_width_entry = Entry(voo_window, font=("Arial", 16))
    ventricular_pulse_width_entry.insert(0,voo_vals[3])
    ventricular_pulse_width_label.pack(pady=10)
    ventricular_pulse_width_entry.pack(pady=10)

    #vrp_label = ttk.Label(voo_window, text="VRP:", background="black", foreground="white", font=("Arial", 16))
    #vrp_entry = Entry(voo_window, font=("Arial", 16))
    #vrp_label.pack(pady=10)
    #vrp_entry.pack(pady=10)

    arp_label = ttk.Label(voo_window, text="ARP:", background="black", foreground="white", font=("Arial", 16))
    arp_entry = Entry(voo_window, font=("Arial", 16))
    arp_entry.insert(0,voo_vals[4])
    arp_label.pack(pady=10)
    arp_entry.pack(pady=10)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                    focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'teal')])

     # Create a "Save" button
    save_button = ttk.Button(voo_window, text="Save", command=update_voo)
    save_button.pack(pady=10)

    # Create a "back" button to return to "Pacing mode"
    back_button = ttk.Button(voo_window, text="Back to Pacing Modes", command=voo_window.destroy)
    back_button.pack(pady=5)
def show_aai_mode_page():
    def update_aai():
        global aai_vals
        if 30<= int(lower_rate_entry.get())<=175 and 50<= int(upper_rate_entry.get())<=175 and 0.0<= float(atrial_amplitude_entry.get())<=7\
                and 0.05 <=float(atrial_pulse_width_entry.get())<=1.9 and 0.25<=float(atrial_sensitivity_entry.get())<=10\
                and 150<=int(arp_entry.get())<=500 and 150<=int(pvarp_entry.get())<=500 and (30<=int(hysteresis_entry.get())<=175 or int(hysteresis_entry.get())==0)\
                and 0<=int(rate_smoothing_entry.get())<=21:
            result = messagebox.askokcancel("Confirmation","Are you sure?")
            if (result):
                aai_vals=[lower_rate_entry.get(), upper_rate_entry.get(), atrial_amplitude_entry.get(),
                          atrial_pulse_width_entry.get(), atrial_sensitivity_entry.get(), arp_entry.get(),
                          pvarp_entry.get(), hysteresis_entry.get(), rate_smoothing_entry.get()]
        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            aai_window.destroy()

    aai_window = Tk()
    aai_window.geometry('%dx%d+0+0' % (width, height))
    aai_window.title("AAI Mode")
    aai_window.configure(background="black")

    # Add label
    aai_label = ttk.Label(aai_window, text="            AAI Mode Information", background="black", foreground="white",font=("Arial", 40))
    aai_label.grid(row=0, column=0, columnspan=9, pady=10, padx =300)

    # Add the parameter here
    lower_rate_label = ttk.Label(aai_window, text="Lower Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    lower_rate_label.grid(row=1, column=5, pady=10, padx =10)
    lower_rate_entry = Entry(aai_window, font=("Arial", 16))
    lower_rate_entry.insert(0,aai_vals[0])
    lower_rate_entry.grid(row=2, column=5, pady=10, padx =10)

    upper_rate_label = ttk.Label(aai_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(aai_window, font=("Arial", 16))
    upper_rate_entry.insert(0,aai_vals[1])
    upper_rate_label.grid(row=1, column=6, pady=10, padx =10)
    upper_rate_entry.grid(row=2, column=6, pady=10, padx =10)

    atrial_amplitude_label = ttk.Label(aai_window, text="Atrial Amplitude:", background="black", foreground="white", font=("Arial", 16))
    atrial_amplitude_entry = Entry(aai_window, font=("Arial", 16))
    atrial_amplitude_entry.insert(0,aai_vals[2])
    atrial_amplitude_label.grid(row=3, column=5, pady=10, padx =10)
    atrial_amplitude_entry.grid(row=4, column=5, pady=10, padx =10)

    atrial_pulse_width_label = ttk.Label(aai_window, text="Atrial Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    atrial_pulse_width_entry = Entry(aai_window, font=("Arial", 16))
    atrial_pulse_width_entry.insert(0,aai_vals[3])
    atrial_pulse_width_label.grid(row=3, column=6, pady=10, padx =10)
    atrial_pulse_width_entry.grid(row=4, column=6, pady=10, padx =10)

    atrial_sensitivity_label = ttk.Label(aai_window, text="Atrial Sensitivity:", background="black", foreground="white", font=("Arial", 16))
    atrial_sensitivity_entry = Entry(aai_window, font=("Arial", 16))
    atrial_sensitivity_entry.insert(0,aai_vals[4])
    atrial_sensitivity_label.grid(row=5, column=5, pady=10, padx =10)
    atrial_sensitivity_entry.grid(row=6, column=5, pady=10, padx =10)

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
    arp_entry.insert(0,aai_vals[5])
    arp_label.grid(row=5, column=6, pady=10, padx =10)
    arp_entry.grid(row=6, column=6, pady=10, padx =10)

    pvarp_label = ttk.Label(aai_window, text="PVARP:", background="black", foreground="white", font=("Arial", 16))
    pvarp_entry = Entry(aai_window, font=("Arial", 16))
    pvarp_entry.insert(0,aai_vals[6])
    pvarp_label.grid(row=7, column=5, pady=10, padx =10)
    pvarp_entry.grid(row=8, column=5, pady=10, padx =10)

    hysteresis_label = ttk.Label(aai_window, text="Hysteresis:", background="black", foreground="white", font=("Arial", 16))
    hysteresis_entry = Entry(aai_window, font=("Arial", 16))
    hysteresis_entry.insert(0,aai_vals[7])
    hysteresis_label.grid(row=7, column=6, pady=10, padx=10)
    hysteresis_entry.grid(row=8, column=6, pady=10, padx=10)

    rate_smoothing_label = ttk.Label(aai_window, text="Rate Smoothing:", background="black", foreground="white", font=("Arial", 16))
    rate_smoothing_entry = Entry(aai_window, font=("Arial", 16))
    rate_smoothing_entry.insert(0,aai_vals[8])
    rate_smoothing_label.grid(row=9, column=5, pady=10)
    rate_smoothing_entry.grid(row=10, column=5, pady=10)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=50, height=30, borderwidth=1,
                    focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'teal')])

     # Create a "Save" button
    save_button = ttk.Button(aai_window, text="Save", command=update_aai)
    save_button.grid(row=12, column=5, pady=10)

    # Create a "back" button to return to "Pacing mode"
    back_button = ttk.Button(aai_window, text="Back to Pacing Modes", command=aai_window.destroy)
    back_button.grid(row=12, column=6, pady=10)
def show_vvi_mode_page():
    def update_vvi():
        global vvi_vals
        if 30 <= int(lower_rate_entry.get()) <= 175 and 50 <= int(upper_rate_entry.get()) <= 175 and 0.0 <= float(ventricular_amplitude_entry.get()) <= 7 \
                and 0.05 <= float(ventricular_pulse_width_entry.get()) <= 1.9 and 0.25 <= float(ventricular_sensitivity_entry.get()) <= 10 \
                and 150 <= int(vrp_entry.get()) <= 500 and (30 <= int(hysteresis_entry.get()) <= 175 or int(hysteresis_entry.get()) == 0) \
                and 0 <= int(rate_smoothing_entry.get()) <= 21:
            result = messagebox.askokcancel("Confirmation", "Are you sure?")
            if (result):
                vvi_vals = [lower_rate_entry.get(), upper_rate_entry.get(), ventricular_amplitude_entry.get(),
                            ventricular_pulse_width_entry.get(), ventricular_sensitivity_entry.get(), vrp_entry.get(), hysteresis_entry.get(),
                            rate_smoothing_entry.get()]
        else:
            messagebox.showerror("Input is not in range", "Please enter valid values for all parameters.")
            vvi_window.destroy()

    vvi_window = Tk()
    vvi_window.geometry('%dx%d+0+0' % (width, height))
    vvi_window.title("VVI Mode")
    vvi_window.configure(background="black")

    # Add label
    vvi_label = ttk.Label(vvi_window, text="            VVI Mode Information", background="black", foreground="white", font=("Arial", 40))
    vvi_label.grid(row=0, column=0, columnspan=9, pady=10, padx=300)

    # Add the parameter here
    lower_rate_label = ttk.Label(vvi_window, text="Lower Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    lower_rate_entry = Entry(vvi_window, font=("Arial", 16))
    lower_rate_entry.insert(0,vvi_vals[0])
    lower_rate_label.grid(row=1, column=5, pady=10, padx =10)
    lower_rate_entry.grid(row=2, column=5, pady=10, padx =10)

    upper_rate_label = ttk.Label(vvi_window, text="Upper Rate Limit:", background="black", foreground="white", font=("Arial", 16))
    upper_rate_entry = Entry(vvi_window, font=("Arial", 16))
    upper_rate_entry.insert(0,vvi_vals[1])
    upper_rate_label.grid(row=1, column=6, pady=10, padx =10)
    upper_rate_entry.grid(row=2, column=6, pady=10, padx =10)

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
    ventricular_amplitude_entry.insert(0,vvi_vals[2])
    ventricular_amplitude_label.grid(row=3, column=5, pady=10, padx =10)
    ventricular_amplitude_entry.grid(row=4, column=5, pady=10, padx =10)

    ventricular_pulse_width_label = ttk.Label(vvi_window, text="Ventricular Pulse Width:", background="black", foreground="white", font=("Arial", 16))
    ventricular_pulse_width_entry = Entry(vvi_window, font=("Arial", 16))
    ventricular_pulse_width_entry.insert(0,vvi_vals[3])
    ventricular_pulse_width_label.grid(row=3, column=6, pady=10, padx =10)
    ventricular_pulse_width_entry.grid(row=4, column=6, pady=10, padx =10)


    ventricular_sensitivity_label = ttk.Label(vvi_window, text="Ventricular Sensitivity:", background="black", foreground="white", font=("Arial", 16))
    ventricular_sensitivity_entry = Entry(vvi_window, font=("Arial", 16))
    ventricular_sensitivity_entry.insert(0,vvi_vals[4])
    ventricular_sensitivity_label.grid(row=5, column=5, pady=10, padx =10)
    ventricular_sensitivity_entry.grid(row=6, column=5, pady=10, padx =10)

    vrp_label = ttk.Label(vvi_window, text="VRP:", background="black", foreground="white", font=("Arial", 16))
    vrp_entry = Entry(vvi_window, font=("Arial", 16))
    vrp_entry.insert(0,vvi_vals[5])
    vrp_label.grid(row=5, column=6, pady=10, padx =10)
    vrp_entry.grid(row=6, column=6, pady=10, padx =10)

    hysteresis_label = ttk.Label(vvi_window, text="Hysteresis:", background="black", foreground="white", font=("Arial", 16))
    hysteresis_entry = Entry(vvi_window, font=("Arial", 16))
    hysteresis_entry.insert(0,vvi_vals[6])
    hysteresis_label.grid(row=7, column=5, pady=10, padx =10)
    hysteresis_entry.grid(row=8, column=5, pady=10, padx =10)

    rate_smoothing_label = ttk.Label(vvi_window, text="Rate Smoothing:", background="black", foreground="white", font=("Arial", 16))
    rate_smoothing_entry = Entry(vvi_window, font=("Arial", 16))
    rate_smoothing_entry.insert(0,vvi_vals[7])
    rate_smoothing_label.grid(row=7, column=6, pady=10, padx =10)
    rate_smoothing_entry.grid(row=8, column=6, pady=10, padx =10)

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
    style.map('TButton', background=[('active', 'teal')])

    # Create a "Save" button
    save_button = ttk.Button(vvi_window, text="Save", command=update_vvi)
    save_button.grid(row=12, column=5, pady=10, padx =10)

    # Creat a "back" button to return to "Pacing mode"
    back_button = ttk.Button(vvi_window, text="Back to Pacing Modes", command=vvi_window.destroy)
    back_button.grid(row=12, column=6, pady=10, padx =10)

def pacing_modes(user,vals):
    aoo_vals_str,voo_vals_str,aai_vals_str,vvi_vals_str,temp = vals.split("}")
    aoo_vals_str = aoo_vals_str.strip("{")
    voo_vals_str = voo_vals_str.strip("{")
    aai_vals_str = aai_vals_str.strip("{")
    vvi_vals_str = vvi_vals_str.strip("{")
    global aoo_vals
    global voo_vals
    global aai_vals
    global vvi_vals
    aoo_vals = aoo_vals_str.split(",")
    voo_vals = voo_vals_str.split(",")
    aai_vals = aai_vals_str.split(",")
    vvi_vals = vvi_vals_str.split(",")
    # print(aoo_vals)
    # print(voo_vals)
    # print(aai_vals)
    # print(vvi_vals)
    def save():
        file = open("text.txt", "w")
        for i in range(len(users)):
            # print(user)
            if (users[i][0] == user):
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
                current_vals_str += "}"
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
    def save_and_logout():
        save()
        home()

    def save_and_quit():
        save()
        quit()
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

    new_old = ttk.Label(master=pacing_modes, text="New Pacemaker Detected", background=bg, foreground=fg, font=("Arial", 20))
    new_old.pack(pady=10)

    connectivity = ttk.Label(master=pacing_modes, text="Device Disconnected", background=bg, foreground=fg, font=("Arial", 20))
    connectivity.pack(pady=10)

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=10, height =30, borderwidth=1, focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'teal')])

    # Create buttons and add them to the frame

    button1 = ttk.Button(master = pacing_modes, text="AOO", style='Pacing.TButton',command=show_aoo_mode_page)
    button1.pack(pady=20)

    button2 = ttk.Button(master = pacing_modes, text="VOO", style='Pacing.TButton',command=show_voo_mode_page)
    button2.pack(pady=20)
    button3 = ttk.Button(master = pacing_modes, text="AAI", style='Pacing.TButton',command=show_aai_mode_page)
    button3.pack(pady=20)
    button4 = ttk.Button(master = pacing_modes, text="VVI", style='Pacing.TButton',command=show_vvi_mode_page)
    button4.pack(pady=20)
    button5 = ttk.Button(master=pacing_modes, text="EGRAM", style='Pacing.TButton', command=show_egram_page)
    button5.pack(pady=20)

    logout = ttk.Button(master=pacing_modes, text="Logout", style='Pacing.TButton', command=save_and_logout)
    logout.pack(pady=20)

    # Exit Button33
    exit_button = ttk.Button(master=pacing_modes, text="Exit", command=save_and_quit)
    exit_button.pack(pady=20)

    # Use the grid layout manager to arrange the buttons in columns
    #button1.grid(row=0, column=0, padx=30, pady=30)
    #button2.grid(row=0, column=1, padx=30, pady=30)
    #button3.grid(row=1, column=0, padx=30, pady=30)
    #button4.grid(row=1, column=1, padx=30, pady=30)



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
        #print(len(users))

        if (len(users) <10):
            #Getting Username and Password from the Textboxes
            username = user_text.get()
            password = password_text.get()
            if not username or not password:
                changing_label.configure(text="Username or password cannot be empty")
            elif is_username_taken(username):
                changing_label.configure(text="Username is already taken")
            else:
            #Creating a New Entry to be added to the file of Users (in the same format)
                new_entry = username+"|"+password+"|{30, 50, 0, 0.05}{30,50,0,0.05,150}{30,50,0,0.05,0.25,150,150,0,0}{30,50,0,0.05,0.35,150,0,0}\n"
            #Opening File in Append Mode (So as not to delete other users)
                file = open("text.txt", "a")
            #Adding Entry
                file.write(new_entry)
            #Closing file
                file.close()

                users.append([username,password])
                all_vals.append("{30, 50, 0, 0.05}{30,50,0,0.05,150}{30,50,0,0.05,0.25,150,150,0,0}{30,50,0,0.05,0.35,150,0,0}")

            # Go to the ACTUAL DO STUFF PAGE
                changing_label.configure(text="Information Recognized!")
                register.destroy()
                pacing_modes(username)
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
    user_text = Entry(master=register, width=50, font=("Arial", 20))
    user_text.pack()

    # Password
    password_label = ttk.Label(master=register, text="Password:", background=bg, foreground=fg, font=("Arial", 20))
    password_label.pack(pady=20)
    password_text = Entry(master=register, width=50, font=("Arial", 20), show="*")
    password_text.pack()

    # Style of Buttons
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background="black", foreground="white", width=20, borderwidth=1, focusthickness=3,
                    focuscolor='none', font=('American typewriter', 20))
    # When Hovering
    style.map('TButton', background=[('active', 'teal')])

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