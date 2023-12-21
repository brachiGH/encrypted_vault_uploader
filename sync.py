vault_path = ''
backup_path = ''
refresh_time = ''
master_pass = ''
folder_id = ''


def set_a_backup(vault_path, backup_path, master_pass):
    backup_path = create_dated_folder(os.path.join(backup_path, "download_backup"))
    archive(backup_path, vault_path, master_pass)

if __name__ == "__main__":
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent
    this_file = BASE_DIR / 'env' / 'Scripts' / 'activate_this.py'
    if (not this_file.exists()):
        this_file = BASE_DIR / 'env' / 'bin' / 'activate_this.py'

    exec(open(this_file).read(), {'__file__': this_file})


    import os
    import time
    from libs.synclib import *
    from libs.archive import *
    from libs.filelib import *
    from loadConfig import create_or_load_config
    from googledrivelibs.auth import authenticate
    from googledrivelibs.drivelib import list_files_in_directory, download_file

    # Authenticate and get the Google Drive API service
    drive_service = authenticate()
    
    vault_path, backup_path, refresh_time, master_pass, folder_id = create_or_load_config()
    
    create_folder(backup_path)
    backup_path = os.path.join(backup_path, 'donwload')
    create_folder(backup_path)



    while (True):
        try:
            lastsync = get_last_register()
            files_list = list_files_in_directory(drive_service, folder_id)
            files_list = filter_elements_by_date(files_list, lastsync) # return files that are not download in the last sync
            files_list = sort_dicts_by_name(files_list) # sort files by date aka name

            print('#########################\n'+str(len(files_list))+' files to to download.\n')
            for drive_file in files_list:
                z_file_path = os.path.join(backup_path, drive_file['name'])
                delete_file(z_file_path)
                delete_folder(z_file_path[:-3])
                download_file(drive_service, drive_file['id'], z_file_path)
                return_code = extract(z_file_path, master_pass)

                if return_code ==0:
                    extracted_files_list = get_all_files_info(z_file_path[:-3])


                    for extracted_file in extracted_files_list:
                        if '.deletedfiles' in extracted_file[0]:
                            ## create backup
                            set_a_backup(vault_path, backup_path, master_pass)

                            deletefiles_file(extracted_file[0], vault_path)
                        else:
                            file_path_in_vault = replace_part(extracted_file[0], z_file_path[:-3], vault_path)
                            delete_file(file_path_in_vault)
                            copy_file_with_folders(extracted_file[0], file_path_in_vault)

                    register_a_sync(drive_file['name'][:-3])
                else:
                    print('AN ERR HAS ACCURRED WHILE EXTRACTING 7Z')
        except Exception as e:
            print("Err syncing files: "+str(e))

        print(f'################################\n\n\n{datenow_for_logging()}next action is in {seconds_to_hhmmss(refresh_time)}')
        time.sleep(refresh_time)