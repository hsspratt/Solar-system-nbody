import tkinter as tk
from tkinter import font

from ExampleGUI import MyApp

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

root = tk.Tk()
root.title("N Body Simulation")
root.geometry('400x300')

frame = tk.Frame(root)
frame.pack()


titlefont = font.Font(family="Lucida Grande",size=45)
text_intro = "N-Body Simulation"
title = tk.Label(root, text=text_intro, font=titlefont)
title.place(relx=0.5, rely=0.1, anchor="center")

fontStyle = font.Font(family="Lucida Grande", size=12)
text_intro = "This is the GUI for the N-Body simulation, from here you can change the planets and the initial conditions along with executing the scripts"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.5, rely=0.2, anchor="center")

# fontStyle = tkFont.Font(family="Lucida Grande", size=25)
# text_intro = "Planets"
# label = tk.Label(root, text=text_intro, font=fontStyle)
# label.place(relx=0.25, rely=0.28)

fontStyle = font.Font(family="Lucida Grande", size=25)
text_intro = "Universal Constants"
label = tk.Label(root, text=text_intro, font=fontStyle)
label.place(relx=0.75, rely=0.30, anchor="center")

fontStyle = font.Font(family="Lucida Grande", size=12)
text_intro = "Gravitational Constant (G)"
G_constant = tk.Label(root, text=text_intro, font=fontStyle)
G_constant.place(relx=0.68, rely=0.35, anchor="center")

fontStyle = font.Font(family="Lucida Grande", size=25)
text_intro = "Select Your Planets"
planetslabel = tk.Label(root, text=text_intro, font=fontStyle)
planetslabel.place(relx=0.25, rely=0.3, anchor="center")

lb = tk.Listbox(root, selectmode = "multiple")
lb.place(relx=0.25, rely=0.5, anchor="center")

x =["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

for item in range(len(x)):
	lb.insert(tk.END, x[item])
	lb.itemconfig(item, bg="#ffffff")

tk.Button(root, text="Confirm Planets", command=confirmSelected).place(relx=0.20, rely=0.6)

app = MyApp(root)
root.mainloop()

"""if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = MyApp(root)
    root.mainloop()"""
