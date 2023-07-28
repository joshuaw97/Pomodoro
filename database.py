import sqlite3

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


