import sqlite3
class Contact:
    DB_FILENAME = 'contacts.db'
    def execute_db_query(self,query,parameters=()):

        with sqlite3.connect(self.DB_FILENAME) as conn:
            print(conn)
            print('you have successfully connect to the Database')
            cursor = conn.cursor()
            query_result = cursor.execute(query,parameters)
            conn.commit()
        return query_result
