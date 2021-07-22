import tkinter as tk
from tkinter import font
import os


########################################################################
class n_body_app(object):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Main frame")
        self.frame = tk.Frame(parent)
        self.frame.pack()
        
        settings = {"G": 6.6743015, "bar": 1, "baz": 1}

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
        label.place(relx=0.75, rely=0.30, anchor="center")

        fontStyle = font.Font(family="Lucida Grande", size=12)
        text_intro = "Gravitational Constant (G)"
        G_constant = tk.Label(self.root, text=text_intro, font=fontStyle)
        G_constant.place(relx=0.68, rely=0.35, anchor="center")

        fontStyle = font.Font(family="Lucida Grande", size=25)
        text_intro = "Select Your Planets"
        planetslabel = tk.Label(self.root, text=text_intro, font=fontStyle)
        planetslabel.place(relx=0.25, rely=0.3, anchor="center")

        global lb

        lb = tk.Listbox(self.root, selectmode = "multiple")
        lb.place(relx=0.25, rely=0.5, anchor="center")

        x = ["Mercury", "Venus", "Earth", "Mars", "Jupiter","Saturn", "Uranus", "Neptune", "Pluto", "AC1", "AC2", "AC_star","F8_1", "F8_2", "F8_3", "F8_planet"]

        for item in range(len(x)):
        	lb.insert(tk.END, x[item])
        	lb.itemconfig(item, bg="#ffffff")

        tk.Button(self.root, text="Confirm Planets", command=self.confirmSelected).place(relx=0.205, rely=0.62)

        e = tk.Entry(self.root, width=10, borderwidth=1)
        e.place(relx=0.80, rely=0.35, anchor="center")
        e.insert(0, "6.6743015")
        e.focus_set()

        G = 6.6743015
        G_button = tk.Button(self.root,text='Change Constants',command=self.change_variable(G,e))
        G_button.place(relx=0.75, rely=0.4, anchor="center")

        Executefile_btn = tk.Button(self.root, text="Run rando file", command=self.runfile)
        Executefile_btn.place(relx=0.5, rely=0.9)


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
        cname = lb.curselection()
        for i in cname:
            op = lb.get(i)
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
    
    """
    def confirmSelected():
        global planets
        planets = []
        cname = lb.curselection()
        for i in cname:
            op = lb.get(i)
            planets.append(op)
        for val in planets:
            print(val)
        if len(planets) < 2:
            print("At least two planets need to be selected")
    """
    
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
