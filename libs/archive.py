
import os
import subprocess
import platform


def archive(backup_path, master_pass):
    """
    Execute a command based on the operating system.
    """
    system_platform = platform.system().lower()
    archive_file = backup_path+".7z"
    folder_that_is_goingtobe_archived = os.path.join(backup_path, '*')
    command = f'a "{archive_file}" -p"{master_pass}" -mhe=on "{folder_that_is_goingtobe_archived}"'
    try:
        if "windows" in system_platform:
            # Execute command on Windows
            subprocess.run(f'.\\7z\\7z_x64\\7za.exe {command}', shell=True, check=True)
        elif "linux" in system_platform:
            # Execute command on Linux
            subprocess.run(f'7za {command}', shell=True, check=True)
        else:
            print("Unsupported operating system.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")


def extract(file, master_pass):
    """
    Execute a command based on the operating system.
    """
    system_platform = platform.system().lower()

    command = f'x "{file}" -p"{master_pass}" -o"{file[:-3]}"'
    try:
        if "windows" in system_platform:
            # Execute command on Windows
            subprocess.run(f'.\\7z\\7z_x64\\7za.exe {command}', shell=True, check=True)
        elif "linux" in system_platform:
            # Execute command on Linux
            subprocess.run(f'7za {command}', shell=True, check=True)
        else:
            print("Unsupported operating system.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")