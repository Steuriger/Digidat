from flask import Flask, render_template
import requests
import time
from operator import itemgetter
from datetime import datetime, timedelta
import pytz
import schedule



app = Flask(__name__)

def determine_room_from_box_id(sensor_name):
    room_mapping = {
        "DIGIdat_AGIN_1": "4c 2. Stock", 
        "DIGIdat_AGIN_2": "4c 2. Stock",
        "DIGIdat_AGIN_3": "3c 2. Stock",
        "DIGIdat_AGIN_4": "3c 2. Stock",
        "DIGIdat_AGIN_5": "3c 2. Stock",
        "DIGIdat_AGIN_6": "2c 1. Stock",
        "DIGIdat_AGIN_7": "2c 1. Stock",
        "DIGIdat_AGIN_8": "2c 1. Stock",
        "DIGIdat_AGIN_9": "5b 3. Stock",
        "DIGIdat_AGIN_10": "Werk2 Untergeschoss",
        "DIGIdat_AGIN_11": "4c 2. Stock",
        "DIGIdat_AGIN_12": "Gang 2. Stock",
        "DIGIdat_AGIN_13": "5b 3. Stock",
        "DIGIdat_AGIN_14": "5b 3. Stock",
        "DIGIdat_AGIN_15": "Balkon"
    }
    return room_mapping.get(sensor_name, "\033[91mUnbekannter Raum\033[0m")

def format_time_difference(time_difference):
    total_seconds = time_difference.total_seconds()
    days = total_seconds // (24 * 3600)
    hours = (total_seconds % (24 * 3600)) // 3600
    minutes = (total_seconds % 3600) // 60
    formatted_time = ""
    if days > 0:
        formatted_time += f"{int(days)} Tage "
    if hours > 0:
        formatted_time += f"{int(hours)} Stunden "
    if minutes > 0:
        formatted_time += f"{int(minutes)} Minuten"
    if total_seconds < 60:
        formatted_time += f"<1 Minute"
    return formatted_time

def get_last_update_time():

    offline_boxes = {}
    base_url = f"https://api.opensensemap.org/boxes?grouptag=AGIN&full=true"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        last_updated_dates = list(map(itemgetter('updatedAt'), data))
        timezone = pytz.timezone('Europe/Berlin')
        current_time_naive = datetime.now()
        current_time = timezone.localize(current_time_naive)
        summertime = current_time.dst() != timedelta(0)
        box_id_list = [entry['_id'] for entry in data]
        school_name_list = [f'DIGIdat_AGIN_{i}' for i in range(1, 16)]
        offline_result_data = []
        online_result_data = []
        for index, box_id in enumerate(box_id_list):
            last_update = last_updated_dates[index]
            sensor_name = school_name_list[index]
            box_id = box_id_list[index]
            last_update_time = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S.%fZ")
            last_update_time = timezone.localize(last_update_time)

            status = None

            if summertime:
                last_update_time += timedelta(hours=2)
            else:
                last_update_time += timedelta(hours=1)
            time_difference = current_time - last_update_time
            formatted_time_difference = format_time_difference(time_difference)
            formatted_last_update = last_update_time.strftime("%Y-%m-%d %H:%M:%S")

            if time_difference <= timedelta(minutes=6):
                status = "online"
                online_result_data.append({
                    'sensor_name': sensor_name,
                    'time_difference': format_time_difference(time_difference),
                    'status': status,
                    'room': determine_room_from_box_id(sensor_name)
                })
            else:
                status = "offline"
                if sensor_name not in offline_boxes:
                    offline_result_data.append({
                        'sensor_name': sensor_name,
                        'time_difference': format_time_difference(time_difference),
                        'status': status
                    })

                    offline_boxes[sensor_name] = {
                        'room': determine_room_from_box_id(sensor_name),
                        'last_updated': formatted_time_difference
                    }

        return offline_result_data, online_result_data

    
    if __name__ == '__main__':
        schedule.every(60).seconds.do(get_last_update_time) 
        start_flask_app()


@app.route('/')
def index():
    sensor_data, online_result_data = get_last_update_time()
    formatted_output = []
    for item in sensor_data:
        data_box = {
            'sensor_name': item['sensor_name'],
            'status': item['status'],
            'time_difference': item['time_difference'],
            'room': determine_room_from_box_id(item['sensor_name'])
        }
        formatted_output.append(data_box)

    return render_template('index.html', data=formatted_output, online_data=online_result_data)

    
def start_flask_app():
    app.run(debug=True, extra_files=['templates/index.html'])

if __name__ == '__main__':
    schedule.every(60).seconds.do(get_last_update_time)
    start_flask_app()


    while True:
        schedule.run_pending()
        time.sleep(1)