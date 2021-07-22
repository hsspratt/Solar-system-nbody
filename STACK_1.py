import tkinter as tk
from tkinter import font
import os


class MyApp(object):

    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Main frame")
        self.frame = tk.Frame(parent)
        self.frame.pack()

        close_btn = tk.Button(self.frame, text="Close Application", command=self.close_application)
        close_btn.pack()

        global lb

        lb = tk.Listbox(self.root, selectmode = "multiple")
        lb.place(relx=0.25, rely=0.5, anchor="center")

        x =["Choice 1", "Choice 2", "Choice 3"]

        for item in range(len(x)):
        	lb.insert(tk.END, x[item])
        	lb.itemconfig(item, bg="#ffffff")

        tk.Button(self.root, text="Confirm Planets", command=self.confirmSelected).place(relx=0.205, rely=0.62)

        Executefile_btn = tk.Button(self.root, text="Run rando file", command=self.runfile)
        Executefile_btn.place(relx=0.5, rely=0.9)

    """
    def closeApplication(self):
        self.root.destroy()
    """

    def close_application(self):
        self.root.destroy()
        exit()


    def runfile(self):
        self.root.destroy()
    """
    def runfile(self):
        os.system('python STACK_3.py')
    """
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
        return planets

