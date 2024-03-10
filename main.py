
def compare_databases(old_db_file, new_db_file, vault_path, backup_path, master_pass):
    """
    Compare two databases.csv files and print paths for new, modified, and deleted files.
    """
    has_been_any_changes = False


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

    vault_path, backup_folder, refresh_time, master_pass, folder_id, folders_count = create_or_load_config()
    print(f"Vault Path: {vault_path}")
    print(f"Backup Path: {backup_folder}")
    print(f"Refresh Time: {refresh_time} seconds")


    database_file = []
    old_database_file = []
    for i in range(folders_count):
        database_path =  os.path.join(backup_folder[i], "database")
        create_folder(database_path)
        database_file.append(os.path.join(database_path, "database.csv"))
        old_database_file.append(os.path.join(database_path, "old_database.csv"))




    #turn list to dict
    config_elements = [
        {'vault_path': v, 'backup_folder': b, 'refresh_time': r, 'master_pass': p, 'folder_id': i,'database_file':d, 'old_database_file':od}
        for v, b, r, p, i, d, od in zip(vault_path, backup_folder, refresh_time, master_pass, folder_id, database_file, old_database_file)
    ]

    config_elements = sorted(config_elements, key=lambda x: x['refresh_time'])
    first_time = True
    waited_time = 9999999999999 #this will allow all configs to run hceck the max fucntion in (time.Sleep - waited_time)
    while (True):
        for i in range(folders_count):
            # Get file information recursively
            file_info_list = get_all_files_info(config_elements[i]['vault_path'])
            # Write file information to CSV
            write_to_csv(file_info_list, config_elements[i]['database_file'])
            print(f"File information has been stored in {config_elements[i]['database_file']}.\n\n")

            backup_path = create_dated_folder(config_elements[i]['backup_folder'])
            has_been_any_changes = compare_databases(config_elements[i]['old_database_file'], config_elements[i]['database_file']
                                                    ,config_elements[i]['vault_path'],backup_path
                                                    ,config_elements[i]['master_pass'])
            
            has_been_any_changes = 1
            if (has_been_any_changes):
                return_code = archive(backup_path, backup_path, config_elements[i]['master_pass'])

                if return_code ==0:
                    upload_file_to_drive(backup_path+'.7z', config_elements[i]['folder_id'], drive_service)
                else:
                    print('AN ERR HAS ACCURRED WHILE USING 7Z')
            else:
                shutil.rmtree(backup_path)

            if return_code == 0:
                register_a_sync(config_elements[i]['backup_folder'])
                fill_old_database(config_elements[i]['database_file'], config_elements[i]['old_database_file'])

            print(f'################################\n\n\n{datenow_for_logging()}next action is in {seconds_to_hhmmss(config_elements[i]['refresh_time'])}')
            time.sleep(max(config_elements[i]['refresh_time'] - waited_time, 0))
            waited_time = config_elements[i]['refresh_time']
        
        
        if first_time:
            first_time = False
            time.sleep(max([element['refresh_time'] for element in config_elements]))
        else:
            waited_time = 0
