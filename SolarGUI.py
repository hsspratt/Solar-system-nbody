#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 15:52:45 2021

@author: harry
"""

import tkinter as tk
import ExampleGUI

root = tk.Tk()
root.title("N Body Simulation")
root.geometry('400x300')
app = ExampleGUI.MyApp(root)
root.mainloop()

# print(app.planets)
