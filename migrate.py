import miniquent
import os

def start():
    db = miniquent.Connection()
    table_files = os.listdir("sql")
    table_list = db.table("sqlite_master").select("name").where("type", "table").get()
    if table_list is not None:
        tables = []
        for tb in table_list:
            tables.append(tb["name"])
        for table_file in table_files:
            target = os.path.splitext(table_file)[0]
            if target not in tables:
                try:
                    f = open(f"sql/{table_file}", 'r', encoding='UTF-8')
                    data = f.read()
                    db.execute(data)
                    db.commit()
                    print(f"worked {target}")
                except Exception as e:
                    print(e)
    del db