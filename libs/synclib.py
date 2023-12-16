from datetime import datetime


def register_a_sync(datetime = datetime.now().strftime("%d-%m-%Y__%H-%M-%S")):
    f=open('date.lastsync', 'w')
    f.write(datetime)
    f.close()

def get_last_register():
    f=open('date.lastsync', 'r')
    time = f.readline()
    f.close()

    return time.strip()


def filter_elements_by_date(elements, target_date_time):
    filtered_elements = []

    # Parse the target date and time
    target_datetime = datetime.strptime(target_date_time, "%d-%m-%Y__%H-%M-%S")

    # Filter elements based on the date and time
    for element in elements:
        element_datetime = datetime.strptime(element['name'][:19], "%d-%m-%Y__%H-%M-%S")
        if element_datetime > target_datetime:
            filtered_elements.append(element)

    return filtered_elements