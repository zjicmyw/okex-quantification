import pymssql
import json

with open("json/accounts.json", 'r', encoding='UTF-8') as load_f:
    database_info = json.load(load_f)['database']
    host = database_info['host']
    user = database_info['user']
    pwd = database_info['pwd']
    db = database_info['db']
    port = database_info['port']


class MSSQL:
    def __init__(self):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQueryALL(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecQueryOne(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchone()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
