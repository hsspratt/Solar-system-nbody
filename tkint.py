import tkinter as tk

# --- classes ---


class Game:

    def __init__(self):
        self.root = tk.Tk()

        self.g_textbox = tk.StringVar()

        self.G_entry = tk.Entry(self.root, textvariable=self.g_textbox)
        self.G_entry.pack()
        
        self.time_textbox = tk.StringVar()

        self.time_entry = tk.Entry(self.root, textvariable=self.g_textbox)
        self.time_entry.pack()

        self.submit = tk.Button(
            self.root, text="Submit", command=self.get_input)
        self.submit.pack()

    def run(self):
        self.root.mainloop()

    def inputs(self, G, time):
        # do something with text
        print(G)
        print(time)

        # and return something
        return 'a', 'b', 'c'

    def get_input(self):

        G = self.g_textbox.get()
        time = self.time_textbox.get()

        if G&time:  # check if text is not empty
            self.g_textbox.set('')  # remove text from entry
            self.time_textbox.set('')
            #G_entry.delete(0, 'end') # remove text from entry
            self.action_input, self.extra_input, self.texts = self.inputs(G,time)

# --- functions ---

# empty


# --- main ---

app = Game()
app.run()
