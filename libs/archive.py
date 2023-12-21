
import os
import subprocess
import platform


def archive(backup_path, folder_to_archive,  master_pass):
    """
    Execute a command based on the operating system.
    """
    system_platform = platform.system().lower()
    archive_file = backup_path+".7z"
    folder_that_is_goingtobe_archived = os.path.join(folder_to_archive, '*')
    command = f'a "{archive_file}" -p"{master_pass}" -mhe=on "{folder_that_is_goingtobe_archived}"'

    return_code = 0
    try:
        if "windows" in system_platform:
            # Execute command on Windows
            return_code = subprocess.check_call(f'.\\7z\\7z_x64\\7za.exe {command}', shell=True)
        elif "linux" in system_platform:
            # Execute command on Linux
            return_code = subprocess.check_call(f'7za {command}', shell=True)
        else:
            print("Unsupported operating system.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

    return return_code


def extract(file, master_pass):
    """
    Execute a command based on the operating system.
    """
    system_platform = platform.system().lower()

    command = f'x "{file}" -p"{master_pass}" -o"{file[:-3]}"'
    return_code = 0
    try:
        if "windows" in system_platform:
            # Execute command on Windows
            return_code = subprocess.check_call(f'.\\7z\\7z_x64\\7za.exe {command}', shell=True, check=True)
        elif "linux" in system_platform:
            # Execute command on Linux
            return_code = subprocess.check_call(f'7za {command}', shell=True, check=True)
        else:
            print("Unsupported operating system.")

        
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    
    return return_code