# 檔案名稱為: ConnectPostgreSQL.py
import psycopg2


class PostgresBaseManager:

    def __init__(self):

        self.database = 'd8q79pjsluumf9'
        self.user = 'yuacqtdojxgkqv'
        self.password = '28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8'
        self.host = 'ec2-3-225-110-188.compute-1.amazonaws.com'
        self.port = '5432'
        self.conn = self.connectServerPostgresDb()

    def connectServerPostgresDb(self):
        """
        :return: 連接 Heroku Postgres SQL 認證用
        """
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        return conn

    def closePostgresConnection(self):
        """
        :return: 關閉資料庫連線使用
        """
        self.conn.close()

    def runServerPostgresDb(self):
        """
        :return: 測試是否可以連線到 Heroku Postgres SQL
        """
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        results = cur.fetchall()
        print("Database version : {0} ".format(results))
        self.conn.commit()
        cur.close()


if __name__ == '__main__':
    postgres_manager = PostgresBaseManager()
    postgres_manager.runServerPostgresDb()
    postgres_manager.closePostgresConnection()