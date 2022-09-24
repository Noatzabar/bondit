from datetime import datetime

import pandas as pd
from flask import Flask, jsonify
app = Flask(__name__)


class Flights:

    def __init__(self):
        self.df = pd.read_csv("flight.csv")
        self.db = {}
        for flight in self.df.to_numpy():
            self.db[flight[0]] = flight[1:]

    def get_flight_by_id(self, flight_id):
        flight = self.db.get(flight_id)
        return {'Arrival': flight[0], 'Departure': flight[1], 'success': flight[2]}

    def update_flight(self, flight_id, arrival, departure, success):
        try:
            flight_info = [flight_id, arrival, departure, success]
            self.db[flight_id] = flight_info[1:]
            self.df = self.df[self.df['flight ID'] != flight_id]
            self.df.to_csv("flight.csv", index=False)
            new_flight = {'flight ID': [flight_id], 'Arrival': [arrival], 'Departure': [departure], 'success': [success]}
            df = pd.DataFrame(new_flight)
            df.to_csv("flight.csv", mode='a', index=False, header=False)
            self.df = pd.read_csv("flight.csv")
            return "success"
        except Exception:
            return "fail"

    def update_flight_file_with_success(self):
        success_count = 0
        flights = sorted(self.df.to_numpy(), key=lambda flight_info: datetime.strptime(flight_info[1].strip(), "%H:%M"))
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


@app.get("/get_info_about_flight/<flight_id>")
def get_info_about_flight(flight_id):
    return jsonify(flight_manager.get_flight_by_id(flight_id))


@app.post("/update_info_about_flight/<flight_id>/<arrival>/<departure>/<success>")
def set_info_about_flight(flight_id, arrival, departure, success):
    return jsonify(flight_manager.update_flight(flight_id, arrival, departure, success))


if __name__ == "__main__":
    flight_manager = Flights()
    app.run()
