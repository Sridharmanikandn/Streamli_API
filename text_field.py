import json
from datetime import datetime

# Your JSON response
json_response = "{'statusCode': 1001, 'msg': 'success', 'data': [{'slotId': '4dbec1af6f41a4d7b36121d5', 'date': '2024-03-08T10:30:00.000Z', 'bookingPerSlot': 3, 'bookedAppointments': 0, 'listOfAppointmentId': []}]}"

# Parse JSON
parsed_json = json.loads(json_response.replace("'", "\""))

# Extract date string
date_string = parsed_json['data'][0]['date']

# Convert to datetime object
datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

# Convert to a different date format (e.g., "%Y-%m-%d %H:%M:%S")
formatted_date = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

print(formatted_date)
