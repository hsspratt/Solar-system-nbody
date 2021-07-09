#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 19:03:30 2021

@author: harry
"""

from tkinter import font
import tkinter as tk

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

root = tk.Tk()
root.title("N Body Simulation")
root.geometry('400x300')

frame = tk.Frame(root)
frame.pack()

# titlefont = font.Font(family="Lucida Grande",size=45)
titlefont = font.Font(family='Helvetica', name='titlefont', size=50, weight='bold')
text_intro = "N-Body Simulation"
title = tk.Label(root, text=text_intro, font=titlefont)
title.place(relx=0.5, rely=0.1, anchor="center")

app = FullScreenApp(root)

root.mainloop()
