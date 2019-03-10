# This script needs to be run in the virtual env i.e.
# source venv/bin/activate
# python populate_db/populate_db.py

import sys
import os

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "app"))
sys.path.append(app_path)

from main import db
from models import Database, Table, Column

import json
import os


if __name__ == "__main__":

    # db.drop_all() #TODO probably make this optional!!
    # db.session.commit()
    os.remove("app/app.db")
    db.create_all()

    subfolders = [f.path for f in os.scandir("populate_db/metadata_folders/") if f.is_dir() ]
    for subfolder in subfolders:
        with open(os.path.join(subfolder, "database.json")) as f:
            dbjson = json.load(f)

        with open(os.path.join(subfolder, "_metadata_source.json")) as f:
            metadata_source_json = json.load(f)

        base_url = metadata_source_json["git_repo"].replace("git@github.com:", "https://github.com/").replace(".git", "")

        if metadata_source_json["branch"]:
            branch = metadata_source_json["branch"]
        else:
            branch = "master"

        base_hyperlink = f"{base_url}/tree/{branch}/{metadata_source_json['path_to_meta']}"


        d = Database()
        d.db_name = dbjson["name"]
        d.db_desc = dbjson["description"]
        d.db_metaloc = f"{base_hyperlink}/database.json"

        path = os.path.join(dbjson["bucket"], dbjson["base_folder"])
        d.db_loc = f"s3://{path}"

        db.session.add(d)
        db.session.commit()

        files = os.listdir(subfolder)
        files = [f for f in files if f != "database.json"]
        files = [f for f in files if f != "_metadata_source.json"]
        table_files = [f for f in files if f.endswith(".json")]
        for table_file in table_files:
            with open(os.path.join(subfolder, table_file)) as f:
                tbljson = json.load(f)

            t = Table()
            t.tbl_name = tbljson["name"]
            t.tbl_desc = tbljson["description"]
            t.tbl_loc = os.path.join(d.db_loc, tbljson["location"])
            t.tbl_metaloc = f"{base_hyperlink}/{table_file}"

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
    sql = """CREATE VIRTUAL TABLE fulltextsearch
           USING fts5(db_id, tbl_id, clm_id, db_name, db_desc, tbl_name, tbl_desc, clm_name, clm_desc);
           """

    result = db.engine.execute(sql)

    sql = """INSERT INTO fulltextsearch
                    (db_id, tbl_id, clm_id, db_name, db_desc, tbl_name, tbl_desc, clm_name, clm_desc)
             SELECT  db_id, tbl_id, clm_id, db_name, db_desc, tbl_name, tbl_desc, clm_name, clm_desc from joined
    """

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




