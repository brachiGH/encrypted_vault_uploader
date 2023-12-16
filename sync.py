vault_path = ''
backup_path = ''
refresh_time = ''
master_pass = ''
folder_id = ''


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
    from libs.archive import extract
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
            files_list = filter_elements_by_date(files_list, lastsync)

            print(str(len(files_list))+' files to to download.')
            for drive_file in files_list:
                z_file_path = os.path.join(backup_path, drive_file['name'])
                delete_file(z_file_path)
                delete_folder(z_file_path[:-3])
                download_file(drive_service, drive_file['id'], z_file_path)
                extract(z_file_path, master_pass)

                extracted_files_list = get_all_files_info(z_file_path[:-3])


                for extracted_file in extracted_files_list:
                    if '.deletedfiles' in extracted_file[0]:
                        deletefiles_file(extracted_file[0], vault_path)
                    else:
                        file_path_in_vault = replace_part(extracted_file[0], z_file_path[:-3], vault_path)
                        delete_file(file_path_in_vault)
                        copy_file_with_folders(extracted_file[0], file_path_in_vault)

                register_a_sync(drive_file['name'][:-3])
        except:
            print("Err syncing files")

        time.sleep(refresh_time)