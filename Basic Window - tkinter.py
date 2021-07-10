import tkinter as tk # importing tkinter into namespace 

root = tk.Tk() # creating a root window

label = tk.Label(root, text="I am a label widget") # configures label

button = tk.Button(root, text="I am a button widget") # cofigures widget

label.place(relx=0.5, rely=0.2) # places label onto window

button.place(relx=0.5, rely=0.4) # places button onto window

root.mainloop() # keeps the program running even after script has stopped
