import configparser
from libs.filelib import *




def create_or_load_config():
    config = configparser.ConfigParser()

    # Check if the config file exists
    config_file_path = "config.cfg"

    if not os.path.exists(config_file_path):
        print("Config file does not exist. Creating a new one.")
        create_config(config, config_file_path)

    # Load the config file
    config.read(config_file_path)

    # Check for missing values and prompt the user for input
    if not config.has_section("Settings"):
        config.add_section("Settings")

    if not config.has_option("Settings", "vault_path") or not config.get("Settings", "vault_path"):
        config.set("Settings", "vault_path", input("Enter the vault path: "))

    if not config.has_option("Settings", "backup_path") or not config.get("Settings", "backup_path"):
        config.set("Settings", "backup_path", input("Enter the backup path: "))

    if not config.has_option("Settings", "refresh_time") or not config.get("Settings", "refresh_time"):
        config.set("Settings", "refresh_time", input("Enter the refresh time (in seconds): "))

    if not config.has_option("Settings", "master_pass") or not config.get("Settings", "master_pass"):
        config.set("Settings", "master_pass", input("Enter the master password: "))

    if not config.has_option("Settings", "folder_id") or not config.get("Settings", "folder_id"):
        config.set("Settings", "folder_id", input("Enter the google drive folder_id: "))

    # Save the updated config
    with open(config_file_path, "w") as config_file:
        config.write(config_file)

    print("Config loaded or created successfully.")

    # Return the configuration values
    vault_path = config.get("Settings", "vault_path")
    if not os.path.exists(vault_path): # check if folder exist
        config.set("Settings", "vault_path", input("Enter a valid vault path: "))
        vault_path = config.get("Settings", "vault_path")

    backup_path = config.get("Settings", "backup_path")
    refresh_time = int(config.get("Settings", "refresh_time"))
    master_pass = config.get("Settings", "master_pass")
    folder_id = config.get("Settings", "folder_id")

    create_folder(backup_path)

    return vault_path, backup_path, refresh_time, master_pass, folder_id

def create_config(config, config_file_path):
    config.add_section("Settings")

    config.set("Settings", "vault_path", input("Enter the vault path: "))
    config.set("Settings", "backup_path", input("Enter the backup path: "))
    config.set("Settings", "refresh_time", input("Enter the refresh time (in seconds): "))
    config.set("Settings", "master_pass", input("Enter the master password: "))
    config.set("Settings", "folder_id", input("Enter the master password: "))

    with open(config_file_path, "w") as config_file:
        config.write(config_file)

