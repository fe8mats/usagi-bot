import miniquent
import datetime
import os

class Information:
    id = None
    slug = ""
    title = ""
    host = ""
    port = ""
    password = ""
    message = None
    manager = ""

    def __init__(self):
        pass

    def setData(self, slug, title, host, port, password, message, manager):
        self.slug = slug
        self.title = title
        self.host = host
        self.port = port
        self.password = password
        self.manager = manager
        if message is None:
            self.message = ""
        else:
            self.message = message

    def getCurrentData(self):
        data = {
            "slug": self.slug,
            "title": self.title,
            "host": self.host,
            "port": self.port,
            "password": self.password,
            "message": self.message,
            "manager": self.manager
        }
        return data

    def insert(self):
        dt_now = datetime.datetime.now()
        db = miniquent.Connection()
        insert_data = self.getCurrentData()
        slug = insert_data["slug"]
        exists = db.table("servers").where("slug", slug).where("delete_flg", 0).first()
        if exists is not None:
             print("exists")
             db.disconnect()
             return False
        insert_data["create_at"] = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        insert_result = db.table("servers").insert(insert_data)
        if insert_result is True:
            db.commit()
            db.disconnect()
            return True
        else:
            db.disconnect()
            return False
        
    def getList(self):
        db = miniquent.Connection()
        data = db.table("servers").where("delete_flg", 0).get()
        db.disconnect()
        return data
    
    def get(self, slug):
        db = miniquent.Connection()
        data = db.table("servers").where('slug', slug).where("delete_flg", 0).first()
        print(data)
        db.disconnect()
        return data
    
    def remove(self, slug):
        try:
            dt_now = datetime.datetime.now()
            db = miniquent.Connection()
            query = db.table('servers').where('slug', slug).update({"delete_flg": 1, "deleted_at": dt_now.strftime('%Y-%m-%d %H:%M:%S')})
            if query is False:
                raise Exception
            db.commit()
            db.disconnect()
            return True
        except Exception as e:
            print(e)
            db.disconnect()
            return False