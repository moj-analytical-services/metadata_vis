from git import Repo, Git
import os
import json
from shutil import rmtree

def clone_metadata_folder(git_repo, path_to_meta):

    temp_dir = "_temp_"
    repo_root_dir = "temprepo"

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    Git(temp_dir).clone(git_repo, repo_root_dir)

    path_to_db_meta = os.path.join(temp_dir, repo_root_dir, path_to_meta)
    files = os.listdir(path_to_db_meta)


    db_file = os.path.join(path_to_db_meta, "database.json")

    with open(db_file) as f:
        db = json.load(f)
    db_name = db["name"]

    from distutils.dir_util import copy_tree

    from_dir = path_to_db_meta
    to_dir = "populate_db/metadata_folders/{}".format(db_name)

    copy_tree(from_dir, to_dir)

    ## Clean up

    if len(temp_dir)>3:  #Rubbish protection against deleting your whole computer by setting
        rmtree(temp_dir)



if __name__ == "__main__":
    clone_list = []
    clone_list.append(("git@github.com:moj-analytical-services/airflow-occupeye-scraper.git", "glue/meta_data/occupeye_db"))
    # clone_list.append(("git@github.com:moj-analytical-services/airflow-nomis-transform.git", "meta_data/curated"))
    clone_list.append(("git@github.com:moj-analytical-services/airflow_natstats_postcodes.git", "meta_data/curated"))

    for c in clone_list:
        clone_metadata_folder(c[0], c[1])
