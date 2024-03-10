import configparser
from libs.filelib import *
from pathlib import Path

def list_files_in_folder(folder_path):
    """
    Print all files in the specified folder.

    Args:
    - folder_path (str): Path to the folder to list files from.
    """
    print("Files in the folder:")
    files = os.listdir(folder_path)
    for index, file_name in enumerate(files, start=1):
        print(f"{index}. {file_name}")
    return files



def get_files_in_config(config_folder_path, is_sync):
    if not is_sync:
        return os.walk(config_folder_path)
    else:
        files = list_files_in_folder(config_folder_path)

        if files:
            while True:
                try:
                    selection = int(input("Select a file by entering its number: "))
                    if 1 <= selection <= len(files):
                        selected_file = files[selection - 1]
                        print(f"You selected: {selected_file}")
                        break
                    else:
                        print("Invalid selection. Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("No files found in the folder.")

        return [(config_folder_path, "", [selected_file])]

def create_or_load_config(is_sync=0):
    config = configparser.ConfigParser()

    config_folder_path = "config"
    vault_path = []
    backup_path = []
    refresh_time = []
    master_pass = []
    folder_id = []
    folders_count = 0


    if not os.listdir(config_folder_path) and is_sync==0:
        print("Config Folder Is Empty!")
        create_config(config_file_path = None)

        #retry
        return create_or_load_config()
    else:
        for root, dirs, files in get_files_in_config(config_folder_path, is_sync):
            for file_name in files:
                config_file_path = os.path.join(root, file_name) # e.g "config.cfg"

                # Load the config file
                config.read(config_file_path)

                # Check for missing values and prompt the user for input
                if not config.has_section("Settings"):
                    config.add_section("Settings")

                if not config.has_option("Settings", "vault_path") or not config.get("Settings", "vault_path"):
                    config.set("Settings", "vault_path", input("Enter the vault path for '{}': ".format(file_name)))

                if not config.has_option("Settings", "backup_path") or not config.get("Settings", "backup_path"):
                    config.set("Settings", "backup_path", input("Enter the backup path for '{}': ".format(file_name)))

                if not config.has_option("Settings", "refresh_time") or not config.get("Settings", "refresh_time"):
                    config.set("Settings", "refresh_time", input("Enter the refresh time (in seconds) for '{}': ".format(file_name)))

                if not config.has_option("Settings", "master_pass") or not config.get("Settings", "master_pass"):
                    config.set("Settings", "master_pass", input("Enter the master password for '{}': ".format(file_name)))

                if not config.has_option("Settings", "folder_id") or not config.get("Settings", "folder_id"):
                    config.set("Settings", "folder_id", input("Enter the google drive folder_id for '{}': ".format(file_name)))

                # Save the updated config
                with open(config_file_path, "w") as config_file:
                    config.write(config_file)

                print("{} loaded or created successfully.".format(file_name))

                # Return the configuration values
                vault_path.append(config.get("Settings", "vault_path"))
                if not os.path.exists(vault_path[-1]): # check if folder exist
                    config.set("Settings", "vault_path", input("Enter a valid vault path for '{}': ".format(file_name)))
                    vault_path[-1] = config.get("Settings", "vault_path")

                backup_path.append(config.get("Settings", "backup_path"))
                refresh_time.append(int(config.get("Settings", "refresh_time")))
                master_pass.append(config.get("Settings", "master_pass"))
                folder_id.append(config.get("Settings", "folder_id"))

                create_folder(backup_path[-1])
                folders_count = folders_count + 1

    if is_sync:
        return vault_path[0], backup_path[0], refresh_time[0], master_pass[0], folder_id[0]
    else:
        return vault_path, backup_path, refresh_time, master_pass, folder_id, folders_count

def create_config(config_file_path = None):
    config = configparser.ConfigParser()
    config.add_section("Settings")

    config.set("Settings", "vault_path", input("Enter the vault path: "))
    config.set("Settings", "backup_path", input("Enter the backup path: "))
    config.set("Settings", "refresh_time", input("Enter the refresh time (in seconds): "))
    config.set("Settings", "master_pass", input("Enter the master password: "))
    config.set("Settings", "folder_id", input("Enter the google drive folder_id: "))

    if config_file_path == None:
        config_file_path = Path("config") / Path(config.get("Settings", "backup_path")).parts[-1]

    with open(config_file_path, "w") as config_file:
        config.write(config_file)

