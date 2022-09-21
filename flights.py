from datetime import datetime, timedelta

import pandas as pd


def update_flight_file():
    success_count = 0
    df = pd.read_csv("flight.csv")
    flights = sorted(df.to_numpy(), key=lambda flight_info: datetime.strptime(flight_info[1].strip(), "%H:%M"))
    for flight in flights:
        if success_count == 20:
            break
        time = datetime.strptime(flight[2].strip(), "%H:%M") - datetime.strptime(flight[1].strip(), "%H:%M")
        if time.seconds >= 180 * 60:
            flight[3] = 'success'
            success_count += 1
        else:
            flight[3] = 'fail'
    for flight in flights:
        print(flight)


update_flight_file()
