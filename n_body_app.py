# %%

import tkinter as tk
from tkinter import font
import os
from tkinter.messagebox import showinfo

class n_body_app(object):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Main frame")
        self.frame = tk.Frame(parent)
        self.frame.pack()
        
        self.G = tk.StringVar()
        self.time_period = tk.StringVar()
        self.n_time_period = tk.StringVar()
        self.iterations = tk.StringVar()
        self.rtol = tk.StringVar()
        self.atol = tk.StringVar()
        self.K = tk.IntVar()

        
        close_btn = tk.Button(self.frame, text="Close Application", command=self.close_application)
        close_btn.pack()

        titlefont = font.Font(family="Lucida Grande",size=45)
        text_intro = "N-Body Simulation"
        title = tk.Label(self.root, text=text_intro, font=titlefont)
        title.place(relx=0.5, rely=0.1, anchor="center")

        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "This is the GUI for the N-Body simulation, from here you can change the planets and the initial conditions along with executing the scripts"
        label = tk.Label(self.root, text=text_intro, font=fontStyle)
        label.place(relx=0.5, rely=0.2, anchor="center")

        fontStyle = font.Font(family="Lucida Grande", size=25)
        text_intro = "Universal Constants"
        label = tk.Label(self.root, text=text_intro, font=fontStyle)
        label.place(relx=0.826, rely=0.30, anchor="center")

        fontStyle = font.Font(family="Lucida Grande", size=25)
        text_intro = "Select Your Planets"
        planetslabel = tk.Label(self.root, text=text_intro, font=fontStyle)
        planetslabel.place(relx=0.1665, rely=0.3, anchor="center")

        fontStyle = font.Font(family="Lucida Grande", size=25)
        text_intro = "Select ODE solver"
        planetslabel = tk.Label(self.root, text=text_intro, font=fontStyle)
        planetslabel.place(relx=0.5, rely=0.3, anchor="center")
        
        global lb_planets

        lb_planets = tk.Listbox(self.root, selectmode = "multiple")
        lb_planets.place(relx=0.1665, rely=0.5, anchor="center")

        p = ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter",
             "Saturn", "Uranus", "Neptune", "Pluto", "AC1", "AC2", 
             "AC_star","F8_1", "F8_2", "F8_3", "F8_planet", "Butterfly_I",
             "Butterfly_II", "Butterfly_III", "moth_I", "moth_II", 
             "moth_III", "bumblebee"]
        
        for item in range(len(p)):
        	lb_planets.insert(tk.END, p[item])
        	lb_planets.itemconfig(item, bg="#ffffff")

        tk.Button(self.root, text="Confirm Planets",
                  command=self.confirmSelected).place(relx=0.1665, rely=0.67, anchor="center")
        
        global lb_integrator
        
        lb_integrator = tk.Listbox(self.root, selectmode="multiple")
        lb_integrator.place(relx=0.5, rely=0.5, anchor="center")

        integrator = ["RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"]
 
        for item in range(len(integrator)):
            lb_integrator.insert(tk.END, integrator[item])
            lb_integrator.itemconfig(item, bg="#ffffff")

        tk.Button(self.root, text="Confirm Odesolver",
                  command=self.confirm_integrator).place(relx=0.5, rely=0.67, anchor="center")
        
        K_button = tk.Radiobutton(self.root, text='Simlify Simulation', variable=self.K, value=1)
        K_button.place(relx=0.83, rely=0.85, anchor="center")

        # G constant
        
        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "Gravitational Constant (G)"
        G_constant = tk.Label(self.root, text=text_intro, font=fontStyle)
        G_constant.place(relx=0.68, rely=0.40, anchor="center")

        G_entry = tk.Entry(self.root, textvariable=self.G)
        G_entry.place(relx=0.80, rely=0.40, anchor="center")
        G_entry.insert(0, "6.6743015e-11")
        G_entry.focus()
        
        # time period
        
        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "Time Period (s):"
        time_period_label = tk.Label(self.root, text=text_intro, font=fontStyle)
        time_period_label.place(relx=0.68, rely=0.45, anchor="center")

        time_period_entry = tk.Entry(self.root, textvariable=self.time_period)
        time_period_entry.place(relx=0.80, rely=0.45, anchor="center")
        time_period_entry.insert(0, "31536000")
        time_period_entry.focus()
        
        # Number of time periods
        
        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "Number of time periods (n):"
        n_time_period_label = tk.Label(self.root, text=text_intro, font=fontStyle)
        n_time_period_label.place(relx=0.68, rely=0.5, anchor="center")

        n_time_period_entry = tk.Entry(self.root, textvariable=self.n_time_period)
        n_time_period_entry.place(relx=0.80, rely=0.5, anchor="center")
        n_time_period_entry.insert(0, "100")
        n_time_period_entry.focus()
        
        # Iterations per time period
        
        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "Iterations per time period (I):"
        iterations_label = tk.Label(self.root, text=text_intro, font=fontStyle)
        iterations_label.place(relx=0.68, rely=0.55, anchor="center")

        iterations_entry = tk.Entry(self.root, textvariable=self.iterations)
        iterations_entry.place(relx=0.80, rely=0.55, anchor="center")
        iterations_entry.insert(0, "25")
        iterations_entry.focus()
        
        # rtol

        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "Relative tolerance:"
        rtol_label = tk.Label(self.root, text=text_intro, font=fontStyle)
        rtol_label.place(relx=0.68, rely=0.6, anchor="center")

        rtol_entry = tk.Entry(self.root, textvariable=self.rtol)
        rtol_entry.place(relx=0.80, rely=0.6, anchor="center")
        rtol_entry.insert(0, "1e-3")
        rtol_entry.focus()
        
        # atol
        
        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "Absolute tolerance:"
        atol_label = tk.Label(self.root, text=text_intro, font=fontStyle)
        atol_label.place(relx=0.68, rely=0.65, anchor="center")

        atol_entry = tk.Entry(self.root, textvariable=self.atol)
        atol_entry.place(relx=0.80, rely=0.65, anchor="center")
        atol_entry.insert(0, "1e-6")
        atol_entry.focus()
          
        # login button
        login_button = tk.Button(self.root, text="Check what values are inputted", command=self.login_clicked)
        login_button.place(relx=0.8333, rely=0.72, anchor="center")

        Executefile_btn = tk.Button(self.root, text="Run simulation", command=self.runfile)
        Executefile_btn.place(relx=0.5, rely=0.9, anchor="center")


        self.FullScreenApp(parent)
        
    #----------------------------------------------------------------------

    def close_application(self):
        self.root.destroy()
        exit()

    #----------------------------------------------------------------------
    def FullScreenApp(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


    def confirmSelected(self):
        planets = []
        cname = lb_planets.curselection()
        for i in cname:
            op = lb_planets.get(i)
            planets.append(op)
            self.planets = planets
        for val in planets:
            print(val)
        if len(planets) < 2:
            print("At least two planets need to be selected")
        if planets == ["AC1", "AC2"]:
            print("This is the Alpha Centauri binary star system")
        if planets == ["AC1", "AC2","AC_star"]:
            print("This is the Alpha Centauri binary star system with a planet")
        if planets == ["F8_1", "F8_2", "F8_3"]:
            print("This is the figure of eight solution")
        return planets
    
    def confirm_integrator(self):
        ODE = []
        cname = lb_integrator.curselection()
        for i in cname:
            op = lb_integrator.get(i)
            ODE.append(op)
            self.ODE = ODE
        for val in ODE:
            print(val)
        if len(ODE) > 1:
            print("Only one ODE solver must be selected!")
        if len(ODE) == 0:
            ODE = ["RK45"]
            print("The defult ODE solver will be used")
        return ODE
    
    def runfile(self):
        self.root.destroy()

    def set_text(self, text):
        self.e.delete(0,tk.END)
        self.e.insert(0,text)
        return

    def change_variable(self, variable, value):
        # global e
        # global variable
        variable = self.value.get()
        # text.insert(INSERT, G)
        
    def change_value(self, settings, name, value):
        settings[name] = 2

    def login_clicked(self):
        """ callback when the login button clicked
        """
        msg = f'You entered: \n G: {self.G.get()} \n time period: {self.time_period.get()} \n number of time periods: {self.n_time_period.get()} \n iterations per time: {self.iterations.get()} \n rtol: {self.rtol.get()} \n atol: {self.atol.get()}'
        showinfo(
            title='Values used',
            message=msg
        )
# %%
