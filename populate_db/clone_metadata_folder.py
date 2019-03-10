from git import Repo, Git
import os
import json
from shutil import rmtree

def clone_metadata_folder(git_repo, path_to_meta, branch=None):

    temp_dir = "_temp_"
    repo_root_dir = "temprepo"


    if len(temp_dir)>3:  #Rubbish protection against deleting your whole computer
        try:
            rmtree(temp_dir)
        except FileNotFoundError:
            pass

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    Git(temp_dir).clone(git_repo, repo_root_dir)
    repo = Repo(os.path.join(temp_dir, repo_root_dir))


    if branch:
        repo.create_head(branch, repo.remotes.origin.refs[branch])  # create local branch "master" from remote "master"
        repo.heads[branch].checkout()



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

    # Include a file that contains information about where the files were cloned from

    meta_location = {"git_repo": git_repo, "path_to_meta": path_to_meta, "branch": branch}
    with open(os.path.join(to_dir, "_metadata_source.json"), "w") as f:
        json.dump(meta_location, f)

    ## Clean up

    if len(temp_dir)>3:  #Rubbish protection against deleting your whole computer
        rmtree(temp_dir)



if __name__ == "__main__":
    # Each item is (git repo, relative path, OPTIONAL branch if not default)
    clone_list = []
    clone_list.append(("git@github.com:moj-analytical-services/airflow-occupeye-scraper.git", "glue/meta_data/occupeye_db"))
    clone_list.append(("git@github.com:moj-analytical-services/airflow_natstats_postcodes.git", "meta_data/curated"))
    clone_list.append(("git@github.com:moj-analytical-services/airflow_get_index_of_multiple_deprivation.git", "meta_data"))
    clone_list.append(("git@github.com:moj-analytical-services/airflow-build-addressbase-premium.git", "meta_data"))

    clone_list.append(("git@github.com:moj-analytical-services/crest_engineering_draft.git", "v1/meta_data/crest"))
    clone_list.append(("git@github.com:moj-analytical-services/crest_engineering_draft.git", "v1/meta_data/lookups"))
    clone_list.append(("git@github.com:moj-analytical-services/airflow-magistrates-data-engineering.git", "meta_data/curated"))
    clone_list.append(("git@github.com:moj-analytical-services/airflow-nomis-transform.git", "meta_data/curated", "alpha"))
    # clone_list.append(("git@github.com:moj-analytical-services/airflow-nomis-transform.git", "meta_data/denormalised", "alpha")) #no database.json
    clone_list.append(("git@github.com:moj-analytical-services/SOP_engineering_draft.git", "v1/meta_data/sop_transformed", "sldedupe"))

    for c in clone_list:
        if len(c) == 3:
            clone_metadata_folder(c[0], c[1], c[2])
        else:
            clone_metadata_folder(c[0], c[1])


