import pyodbc
from Function.User_file import User
class UserDao:
    def check_login(self,user:User):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI;DATABASE=SalesPhone;Trusted_Connection=yes')
        cursor = conn.cursor()
        cursor.execute("EXEC CheckLogin @Username=?, @Password=?", (user._username, user._password))
        login_success = cursor.fetchone()[0]  
        conn.close()
        return login_success
    def get_full_name(self,comment):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI;DATABASE=SalesPhone;Trusted_Connection=yes')
        cursor = conn.cursor()
        cursor.execute(f"select full_name From users join comments on comments.user_id=users.id where comment = N'{comment}'")
        user_row = cursor.fetchone()
        conn.close()
        return user_row[0] if user_row else None
    def get_user_id(self,user:User):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI;DATABASE=SalesPhone;Trusted_Connection=yes')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM users WHERE username = '{user._username}'")
        user_row = cursor.fetchone()
        conn.close()
        return user_row[0] if user_row else None
    def get_comment_by_user(self):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI;DATABASE=SalesPhone;Trusted_Connection=yes')
        cursor = conn.cursor()
        cursor.execute("SELECT comment FROM comments")
        comments = cursor.fetchall()
        return comments
    def insert_comment(self,user:User,comment):
        user_id = self.get_user_id(user) 
        if user_id:
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI;DATABASE=SalesPhone;Trusted_Connection=yes')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO comments (user_id, comment) VALUES (?, ?)",(user_id,comment))
            conn.commit()  
            print("Comment inserted successfully.")
            conn.close()
        else:
            print("User not found.")




    