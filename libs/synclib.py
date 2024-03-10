from datetime import datetime
import os

def register_a_sync(backup_folder, datetime = datetime.now().strftime("%d-%m-%Y__%H-%M-%S")):
    f=open(os.path.join(backup_folder, 'date.lastsync'), 'w')
    f.write(datetime)
    f.close()

def get_last_register(default_value='16-12-2023__01-00-00'):
    try:
        with open('date.lastsync', 'r') as f:
            time = f.readline()
            return time.strip()
    except FileNotFoundError:
        print("File 'date.lastsync' not found. Returning default value.")
        return default_value
    except Exception as e:
        print(f"Error reading file: {e}")
        return default_value


def filter_elements_by_date(elements, target_date_time):
    filtered_elements = []

    # Parse the target date and time
    target_datetime = datetime.strptime(target_date_time, "%d-%m-%Y__%H-%M-%S")

    # Filter elements based on the date and time
    for element in elements:
        try:
            element_datetime = datetime.strptime(element['name'][:19], "%d-%m-%Y__%H-%M-%S")
            if element_datetime > target_datetime:
                filtered_elements.append(element)
        except ValueError:
            print("Invalid date format. Please enter a date in the format YYYY-MM-DD. for "+element['name'])

    print(filtered_elements)
    return filtered_elements