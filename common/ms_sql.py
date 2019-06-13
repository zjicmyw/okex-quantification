import pymssql
import json

with open("database/accounts.json", 'r') as load_f:
    load_dict = json.load(load_f)
    host1 = load_dict['database']['host']
    user1 = load_dict['database']['user']
    pwd1 = load_dict['database']['pwd']
    db1 = load_dict['database']['db']


class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host1
        self.user = user1
        self.pwd = pwd1
        self.db = db1

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
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
