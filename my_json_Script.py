import pandas as pd
from datetime import datetime

json_response = {
    'statusCode': 1001,
    'msg': 'success',
    'data': {
        'slots': [
            {
                'slotId': '58a5b4cccfc4321ce085e904',
                'date': '2024-03-13T18:00:00.000Z',
                'bookingPerSlot': 10,
                'bookedAppointments': 2,
                'listOfAppointmentId': ['78fcced4418b49ed8df81032', '65f173005adccd7e3012f480']
            },
            {
                'slotId': '55cad02e38c3a6016d0452e1',
                'date': '2024-03-13T22:30:00.000Z',
                'bookingPerSlot': 25,
                'bookedAppointments': 2,
                'listOfAppointmentId': ['65f1b1059f6966462b056ea8', '65f1b2d39f6966462b0570e2']
            },
            {
                'slotId': '62272520434225ea3e9d7f15',
                'date': '2024-03-14T22:30:00.000Z',
                'bookingPerSlot': 25,
                'bookedAppointments': 5,
                'listOfAppointmentId': ['65f28b139f6966462b057a33', '65f28b359f6966462b057a61', '65f28b4d9f6966462b057a7e', '65f28b679f6966462b057a9b', '65f28d0c9f6966462b057b8d']
            }
        ]
    }
}

for slot in json_response['data']['slots']:
    slot['date'] = datetime.strptime(slot['date'], '%Y-%m-%dT%H:%M:%S.%fZ')

slots_data = json_response['data']['slots']

df = pd.DataFrame(slots_data)

df.to_csv('slots1_data.csv', index=False)

print("Data exported successfully.")
