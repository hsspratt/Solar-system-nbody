#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 18:11:05 2021

@author: harry
"""

import tkinter as tk
import tkinter.font as tkFont
# from subprocess import Popen
import os
import sys

def exitclick():
    root.destroy()
    sys.exit()

def addtolist():
    global List

    # List = []
    for item in varList:
        if item.get() == "0":
            List.append(item.get())
    print(List)
    if len(List) > 1:
        print("It's worked")

    return List

root = tk.Tk()
root.title("N Body Simulation")

frame = tk.Frame(root)

fontStyle = tkFont.Font(family="Lucida Grande", size=45)
text_intro = "N-Body Simulation"
title = tk.Label(root, text=text_intro, font=fontStyle)
title.place(relx=0.5, rely=0.1, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=12)
text_intro = "This is the GUI for the N-Body simulation, from here you can change the plents and the initial conditions"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.5, rely=0.2, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=25)
text_intro = "Planets"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.25, rely=0.28)


close_button = tk.Button(root, text="Close", command=exitclick, height=5, width = 30)
# close_button.place(relx=0.8, rely=20)
close_button.place(relx=0.5, rely=0.9, anchor="center")

planets = []
varList = []
List = []

planet_1 = tk.StringVar()
tk.Checkbutton(root, text="Mercury", variable=planet_1, onvalue="1", offvalue="0").place(relx=0.25, rely=0.35)

varList.append(planet_1)

button_planets = tk.Button(root,text='Confirm Planets',command=addtolist).place(relx=0.25, rely=0.80)













frame.mainloop()

# %%

def exitclick():
    root.destroy()
    sys.exit()

def addtolist():
    global List

    # List = []
    for item in varList:
        if item.get() == "0":
            List.append(item.get())
    print(List)
    if len(List) > 1:
        print("It's worked")

    return List

root = tk.Tk()
root.title("N Body Simulation")

frame = tk.Frame(root)

fontStyle = tkFont.Font(family="Lucida Grande", size=45)
text_intro = "N-Body Simulation"
title = tk.Label(root, text=text_intro, font=fontStyle)
title.place(relx=0.5, rely=0.1, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=12)
text_intro = "This is the GUI for the N-Body simulation, from here you can change the plents and the initial conditions"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.5, rely=0.2, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=25)
text_intro = "Planets"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.25, rely=0.28)


close_button = tk.Button(root, text="Close", command=exitclick, height=5, width = 30)
# close_button.place(relx=0.8, rely=20)
close_button.place(relx=0.5, rely=0.9, anchor="center")

planets = []
varList = []
List = []

planet_1 = tk.StringVar()
tk.Checkbutton(root, text="Mercury", variable=planet_1, onvalue="1", offvalue="0").place(relx=0.25, rely=0.35)

varList.append(planet_1)

button_planets = tk.Button(root,text='Confirm Planets',command=addtolist).place(relx=0.25, rely=0.80)

frame.mainloop()
# %%

# Import relevant modules

import tkinter as tk
import tkinter.font as tkFont
# from subprocess import Popen
# import os
# import sys

# Definitions

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

def exitclick():
    root.destroy()
    sys.exit()

# GUI

root = tk.Tk()
root.title("N Body Simulation")
root.geometry('400x300')

var = tk.StringVar()

frame = tk.Frame(root)
frame.pack()

fontStyle = tkFont.Font(family="Lucida Grande", size=45)
text_intro = "N-Body Simulation"
title = tk.Label(root, text=text_intro, font=fontStyle)
title.place(relx=0.5, rely=0.1, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=12)
text_intro = "This is the GUI for the N-Body simulation, from here you can change the plents and the initial conditions"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.5, rely=0.2, anchor="center")

# fontStyle = tkFont.Font(family="Lucida Grande", size=25)
# text_intro = "Planets"
# label = tk.Label(root, text=text_intro, font=fontStyle)
# label.place(relx=0.25, rely=0.28)

fontStyle = tkFont.Font(family="Lucida Grande", size=25)
text_intro = "Universal Constants"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.75, rely=0.30, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=12)
text_intro = "Gravitational Constant (G)"
G_constant = tk.Label(root, text=text_intro, font=fontStyle)
G_constant.place(relx=0.68, rely=0.35, anchor="center")

fontStyle = tkFont.Font(family="Lucida Grande", size=14)
text_intro = "Select Your Planets"
planetslabel = tk.Label(root, text=text_intro, font=fontStyle)
planetslabel.place(relx=0.25, rely=0.28, anchor="center")

close_button = tk.Button(root, text="Close", command=exitclick, height=5, width = 30)
# close_button.place(relx=0.8, rely=20)
close_button.place(relx=0.5, rely=0.9, anchor="center")

lb = tk.Listbox(root, selectmode = "multiple")
lb.place(relx=0.25, rely=0.5, anchor="center")


# show = tk.Label(root, text = "Select Your Planets", font = ("Times", 14), relx = 10, rely = 10)
# show.pack()
# lb = tk.Listbox(root, selectmode = "multiple").place(relx = 0.5, rely = 0.8, expand = tk.YES, fill = "both")

x =["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

for item in range(len(x)):
	lb.insert(tk.END, x[item])
	lb.itemconfig(item, bg="#ffffff")

tk.Button(root, text="Confirm Planets", command=confirmSelected).place(relx=0.20, rely=0.6)

app = FullScreenApp(root)

root.mainloop()

# %%


from tkinter import *
# import tkMessageBox

top = Tk()
top.wm_title("Checklist")
my_items = ['Underwear', 'T_shirst', 'Socks', 'Hats'] # you can expand list of items/check-boxes
check_boxes = {item:IntVar(root) for item in my_items} #create dict of check_boxes

def confirm():
    print(item.get() for item in check_boxes.values()) # just for info to show you the reasult
    if all(item.get() for item in check_boxes.values()):
        pass # do something you want

def addtolist():
    global List

    # List = []
    for item in my_items:
        if item.get() == "0":
            List.append(item.get())
    print(List)
    if len(List) > 1:
        print("It's worked")

    return List

#create all check-boxes on the form
for item in my_items:
    C = Checkbutton(top, text = item, variable = check_boxes[item], anchor = W,  onvalue = str(item), offvalue = 0, height=1, width = 40)
    C.pack()

B1 = Button(top, text = "Confirm", command = addtolist)
B1.pack()


top.mainloop()