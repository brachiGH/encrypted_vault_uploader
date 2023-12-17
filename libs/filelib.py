
import os
import shutil
from datetime import datetime

def get_modification_time(path, data):
    """
    Get the modification time for a given file path from the provided data.
    """
    for item in data:
        if item[0] == path:
            return item[1]
    return None


def get_all_files_info(path):
    """
    Recursively get file information (path and last modification time) for a given directory.
    """
    file_info_list = []

    for root, dirs, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            file_info_list.append((file_path, int(mod_time.timestamp())))

    return file_info_list


def replace_part(original_string, old_part, new_part):
    """
    Replace a part of the original string with a new part.
    """
    modified_string = original_string.replace(old_part, new_part)
    return modified_string


def create_folder(folder_path):
    """
    Create a folder if it does not exist.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        print(f"Folder already exists: {folder_path}")

def create_dated_folder(base_path):
    """
    Create a folder with a name based on the current date and time.
    Returns the full path of the created folder.
    """
    current_datetime = datetime.now()
    folder_name = current_datetime.strftime("%d-%m-%Y__%H-%M-%S")
    folder_path = os.path.join(base_path, folder_name)

    try:
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    except FileExistsError:
        print(f"Folder already exists: {folder_path}")


    return folder_path




def copy_file_with_folders(source_file, destination_folder):
    """
    Copy a file to a destination folder, creating folders and subfolders if they don't exist.
    """
    try:
        # Ensure the destination folder and its parent folders exist
        os.makedirs(os.path.dirname(destination_folder), exist_ok=True)

        # Use shutil.copy to copy the file to the destination folder
        shutil.copy(source_file, destination_folder)
    except Exception as e:
        print(f"Error copying file: {e}")


def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' successfully deleted.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"Error deleting file: {e}")


def deletefiles_file(path, vault_path):
    with open(path, 'r') as file:
        for line in file:
            components = [vault_path] + line.strip().split(';')
            file_path = os.path.join(*components)
            delete_file(file_path)



def fill_old_database(database_file, old_database_file):
    delete_file(old_database_file)
    copy_file_with_folders(database_file, old_database_file)



def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted successfully.")
    except Exception as e:
        print(f"Folder '{folder_path}' does not exist.")

def seconds_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def sort_dicts_by_name(dict_list):
    # Define a custom sorting key function
    def custom_sorting_key(d):
        return datetime.strptime(d['name'], "%d-%m-%Y__%H-%M-%S")

    # Use the sorted function with the custom sorting key
    sorted_dict_list = sorted(dict_list, key=custom_sorting_key)

    return sorted_dict_list