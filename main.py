import tkinter as tk
import time

# This is a program that allows users to track their study time using the Pomodoro technique


class App(tk.Tk):

    # Initialize main application window
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Pomodoro App")


        # Create a container frame for the two frames
        container = tk.Frame(self)
        container.pack(fill="both", expand = True)

        # Place clock and session data in container frame
        clock = Clock(container, controller=self)
        sessionData = SessionData(container, controller=self)
        timer = tk.Frame(clock, height=150, width=250)
        timer.place(in_ = clock, anchor="center", relx=.5, rely=.5)





        # Configure grid to make columns resizable
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Place Clock and SessionData frames inside container
        clock.grid(row=0, column=0, sticky="nsew")
        sessionData.grid(row=0, column=1, sticky="nsew")


        # Place labels for Clock, SessionData, and Timer frames
        label = tk.Label(clock, text ="Study Timer", bg = "black",fg ="white", font = ("Terminal",20))
        label.pack(padx=5, pady=5)
        self.timerLabel = tk.Label(timer, text = "25:00", bg ="black", fg ="white", font = ("Terminal", 30))
        self.timerLabel.pack()
        sessionLabel = tk.Label(sessionData, text ="Session Data", bg ="black", fg="white", font = ("Terminal", 20))
        sessionLabel.pack()


        # calls the Timer class
        self.timer = Timer(self.timerLabel)

        # Button to start the timer
        button1 = tk.Button(clock, text="START", bg="black", fg="white", font=("Terminal", 14), command=self.timer.startTimer)
        button1.pack(side="bottom", padx=20, pady=140)
        button2 = tk.Button(clock, text="RESET", bg="black", fg ="white", font=("Terminal", 14), command=self.timer.resetTimer)
        button2.pack(side="bottom", padx=20, pady=80)


# Timer class that starts and resets the timer
class Timer:

    # initializes the timer class
    def __init__(self, label):
        self.label = label
        self.isRunning = False



    #starts the timer
    def startTimer(self):
        if not self.isRunning:
            self.isRunning = True
            self.endTime = time.time() + (25 * 60)
            self.updateTimer()

    #resets the timer
    def resetTimer(self):
        if self.isRunning:
            self.isRunning = False


    # updates the timer as it is running
    def updateTimer(self):
        if self.isRunning:
            remaining_time = int(self.endTime - time.time())
            if remaining_time <= 0:
                self.label.config(text="00:00")
                self.isRunning = False
            else:
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                self.label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.label.after(1000, self.updateTimer)








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




















