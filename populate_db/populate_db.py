import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from app.models import Database, Table, Column
from app import db
import json


if __name__ == "__main__":

    # db.drop_all() #TODO probably make this optional!!
    os.remove("app.db")
    db.session.commit()
    db.create_all()

    subfolders = [f.path for f in os.scandir("populate_db/metadata_folders/") if f.is_dir() ]
    for subfolder in subfolders:
        with open(os.path.join(subfolder, "database.json")) as f:
            dbjson = json.load(f)

        d = Database()
        d.db_name = dbjson["name"]
        d.db_desc = dbjson["description"]

        db.session.add(d)
        db.session.commit()

        files = os.listdir(subfolder)
        files = [f for f in files if f != "database.json"]
        table_files = [f for f in files if f.endswith(".json")]
        for table_file in table_files:
            with open(os.path.join(subfolder, table_file)) as f:
                tbljson = json.load(f)

            t = Table()
            t.tbl_name = tbljson["name"]
            t.tbl_desc = tbljson["description"]
            t.databases = d
            db.session.add(t)
            db.session.commit()

            for column in tbljson["columns"]:
                c = Column()
                c.clm_desc = column["description"]
                c.clm_name = column["name"]

                c.tables = t

                db.session.add(c)
                db.session.commit()

    # Get column
    sql = """
    CREATE VIEW joined as
    select * from databases as db
                left join tables as tbl
                on db.db_id= tbl.db_id
                left join columns as cl
                on tbl.tbl_id = cl.tbl_id

    """
    result = db.engine.execute(sql)

    # Create FTS5 table
    sql = "CREATE VIRTUAL TABLE fulltextsearch USING fts5(db_name, db_desc, tbl_name, tbl_desc, clm_name, clm_desc);"

    result = db.engine.execute(sql)

    sql = "INSERT INTO fulltextsearch (db_name, db_desc, tbl_name, tbl_desc, clm_name, clm_desc) SELECT  db_name, db_desc, tbl_name, tbl_desc, clm_name, clm_desc from joined"

    db.engine.execute(sql)

    sql = "pragma compile_options"

    rows = db.engine.execute(sql)

    # cur.execute(sql)
    # rows = cur.fetchall()

    print(rows.fetchall())

    sql = "SELECT * FROM fulltextsearch WHERE fulltextsearch MATCH 'sensor' ORDER BY rank;"
    rows = db.engine.execute(sql)
    # cur.execute(sql)
    # rows = cur.fetchall()
    print(rows.cursor.description)
    # print(rows.fetchall())




