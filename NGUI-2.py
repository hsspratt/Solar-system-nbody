#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:48:37 2020

@author: harry
"""
from tkinter import *
import tkinter.font as tkFont
from subprocess import Popen
import os
import sys


root = Tk()
root.title("N Body Simulation")

def exitclick():
    root.destroy()
    sys.exit()

def runSlimSim():
    exec(open("SlimSimulation.py").read())

def helloCallBack():
    os.system('python SlimSimulation.py')

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
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


frame = Frame(root)
frame.pack()

fontStyle = tkFont.Font(family="Lucida Grande", size=45)
text_intro = "N-Body Simulation"
title = Label(root, text=text_intro, font=fontStyle)
title.place(relx=0.5, rely=0.1, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=12)
text_intro = "This is the GUI for the N-Body simulation, from here you can change the plents and the initial conditions"
label = Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.5, rely=0.2, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=25)
text_intro = "Planets"
label = Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.25, rely=0.28)

fontStyle = tkFont.Font(family="Lucida Grande", size=25)
text_intro = "Universal Constants"
label = Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.75, rely=0.30, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=12)
text_intro = "Gravitational Constant (G)"
G_constant = Label(root, text=text_intro, font=fontStyle)
G_constant.place(relx=0.68, rely=0.35, anchor="center")

run_slimsim_button = Button(root, text="Run Slim Simulation", command=runSlimSim, height=5, width = 20)
# close_button.place(relx=0.8, rely=20)
run_slimsim_button.place(relx=0.75, rely=0.5, anchor="center")

close_button = Button(root, text="Close", command=exitclick, height=5, width = 30)
# close_button.place(relx=0.8, rely=20)
close_button.place(relx=0.5, rely=0.9, anchor="center")

def var_states():
   print("male: %d,\nfemale: %d" % (planet_1.get(), planet_2.get()))


def addtolist():
    global List

    List = []
    for item in varList:
        if item.get() != "":
            List.append(item.get())
    print(List)
    if len(List) < 1:
        print("At least two planets / stars needed")

    return List

planets = []
varList = []

planet_1 = StringVar()
Checkbutton(root, text="Mercury", variable=planet_1, onvalue="Mercury", offvalue="").place(relx=0.25, rely=0.35)

planet_2 = StringVar()
Checkbutton(root, text="Venus", variable=planet_2, onvalue="Venus", offvalue="").place(relx=0.25, rely=0.40)

planet_3 = StringVar()
Checkbutton(root, text="Earth", variable=planet_3, onvalue="Earth", offvalue="").place(relx=0.25, rely=0.45)

planet_4 = StringVar()
Checkbutton(root, text="Mars", variable=planet_4, onvalue="Mars", offvalue="").place(relx=0.25, rely=0.50)

planet_5 = StringVar()
Checkbutton(root, text="Jupiter", variable=planet_5, onvalue="Jupiter", offvalue="").place(relx=0.25, rely=0.55)

planet_6 = StringVar()
Checkbutton(root, text="Saturn", variable=planet_6, onvalue="Saturn", offvalue="").place(relx=0.25, rely=0.60)

planet_7 = StringVar()
Checkbutton(root, text="Uranus", variable=planet_7, onvalue="Uranus", offvalue="").place(relx=0.25, rely=0.65)

planet_8 = StringVar()
Checkbutton(root, text="Neptune", variable=planet_8, onvalue="Neptune", offvalue="").place(relx=0.25, rely=0.70)

planet_9 = StringVar()
Checkbutton(root, text="Pluto", variable=planet_9, onvalue="Pluto", offvalue="").place(relx=0.25, rely=0.75)


varList.append(planet_1)
varList.append(planet_2)
varList.append(planet_3)
varList.append(planet_4)
varList.append(planet_5)
varList.append(planet_6)
varList.append(planet_7)
varList.append(planet_8)
varList.append(planet_9)

button_planets = Button(root,text='Confirm Planets',command=addtolist)
button_planets.place(relx=0.25, rely=0.80)

List = addtolist

Button(root, text='Show', command=var_states).pack()

def set_text(text):
    e.delete(0,END)
    e.insert(0,text)
    return


e = Entry(root, width=10, borderwidth=1)
e.place(relx=0.80, rely=0.35, anchor="center")
e.insert(0, "6.6743015")
e.focus_set()

def changeG():
    global e
    global G
    G = e.get()
    # text.insert(INSERT, G)

G_button = Button(root,text='Change Constants',command=changeG)
G_button.place(relx=0.75, rely=0.4, anchor="center")


app = FullScreenApp(root)

root.mainloop()
