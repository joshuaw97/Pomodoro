import tkinter as tk

# This is a program that allows users to track their study time using the Pomodoro technique


class App(tk.Tk):

    # Initialize main application window
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Pomodoro App")


        # Create a container frame for the two frames
        container = tk.Frame(self)
        container.pack(fill = "both", expand = True)

        # Place clock and session data in container frame
        clock = Clock(container, controller = self)
        sessionData = SessionData(container, controller = self)
        timer = tk.Frame(clock, height=150, width=250)
        timer.place(in_ = clock, anchor="center", relx=.5, rely=.5)





        # Configure grid to make columns resizable
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Place Clock and SessionData frames inside container
        clock.grid(row=0, column=0, sticky="nsew")
        sessionData.grid(row=0, column=1, sticky="nsew")

        # Place labels for Clock and SessionData frames
        label = tk.Label(clock, text ="Study Timer", bg = "black",fg ="white", font = ("Terminal",20))
        label.pack(padx = 5, pady = 5)
        sessionLabel = tk.Label(sessionData, text ="Session Data", bg ="black", fg="white", font = ("Terminal", 20))
        sessionLabel.pack(padx= 5, pady = 5)

        # Button to start timer, placed at bottom of Clock frame
        button1 = tk.Button(clock, text = "START", font = ("Terminal", 14))
        button1.pack(side ="bottom", padx=20, pady=140)



# initializes frame containing the timer
class Clock(tk.Frame):
    # initializes Clock frame as a child of parent container
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="forest green")


# initializes frame containing session data
class SessionData(tk.Frame):
    # initializes Session Data frame as a child of container frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="dark goldenrod")

app = App()
app.minsize(750, 500)
app.mainloop()




















