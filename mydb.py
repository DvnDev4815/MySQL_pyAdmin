import mysql.connector

class dataBase:
    def __init__(self)-> None:
        pass

    def _validateData(self, username : str, password : str) -> bool:
        self.username = username
        self.passw = password

        if (self.username == ""):
            return False

        try:
            self.conexion = mysql.connector.connect(
                password = self.passw,
                user = self.username,
                host = "localhost",
            )

            self.cur = self.conexion.cursor()

            return True

        except mysql.connector.Error as err:
            print(err)

            return False

    def _getDataBases(self):
        self.cur.execute("SHOW DATABASES")
        self.result = self.cur.fetchall()
        self.databases = []

        for database in self.result:
            for i in database:
                self.databases.append(i)

        return self.databases

    def _selectDataBase(self, database:str):
        try:
            self.cur.execute(f"USE {database}")
            return True
        except mysql.connector.errors.ProgrammingError as err:
            return False

    def _getUsername(self):
        self.cur.execute("SELECT USER()")
        self.result = self.cur.fetchall()

        return self.result[0][0]

    def _getTablesData(self):
        self.cur.execute("SHOW TABLES")
        self.tables = []

        for row in self.cur.fetchall():
            for table in row:
                self.tables.append(table)

        return self.tables
    
    def _getRowsFrom(self, table : str, limit : int):
        self.cur.execute(f"SELECT * FROM {table} LIMIT {limit}")
        return self.cur.fetchall()

    def _getColumnsFrom(self, table : str):
        self.cur.execute(f"SHOW COLUMNS FROM {table}")
        return self.cur.fetchall()

    def _logOut(self):
        self.username = ""
        self.passw = ""

if __name__ == "__main__":
    debug = dataBase()
    debug._validateData("dvndev4815", "")

    print(debug._getDataBases())