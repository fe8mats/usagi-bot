import sqlite3
import os
import re

# Original small ORM inspired by Laravel Eloquent
DB_FILE = os.getenv('DB_FILE')

class Connection:
    dbname = ""
    conn = None
    cur = None
    current_table = ""
    current_select = []
    current_where = []
    current_join = []
    current_limit = None
    current_orderby = None
    current_groupby = None
    current_offset = None
    current_ph = {}
    genereted_sql = None

    def __init__(self) -> None:
        self.dbname = DB_FILE
        self.conn = sqlite3.connect(self.dbname)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.resetCondition()

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def table(self, table: str):
        self.current_table = table
        return self

    def select(self, *args):
        self.current_select = args
        return self
    
    def join(self, table: str, first: str, operator: str, second: str):
        self.current_join.append[table, first, operator, second]
        return self

    def where(self, *args):
        if len(args) == 2:
            self.current_where.append([args[0], "=", args[1]])
        elif len(args) == 3:
            self.current_where.append([args[0], args[1], args[2]])
        return self
    
    def limit(self, limit: int):
        self.current_limit = limit
        return self

    def groupBy(self, groupby: str):
        self.current_limit = groupby
        return self
    
    def orderBy(self, orderby: str):
        self.current_limit = orderby
        return self
    
    def offset(self, offset: int):
        self.current_offset = offset
        return self
    
    def get(self):
        result = None
        column = ','.join(self.current_select)
        if column == "":
            column = "*"
        sql = f"SELECT {column} FROM {self.current_table}"
        if len(self.current_join) > 0:
            joins = ""
            for join in self.current_join:
                joins += f" LEFT JOIN {join[0]} ON {join[1]} {join[2]} {join[3]}"
            sql += joins
        if len(self.current_where) > 0:
            cond = ""
            for i in range(len(self.current_where)):
                where = self.current_where[i]
                call_type = "AND"
                if i == 0:
                    call_type = "WHERE"
                cond += f" {call_type} {where[0]} {where[1]} '{where[2]}'"
            sql += cond

        if self.current_groupby is not None:
            sql += f" GROUP BY {self.current_groupby}"
        if self.current_orderby is not None:
            sql += f" ORDER BY {self.current_orderby}"
        if self.current_limit is not None:
            sql += f" LIMIT {self.current_limit}"
        if self.current_offset is not None:
            sql += f" OFFSET {self.current_offset}"

        sql += ";"
        self.genereted_sql = sql
        try:
            print(sql)
            self.cur.execute(sql, self.current_ph)
            result = [dict(row) for row in self.cur.fetchall()]
        except Exception as e:
            print(e)
        finally:
            self.resetCondition()
        return result
    
    def first(self):
        self.current_limit = 1
        result = self.get()
        if len(result) > 0:
            return result[0]
        else:
            return None
        
    def insert(self, data: dict):
        result = False
        column_list = data.keys()
        column = ','.join(column_list)
        values_list = []
        for c in column_list:
            values_list += [f":{c}"]
        values = ','.join(values_list)
        sql = f"INSERT INTO {self.current_table}({column}) VALUES({values})"
        try:
            print(sql)
            self.cur.execute(sql, data)
            result = True
        except Exception as e:
            print(e)
        finally:
            self.resetCondition()
        return result
    
    def update(self, data: dict):
        result = False
        column_list = data.keys()
        set_list = []
        for c in column_list:
            set_list.append(f"{c} = :{c}")
        set_data = ','.join(set_list)
        sql = f"UPDATE {self.current_table} SET {set_data}"
        if len(self.current_join) > 0:
            joins = ""
            for join in self.current_join:
                joins += f" LEFT JOIN {join[0]} ON {join[1]} {join[2]} {join[3]}"
            sql += joins
        if len(self.current_where) > 0:
            cond = ""
            ph_where = {}
            for i in range(len(self.current_where)):
                where = self.current_where[i]
                call_type = "AND"
                if i == 0:
                    call_type = "WHERE"
                cond += f" {call_type} {where[0]} {where[1]} :where_{i}"
                ph_where[f"where_{i}"] = where[2]

            sql += cond
            data.update(ph_where)
        if self.current_groupby is not None:
            sql += f" GROUP BY {self.current_groupby}"
        if self.current_orderby is not None:
            sql += f" ORDER BY {self.current_orderby}"
        if self.current_limit is not None:
            sql += f" LIMIT {self.current_limit}"
        if self.current_offset is not None:
            sql += f" OFFSET {self.current_offset}"
        sql += ";"
        self.genereted_sql = sql
        try:
            print(sql)
            self.cur.execute(sql, data)
            result = True
        except Exception as e:
            print(e)
        finally:
            self.resetCondition()
        return result
    
    def getGeneretedSQL(self):
        return self.genereted_sql
    
    def commit(self):
        self.conn.commit()

    def disconnect(self):
        self.conn.close()

    def execute(self, sql, placeholder = None):
        result = False
        try:
            if placeholder is None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, placeholder)
            result = True
        except Exception as e:
            print(e)
        return result
    
    def resetCondition(self):
        self.current_table = ""
        self.current_select = []
        self.current_where = []
        self.current_join = []
        self.current_limit = None
        self.current_orderby = None
        self.current_groupby = None
        self.current_offset = None
        self.current_ph = {}
