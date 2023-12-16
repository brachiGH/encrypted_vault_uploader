vault_path = ''
backup_path = ''
refresh_time = ''
master_pass = ''
folder_id = ''


def compare_databases(old_db_file, new_db_file):
    """
    Compare two databases.csv files and print paths for new, modified, and deleted files.
    """
    has_been_any_changes = False
    global vault_path
    global backup_path
    global master_pass


    create_empty_csv(old_db_file)
    old_data = read_csv(old_db_file)
    new_data = read_csv(new_db_file)

    old_paths = set(item[0] for item in old_data)
    new_paths = set(item[0] for item in new_data)

    # Paths for new files
    new_files = new_paths - old_paths
    for path in new_files:
        has_been_any_changes = True
        copy_file_with_folders(path, replace_part(path, vault_path, backup_path))

    # Paths for modified files
    common_paths = old_paths.intersection(new_paths)
    modified_files = [path for path in common_paths if get_modification_time(path, old_data) != get_modification_time(path, new_data)]
    for path in modified_files:
        has_been_any_changes = True
        copy_file_with_folders(path, replace_part(path, vault_path, backup_path))

    # Paths for deleted files
    deleted_files = old_paths - new_paths
    f = open(os.path.join(backup_path, '.deletedfiles'),'w')
    f.writelines([replace_part(x, vault_path, '').replace('/',';').replace('\\',';')+'\n' for x in deleted_files])
    f.close()
    if (len(deleted_files) != 0):
        has_been_any_changes = True
    
    return has_been_any_changes





if __name__ == "__main__":
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent
    this_file = BASE_DIR / 'env' / 'Scripts' / 'activate_this.py'
    if (not this_file.exists()):
        this_file = BASE_DIR / 'env' / 'bin' / 'activate_this.py'

    exec(open(this_file).read(), {'__file__': this_file})

    import os
    import shutil
    import time

    from libs.filelib import *
    from libs.csvlib import *
    from libs.archive import *
    from libs.synclib import *
    from loadConfig import create_or_load_config
    from googledrivelibs.drivelib import upload_file_to_drive
    from googledrivelibs.auth import authenticate


    
    # Authenticate and get the Google Drive API service
    drive_service = authenticate()

    vault_path, backup_path, refresh_time, master_pass, folder_id = create_or_load_config()
    print(f"Vault Path: {vault_path}")
    print(f"Backup Path: {backup_path}")
    print(f"Refresh Time: {refresh_time} seconds")
    print(f"Master Password: {master_pass}")

    # Specify the CSV file to store the information
    create_folder('database')
    database_file = os.path.join('database', "database.csv")
    old_database_file = os.path.join('database', "old_database.csv")



    while (True):
        # Get file information recursively
        file_info_list = get_all_files_info(vault_path)
        # Write file information to CSV
        write_to_csv(file_info_list, database_file)
        print(f"File information has been stored in {database_file}.\n\n")

        backup_path = create_dated_folder(backup_path)
        has_been_any_changes = compare_databases(old_database_file, database_file)
        
        if (has_been_any_changes):
            archive(backup_path, master_pass)

            upload_file_to_drive(backup_path+'.7z', folder_id, drive_service)
        else:
            shutil.rmtree(backup_path)

        register_a_sync()
        fill_old_database(database_file, old_database_file)


        time.sleep(refresh_time)
