import tkinter as tk
from tkinter import font
import os


########################################################################
class n_body_app(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Main frame")
        self.frame = tk.Frame(parent)
        self.frame.pack()

        close_btn = tk.Button(self.frame, text="Close Application", command=self.closeApplication)
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

        x =["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "AC1", "AC2"]

        for item in range(len(x)):
        	lb.insert(tk.END, x[item])
        	lb.itemconfig(item, bg="#ffffff")

        tk.Button(self.root, text="Confirm Planets", command=self.confirmSelected).place(relx=0.205, rely=0.62)

        e = tk.Entry(self.root, width=10, borderwidth=1)
        e.place(relx=0.80, rely=0.35, anchor="center")
        e.insert(0, "6.6743015")
        e.focus_set()

        G = 24
        G_button = tk.Button(self.root,text='Change Constants',command=self.changeG(e,G))
        G_button.place(relx=0.75, rely=0.4, anchor="center")

        Executefile_btn = tk.Button(self.root, text="Run rando file", command=self.runfile)
        Executefile_btn.place(relx=0.5, rely=0.9)


        self.FullScreenApp(parent)

    #----------------------------------------------------------------------
    def hide(self):
        """"""
        self.root.withdraw()

    #----------------------------------------------------------------------
    def openFrame(self):
        """"""
        self.hide()
        otherFrame = tk.Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("otherFrame")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = tk.Button(otherFrame, text="Close", command=handler)
        btn.pack()
        
        """ -- How to utilise
        open_btn = tk.Button(self.frame, text="Open Frame",
                             command=self.openFrame)
        open_btn.pack()
        """
    #----------------------------------------------------------------------
    def onCloseOtherFrame(self, otherFrame):
        """"""
        otherFrame.destroy()
        self.show()

    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()

    #----------------------------------------------------------------------

    def closeApplication(self):
        """"""
        self.root.destroy()

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


    def runfile(self):
        os.system('python SlimSimulation-K1=K2=0.py')

    def set_text(self, text):
        self.e.delete(0,tk.END)
        self.e.insert(0,text)
        return

    def changeG(self,e,G):
        #global G
        G = e.get()
        print("G is changed to:", G)
        # text.insert(INSERT, G)
# GUI


#----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = n_body_app(root)
    root.mainloop()


