import tkinter as tk
import time
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.studyHours = tk.Label()


        graph = tk.Frame(sessionData, height = 150, width = 200)
        graph.place(in_= sessionData, anchor="center", relx=.5, rely=.5)

        self.fig, self.ax = plt.subplots(figsize=(3, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph)
        self.canvas.get_tk_widget().pack()

        # Update the graph initially
        self.updateGraph()









        # add timer frame to clock frame
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
        label = tk.Label(clock, text="Study Timer", bg="black", fg="white", font = ("Terminal",20))
        label.pack(padx=5, pady=5)
        self.timerLabel = tk.Label(timer, text="25:00", bg ="black", fg="white", font=("Terminal", 30))
        self.timerLabel.pack()
        sessionLabel = tk.Label(sessionData, text="Session Data", bg="black", fg="white", font=("Terminal", 20))
        sessionLabel.pack()
        self.totalHoursLabel = tk.Label(sessionData, text = "Total hours studied this week:",
                                         bg="black", fg="white", font=("Terminal", 12))
        self.totalHoursLabel.pack()


        self.updateHours()



        # calls the Timer class
        self.timer = Timer(self.timerLabel, self)

        button2 = tk.Button(clock, text="RESET", bg="black", fg="white", font=("Terminal", 14), command=self.timer.resetTimer)
        button2.pack(side="bottom")
        button1 = tk.Button(clock, text="START", bg="black", fg="white", font=("Terminal", 14), command=self.timer.startTimer)
        button1.pack(side ="bottom")

    def updateGraph(self):
        # Initialize hours_studied with zeros for all days of the week
        hoursStudied = [0] * 7

        # Retrieve data from the database and update hours_studied
        with Database('sessionDatabase.sqlite') as db:
            sessionsByDay = db.getSessionByDayOfWeek()
            for day, sessionCount in sessionsByDay:
                hoursStudied[int(day)] = sessionCount * 25 / 60

        # Clear the previous data and update the graph
        self.ax.clear()
        xData = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        self.ax.bar(xData, hoursStudied)
        self.ax.set_title("Weekly Study Hours")
        self.ax.set_yticks(range(1, 11))
        self.canvas.draw()


    def updateHours(self):
        with Database('sessionDatabase.sqlite') as db:
            db.execute(f"SELECT COUNT(*) FROM date")
            totalSessions = db.fetchone()[0]
        self.totalHoursLabel.config(text=f"Total Hours: {totalSessions * 30 / 60}")











# Timer class that starts and resets the timer
class Timer:

    # initializes the timer class
    def __init__(self, label, appInstance):
        self.label = label
        self.isRunning = False
        self.appInstance = appInstance




    #starts the timer
    def startTimer(self):
        if not self.isRunning:
            self.isRunning = True
            self.endTime = time.time() + (60 * 25)
            self.updateTimer()

    #resets the timer
    def resetTimer(self):
        if self.isRunning:
            self.isRunning = False
            self.updateTimer()


    # updates the timer as it is running
    def updateTimer(self):
        if self.isRunning:
            remaining_time = int(self.endTime - time.time())
            if remaining_time <= 0:
                self.label.config(text="00:00")
                self.appInstance.updateWeeklyHours()
    # calls sessionComplete function when session is over
                self.sessionComplete(complete = True)
                self.isRunning = False
            else:
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                self.label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.label.after(1000, self.updateTimer)
        if not self.isRunning:
            self.label.config(text="25:00")

    # Calls insert time function if session is complete
    def sessionComplete(self, complete):
        if complete:
            self.insertTime()


    # Insert time into database when a session is completed
    def insertTime(self):
        with Database('sessionDatabase.sqlite') as db:
            db.execute('CREATE TABLE IF NOT EXISTS date(date_completed TIMESTAMP)')
            db.execute('INSERT INTO date (date_completed) VALUES (current_date)')
            comments = db.query('SELECT * FROM date')

            print(comments)
        self.appInstance.updateGraph()



        







class Clock(tk.Frame):
    # initializes Clock frame as a child of container frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="forest green")





class SessionData(tk.Frame):
    # initializes Session Data frame as a child of container frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="saddle brown")







class Database:
    # Initializes the Database class with specified name of the SQLite database file
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()
        self.table = self.createTable()

    # Enables the usage of 'with' statement to ensure proper closing of the database connection
    def __enter__(self):
        return self

    # Closes the database connection when the 'with' statement is exited
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def createTable(self):
        self.execute('CREATE TABLE IF NOT EXISTS date(date_completed TIMESTAMP)')


    def getSessionByDayOfWeek(self):
        sql = """
            SELECT strftime('%w', date_completed) AS day, COUNT(*) AS sessions
            FROM date
            GROUP BY day
        """
        self.execute(sql)
        return self.fetchall()

    # Property method to access the database connection externally
    @property
    def connection(self):
        return self._conn

    # Property method to access the database cursor externally
    @property
    def cursor(self):
        return self._cursor

    # Commits the changes made to the database
    def commit(self):
        self.connection.commit()

    # Closes the database connection
    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    # Executes an SQL query with optional parameters
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    # Fetches all the rows returned by the most recent query
    def fetchall(self):
        return self.cursor.fetchall()

    # Fetches the next row returned by the most recent query
    def fetchone(self):
        return self.cursor.fetchone()

    # Executes an SQL query and returns the result as a list of rows
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()




































app = App()
app.minsize(750, 500)
app.mainloop()




















