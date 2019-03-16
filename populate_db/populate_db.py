# This script needs to be run in the virtual env i.e.
# source venv/bin/activate
# python populate_db/populate_db.py



import sys
import os
import requests
from requests.auth import HTTPBasicAuth

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "app"))
sys.path.append(app_path)



from main import db
from models import Database, Table, Column, Enum, AccessRight
from db_secrets import DJANGO_PASSWORD, DJANGO_USERNAME

import json
import os


def create_accessrights_table():

    s3buckets_results = []
    nextpage = True
    url = 'https://cpanelapi-master.services.alpha.mojanalytics.xyz/s3buckets/'
    while nextpage:
        r = requests.get(url, auth=HTTPBasicAuth(DJANGO_USERNAME, DJANGO_PASSWORD))
        s3buckets = json.loads(r.text)
        s3buckets_results.extend(s3buckets["results"])
        url = s3buckets['next']
        if not s3buckets['next']:
            nextpage = False

    for r in s3buckets_results:
        users = r["users3buckets"]
        for user in users:

            ar = AccessRight()

            ar.ar_s3bucket = r["arn"].replace("arn:aws:s3:::", "")
            ar.ar_git_username = user["user"]["username"]
            ar.ar_email = user["user"]["email"]
            ar.ar_is_admin = user["is_admin"]

            dbs = Database.query.filter(
                Database.db_s3bucket == ar.ar_s3bucket).first()


            ar.databases = dbs

            db.session.add(ar)
            db.session.commit()

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
        d.db_s3bucket = dbjson["bucket"]

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
            t.tbl_datatype = tbljson["data_format"]
            if "partitions" in tbljson:
                t.tbl_partitions = json.dumps(tbljson["partitions"])
            else:
                t.tbl_partitions = None

            t.databases = d
            db.session.add(t)
            db.session.commit()

            for column in tbljson["columns"]:
                c = Column()
                c.clm_desc = column["description"]
                c.clm_name = column["name"]
                c.clm_datatype = column["type"]
                if "partitions" in tbljson:
                    c.clm_is_parition = column["name"] in tbljson["partitions"]
                else:
                    c.clm_is_parition = False

                if "pattern" in column:
                    c.clm_pattern = column["pattern"]

                c.tables = t

                db.session.add(c)
                db.session.commit()

                if "enum" in column:
                    for val in column["enum"]:
                        e = Enum()
                        e.enum_value = val
                        e.columns = c
                        db.session.add(e)
                        db.session.commit()

    create_accessrights_table()

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





